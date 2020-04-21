from selenium.webdriver import chrome
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from correo import Correo
from temporizador import Temporizador
from selenium_testing_utils import SeleniumTesting
from format_utils import FormatUtils
from statusJson import JsonPorEnviar
from validacion_result import Result
from validacion_result import EvaluacionStepsJson
from validacion_result import ValidacionResultList
import constantes_json
import configparser
import sys
import logging
import time
import json
import datetime
import os
                    
correos_obtenidos = []

# funcion encargada de configurar el driver a utilizar (chrome o firefox)
# dependiendo de los valores que se hayan establecido dentro del archivo
# de configuracion (.ini)
def configurar_webdriver(driver_por_usar, ruta_driver_navegador):
    driver = None

    if len(ruta_driver_navegador.strip()) == 0:
        logging.info('Favor de establecer la ruta del driver por utilizar')
        sys.exit()

    if driver_por_usar == 'chrome':
        logging.info('Configurando driver chrome')
        driver = SeleniumTesting.inicializar_webdriver_chrome(ruta_driver_navegador.strip())
    elif driver_por_usar == 'firefox':
        logging.info('Configurando driver firefox')
        driver = SeleniumTesting.inicializar_webdriver_firefox(ruta_driver_navegador.strip())
    elif driver_por_usar == 'phantomjs':
        logging.info('Configurando driver phantomjs')
        driver = SeleniumTesting.inicializar_webdriver_phantom_js(ruta_driver_navegador.strip())
    else:
        logging.info('Favor de establecer el driver a configurar (chrome o firefox)')
        sys.exit()

    return driver


def generar_test_json(driver, url_a_navegar, correo):
    lista_carpetas_por_navegar = []
    objeto_json = None

    # objeto con lista de objetos result el cual verificara cada una de 
    # las validaciones para cada uno de los steps y el cual nos permitira adjuntar 
    # el resultado en el JSON
    lista_validaciones = ValidacionResultList()

    # genera la estructura del archivo JSON (resultado/salida)
    objeto_json = JsonPorEnviar.generar_nuevo_template_json()

    # establece el datetime de inicio dentro del json
    objeto_json = EvaluacionStepsJson.establecer_fecha_tiempo_de_inicio(objeto_json)

    # empieza la primera validacion de ingresar a la url del portal
    lista_validaciones = SeleniumTesting.navegar_a_sitio(driver, url_a_navegar, lista_validaciones)

    # intenta ingresar las credenciales de la cuenta dentro del portal, verificando
    # el acceso del correo desde el portal 
    lista_validaciones = SeleniumTesting.iniciar_sesion_en_owa(driver, correo, lista_validaciones)

    # se obtiene la lista de carpetas que contiene el correo electronico
    lista_carpetas_por_navegar = SeleniumTesting.obtener_carpetas_en_sesion(driver)

    # empieza la validacion de la navegacion en cada una de las carpetas que se obtuvieron
    # en la linea anterior
    lista_validaciones = SeleniumTesting.navegacion_de_carpetas_por_segundos(
        lista_carpetas_por_navegar, driver,lista_validaciones)

    # se valida el cierre de sesion desde el OWA
    lista_validaciones = SeleniumTesting.cerrar_sesion(driver, lista_validaciones)

    # establece los datos en el json con los resultados de cada una de las validaciones
    objeto_json = EvaluacionStepsJson.formar_cuerpo_json(lista_validaciones, objeto_json, correo)

    return objeto_json

def iniciar_prueba(correo, url_exchange):
    
    # obtiene los datos del archivo de configuracion
    archivo_configuracion_ini = FormatUtils.lector_archivo_ini()
    driver_por_usar = FormatUtils.CADENA_VACIA
    ruta_driver_navegador = FormatUtils.CADENA_VACIA
    driver = None
    objeto_json = None

    try:
        # url_exchange = archivo_configuracion_ini.get('UrlPorProbar','urlPortalExchange')
        driver_por_usar = archivo_configuracion_ini.get('Driver', 'driverPorUtilizar')
        ruta_driver_navegador = archivo_configuracion_ini.get('Driver', 'ruta')
    except configparser.Error as e:
        logging.error('Sucedio un error al momento de leer el archivo de configuracion')
        logging.error('{}'.format(e.message))
        sys.exit()

    # lista de carpetas por navegar (estos los obtenemos por medio del webdriver)
    carpetas_formateadas = []

    # obtiene los datos necesarios desde el archivo de configuracion

    # establece el driver por utilizar (chrome o firefox)
    driver = configurar_webdriver(driver_por_usar, ruta_driver_navegador)

    # se generan las validaciones y el resultado por medio de un objeto JSON
    objeto_json = generar_test_json(driver, url_exchange, correo)

    # se retorna el objeto json como cadena
    return json.dumps(objeto_json)


def configuracion_log():

    # verifica si el folder del log existe
    if not os.path.isdir(constantes_json.DIR_BASE_LOG):
        os.mkdir(constantes_json.DIR_BASE_LOG)

    # verifica que el archivo del log exista en caso contrario lo crea
    if not os.path.exists(constantes_json.PATH_ABSOLUTO_LOG):
        log = open(constantes_json.PATH_ABSOLUTO_LOG, 'x')
        log.close()

    logging.basicConfig(level=logging.INFO, 
                        filename=constantes_json.PATH_ABSOLUTO_LOG, 
                        filemode='w+', 
                        format='%(asctime)s  %(name)s  %(levelname)s: %(message)s', 
                        datefmt='%d-%m-%YT%H:%M:%S')
    
    logging.info('Inicializando log: {}'.format(constantes_json.PATH_ABSOLUTO_LOG))



# Punto de partida/ejecucion principal del script
def main(cadena_json=''):
    response = FormatUtils.CADENA_VACIA
    correo_a_probar = None

    constantes_json.configuracion_archivo_configuracion(__file__)
    configuracion_log()
    
    # verifica que la cadena sea un json valido en caso contrario 
    # se omite la experiencia de usuario
    cadena_json = cadena_json.strip()
    if FormatUtils.cadena_a_json_valido(cadena_json):
        logging.info('"{}" - JSON valido'.format(cadena_json))
        
        objeto_json = json.loads(cadena_json)

        url_exchange = objeto_json['url']
        usuario = objeto_json['user']
        password = objeto_json['password']

        correo_a_probar = Correo(usuario, password, url_exchange)
        
        response = iniciar_prueba(correo_a_probar, correo_a_probar.url)
    else:
        logging.error('"{}" - JSON invalido, se omite exp. de usuario'.format(cadena_json))
        print('"{}" - JSON invalido, se omite exp. de usuario'.format(cadena_json))
        response = '"{}" - JSON invalido, se omite exp. de usuario'.format(cadena_json)

    return response