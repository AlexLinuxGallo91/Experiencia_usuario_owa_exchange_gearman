from selenium import webdriver
from selenium.webdriver import chrome
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from validacion_result import ValidacionResultList
from correo import Correo
from format_utils import FormatUtils
from temporizador import Temporizador
from validacion_result import Result
import warnings
import constantes_json
import logging
import json
import time
import sys

class SeleniumTesting:

    # variable/bandera el cual indica que version del owa se esta analizando
    owa_descubierto = 0
    cuenta_sin_dominio = ''
    url_owa_exchange = ''
    log = logging.getLogger(__name__)

    # bandera para revisar si se encontro error en la plataforma
    mensaje_error_encontrado_owa = False
    txt_mensaje_error_encontrado_owa = ''


    # inicializa un nuevo driver (phantomjs) para la experiencia de usuario
    # con el uso del navegador Phantom JS
    @staticmethod
    def inicializar_webdriver_phantom_js(path_driver):

        webdriver_phantomjs = None

        # suprime el mensaje warning del uso de phantomjs ya que es una libreria obsoleta
        warnings.filterwarnings('ignore')
        
        try:
            webdriver_phantomjs = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any'], 
                                                      executable_path=path_driver, 
                                                      service_log_path=constantes_json.DEV_NULL
                                                      )
            webdriver_phantomjs.set_window_size(1120,550)
        except FileNotFoundError as e:
            SeleniumTesting.log.error('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            #sys.exit()
        except Exception as e:
            SeleniumTesting.log.error('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            #sys.exit()

        return webdriver_phantomjs


    # inicializa un nuevo driver (firefox) para la experiencia de usuario
    # con el uso del navefador Mozilla Firefox
    @staticmethod
    def inicializar_webdriver_firefox(path_driver):
        #ruta para deshabilitar log inecesario del geckodriver
        webdriver_firefox = None
        opciones_firefox = webdriver.FirefoxOptions()
        perfil_firefox = webdriver.FirefoxProfile()
        
        firefox_capabilities = webdriver.DesiredCapabilities().FIREFOX.copy()
        firefox_capabilities.update(
            {'acceptInsecureCerts': True, 'acceptSslCerts': True})
        firefox_capabilities['acceptSslCerts'] = True

        # ignora las certificaciones de seguridad, esto solamente se realiza
        # para la experiencia de usuario
        opciones_firefox.add_argument('--ignore-certificate-errors')
        opciones_firefox.accept_insecure_certs = True
        perfil_firefox.accept_untrusted_certs = True
        perfil_firefox.assume_untrusted_cert_issuer = False

        opciones_firefox.headless = True
        try:
            webdriver_firefox = webdriver.Firefox(executable_path=path_driver,
                                 firefox_options=opciones_firefox,
                                 firefox_profile=perfil_firefox,
                                 capabilities=firefox_capabilities,
                                 log_path=constantes_json.DEV_NULL
                                 )
        except FileNotFoundError as e:
            SeleniumTesting.log.error('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            #sys.exit()
        except Exception as e:
            SeleniumTesting.log.error('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            #sys.exit()

        return webdriver_firefox

    # inicializa un nuevo driver (chrome driver) para la experiencia de usuario
    # con el uso del navefador google chrome
    @staticmethod
    def inicializar_webdriver_chrome(path_driver):

        webdriver_chrome = None

        opciones_chrome = webdriver.ChromeOptions()

        # ignora las certificaciones de seguridad, esto solamente se realiza
        # para la experiencia de usuario
        opciones_chrome.add_argument('--ignore-certificate-errors')
        opciones_chrome.add_argument("--headless")
        opciones_chrome.add_argument('--allow-running-insecure-content')
        opciones_chrome.add_argument("--enable-javascript")
        opciones_chrome.add_argument('window-size=1920x1080')
        opciones_chrome.add_argument('--no-sandbox')
        opciones_chrome.add_experimental_option('excludeSwitches', ['enable-logging'])

        chrome_capabilities = webdriver.DesiredCapabilities().CHROME.copy()
        chrome_capabilities['acceptSslCerts'] = True
        chrome_capabilities['acceptInsecureCerts'] = True

        try:
            webdriver_chrome = webdriver.Chrome(path_driver, 
                                                chrome_options=opciones_chrome,
                                                desired_capabilities=chrome_capabilities,
                                                service_log_path=constantes_json.DEV_NULL)
        except FileNotFoundError as e:
            SeleniumTesting.log.error('Sucedio un error al intentar configurar el webdriver: {}'.format(e))
            #sys.exit()
        except Exception as e:
            SeleniumTesting.log.error('Sucedio una excepcion al intentar configurar el webdriver {}'.format(e))
            #sys.exit()

        return webdriver_chrome

    # funcion el cual permite navegar hacia la url que se establezca como parametro
    @staticmethod
    def navegar_a_sitio(webdriver, url_a_navegar, result_list):

        resultado = Result()
        resultado.tiempo_inicio_de_ejecucion = 0
        resultado.inicializar_tiempo_de_ejecucion()

        SeleniumTesting.log.info(
            'ingresando a la siguiente url: "{}"'.format(url_a_navegar))
        try:
            webdriver.set_page_load_timeout(100)
            webdriver.get(url_a_navegar)

            resultado.mensaje_error = 'Accediendo a la pagina principal de la plataforma Exchange'\
                                      ' OWA con exito, url actual: "{}"'.format(url_a_navegar)
            
            resultado.validacion_correcta = True
            SeleniumTesting.log.info(resultado.mensaje_error)

        except TimeoutException as e:
            
            resultado.mensaje_error = 'Han transcurrido mas de 60 segundos sin poder acceder a la '\
                                      'pagina principal de la plataforma "{}": {}'.format(url_a_navegar, SeleniumTesting.formatear_excepcion(e))
            
            resultado.validacion_correcta = False
           
            SeleniumTesting.log.error(resultado.mensaje_error)
        except WebDriverException as e:
            resultado.mensaje_error = 'No fue posible ingresar a la plataforma de Exchange OWA, favor de verificar'\
                ' si se tiene conectividad por internet, error detallado : {}'.format(
                SeleniumTesting.formatear_excepcion(e))
            resultado.validacion_correcta = False
            SeleniumTesting.log.error(resultado.mensaje_error)

        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_ingreso_url = resultado
        
        return result_list


    # Metodo el cual se encarga de establecer las credenciales en los inputs de la pagina principal del OWA
    @staticmethod
    def iniciar_sesion_en_owa(driver, correo_en_prueba, result_list):
        # verificacion en texto de mensajes de error en inicio de sesion
        error_security_context = 'NegotiateSecurityContext'

        # se obtiene la cuenta sin el origen del dominio
        SeleniumTesting.cuenta_sin_dominio = FormatUtils.formatear_correo(correo_en_prueba.correo)
        SeleniumTesting.url_owa_exchange = correo_en_prueba.url

        #xpath de botones owa 2010, 2016, 2013
        xpath_btn_owa_2010 = "//input[@type='submit'][@class='btn']"
        xpath_btn_owa_2013_2016 = "//div[@class='signinbutton']"

        driver.accept_insecure_certs = True
        driver.accept_untrusted_certs = True

        resultado = Result()

        resultado.tiempo_inicio_de_ejecucion = Temporizador.obtener_tiempo_timer()
        resultado.datetime_inicial = Temporizador.obtener_fecha_tiempo_actual()

        # resultado.inicializar_tiempo_de_ejecucion()
        mensaje_error_de_credenciales = None

        try:
            # obtiene los elementos html para los campos de usuario, password y el boton de inicio de
            # sesion
            time.sleep(3)

            input_usuario = driver.find_element_by_id('username')
            input_password = driver.find_element_by_id('password')
            check_casilla_owa_2010_version_ligera = None
            boton_ingreso_correo = None

            # verifica si se encuentra la casilla con el id chkBsc, el cual pertenece a la version
            # ligera de la plataforma de Exchange 2010
            if SeleniumTesting.verificar_elemento_encontrado_por_id(driver, 'chkBsc'):
                
                # selecciona el check para ingresar a la plataforma ligera
                check_casilla_owa_2010_version_ligera = driver.find_element_by_id('chkBsc')
                check_casilla_owa_2010_version_ligera.click()
                SeleniumTesting.owa_descubierto = 2010

            if SeleniumTesting.verificar_elemento_encontrado_por_xpath(driver, xpath_btn_owa_2010):
                boton_ingreso_correo = driver.find_element_by_xpath(xpath_btn_owa_2010)
                SeleniumTesting.owa_descubierto = 2010

            elif SeleniumTesting.verificar_elemento_encontrado_por_xpath(driver, xpath_btn_owa_2013_2016):
                boton_ingreso_correo = driver.find_element_by_xpath(
                    xpath_btn_owa_2013_2016)
                
                # establece la bandera version owa por analizar
                SeleniumTesting.owa_descubierto = 2016

            # ingresa los datos en cada uno de los inputs localizados en el sitio de owa, uno por
            # cada segundo
            time.sleep(1)
            input_usuario.send_keys(correo_en_prueba.correo)

            time.sleep(1)
            input_password.send_keys(correo_en_prueba.password)

            time.sleep(1)
            boton_ingreso_correo.click()

            time.sleep(18)

            SeleniumTesting.log.info('Titulo actual de la plataforma: {}'.format(driver.title))
            SeleniumTesting.log.info('URL actual de la plataforma: {}'.format(driver.current_url))
        
        except NoSuchElementException as e:
            
            resultado.mensaje_error = 'No fue posible iniciar sesion dentro de la plataforma OWA, '\
                                      'no se localizaron los inputs para ingresar las credenciales de la cuenta '\
                                      'de correo electronico Exchange: {}'.format(SeleniumTesting.formatear_excepcion(e))

            resultado.validacion_correcta = False
            SeleniumTesting.log.error(resultado.mensaje_error)
        
        except WebDriverException as e:
            
            resultado.mensaje_error = 'No fue posible ingresar a la plataforma de Exchange OWA, favor de verificar'\
                ' si se tiene conectividad por internet, error detallado : {}'.format(SeleniumTesting.formatear_excepcion(e))
            resultado.validacion_correcta = False
            SeleniumTesting.log.error(resultado.mensaje_error)

        # verifica que se haya ingresado correctamente al OWA, se localiza si esta establecido
        # el mensaje de error de credenciales dentro del aplicativo del OWA

        if resultado.validacion_correcta == False:
            try:

                if SeleniumTesting.owa_descubierto == 2010:

                    mensaje_error_de_credenciales = driver.find_element_by_id('trInvCrd')

                    SeleniumTesting.log.error('No fue posible ingresar a la plataforma OWA, se tiene error de credenciales')
                    mensaje_error_de_credenciales = driver.find_element_by_xpath("//tr[@id='trInvCrd']/td")
                    
                    texto_mensaje_error = mensaje_error_de_credenciales.get_attribute('innerHTML')
                    
                    SeleniumTesting.log.error('Se muestra el siguiente mensaje de error de credenciales: {} '\
                                            .format(texto_mensaje_error))
                    
                    resultado.mensaje_error = 'No fue posible ingresar a la plataforma OWA, se tiene error de credenciales: {}'\
                        .format(mensaje_error_de_credenciales.get_attribute('innerHTML'))
                        
                    resultado.validacion_correcta = False

                elif SeleniumTesting.owa_descubierto == 2016 or SeleniumTesting.owa_descubierto == 2013:
                    
                    mensaje_error_de_credenciales = driver.execute_script(
                    '''
                    var mensaje_error = document.querySelector("#signInErrorDiv").innerText;
                    return mensaje_error;
                    '''
                    )

                    SeleniumTesting.log.error('No se puede ingresar al aplicativo debido a error de credenciales:')
                    SeleniumTesting.log.error('Se muestra el siguiente mensaje de advertencia: {} '\
                                             .format(mensaje_error_de_credenciales))

                    resultado.mensaje_error = 'No fue posible ingresar a la plataforma OWA, se tiene error de credenciales: '\
                                              '{}'.format(mensaje_error_de_credenciales)

                    resultado.validacion_correcta = False

            except NoSuchElementException as e:
                resultado.mensaje_error = constantes_json.OUTPUT_EXITOSO_1_1
                resultado.validacion_correcta = True
                SeleniumTesting.log.info(resultado.mensaje_error)
            except InvalidSessionIdException as e:
                resultado.mensaje_error = 'No fue posible ingresar a la plataforma de Exchange OWA, favor de verificar '\
                                          'si se tiene conectividad por internet, error detallado : {}'.format(e)
                resultado.validacion_correcta = False
                SeleniumTesting.log.error(resultado.mensaje_error)
            except JavascriptException as e:
                # Se ingresa correctamente, debido a que no se encontro el mensaje de error de credenciales incorrectas
                resultado.mensaje_error = constantes_json.OUTPUT_EXITOSO_1_1
                resultado.validacion_correcta = True
                SeleniumTesting.log.info(resultado.mensaje_error)
            except WebDriverException as e:
                # Se ingresa correctamente, debido a que no se encontro el mensaje de error de credenciales incorrectas
                resultado.mensaje_error = constantes_json.OUTPUT_EXITOSO_1_1
                resultado.validacion_correcta = True
                SeleniumTesting.log.info(resultado.mensaje_error)

        # realiza la validacion de ingreso correcto de sesion
        # se verifica que no haya algun error que se presente en la plataforma
        # en caso contrario se obtiene el mensaje del error y se establecer en el 
        # objeto resultado
        
        if SeleniumTesting.verificar_error_plataforma(driver):
            resultado.mensaje_error = 'No fue posible ingresar a la sesion, se presenta '\
                'el siguiente mensaje de error en la plataforma: {}'.format(SeleniumTesting.txt_mensaje_error_encontrado_owa)
            resultado.validacion_correcta = False

        resultado.finalizar_tiempo_de_ejecucion()
        resultado.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_acceso_portal_owa = resultado

        return result_list

    # verifica si se encontro el elemento deseado mediante el id
    # retorna True si se encontro el elemento
    # en caso contrario retorna False
    @staticmethod
    def verificar_elemento_encontrado_por_id(driver, id):
        elemento_html = None

        try:
            elemento_html = driver.find_element_by_id(id)
            SeleniumTesting.log.info(
                'Se localiza el elemento con el id {} correctamente'.format(id))
            return True
        except NoSuchElementException as e:
            SeleniumTesting.log.error(
                'No se encontro el elemento con el id: {}'.format(id))
            return False


    # verifica si se encontro el elemento deseado mediante el xpath
    # retorna True si se encontro el elemento
    # en caso contrario retorna False
    @staticmethod
    def verificar_elemento_encontrado_por_xpath(driver, xpath):
        elemento_html = None

        try:
            elemento_html = driver.find_element_by_xpath(xpath)
            SeleniumTesting.log.info(
                'Se localiza el elemento mediante el xpath {} correctamente'.format(xpath))
            return True
        except NoSuchElementException as e:
            SeleniumTesting.log.error(
                'No se encontro el elemento mediante el xpath: {}'.format(xpath))
            return False


    @staticmethod
    def verificar_elemento_encontrado_por_clase_js(driver, clase):
        elementos_html = []

        elementos_html = driver.execute_script(
            "return document.getElementsByClassName('{}');".format(clase))

        if elementos_html is not None and len(elementos_html) >= 1:
            SeleniumTesting.log.info('Se encontraron elementos Html con la clase {}'.format(clase))
            return True
        else:
            SeleniumTesting.log.info('No se encontraron elementos Html con la clase {}'.format(clase))
            return False

    
    # verifica si en la plataforma existe algun error presente, las cuales se enlistan a continuacion y 
    # que se han descubierto hasta este momento:
    #
    #   1) elemento title HTML con leyenda "Error"
    #   2) En el body de la plataforma se se presente la leyenda 'NegotiateSecurityContext failed with for host'
    @staticmethod
    def verificar_error_plataforma(driver):
        existe_error = False
        leyenda_title = driver.title
        mensaje_error_localizado = ''

        if leyenda_title is None:
            leyenda_title = FormatUtils.CADENA_VACIA

        if 'Error' in leyenda_title:
            existe_error = True
           
            if SeleniumTesting.verificar_elemento_encontrado_por_id(driver, 'errMsg'):
                elemento_mensaje_error = driver.find_element_by_id('errMsg')
                mensaje_error_localizado = elemento_mensaje_error.get_attribute('innerHTML')
                existe_error = True

        elif SeleniumTesting.verificar_elemento_encontrado_por_xpath(driver,'//body'):

            elemento_body = driver.find_element_by_xpath('//body')
            mensaje_error_localizado = elemento_body.get_attribute('innerHTML')

            if mensaje_error_localizado is None:
                    mensaje_error_localizado = ''

            if 'NegotiateSecurityContext' in mensaje_error_localizado or \
                    'LogonDenied' in mensaje_error_localizado:
                    existe_error = True

        if existe_error:
            SeleniumTesting.log.error('Se localiza error dentro de la plataforma '\
                'owa: {}'.format(mensaje_error_localizado))
            SeleniumTesting.txt_mensaje_error_encontrado_owa = mensaje_error_localizado
            SeleniumTesting.mensaje_error_encontrado_owa = existe_error
        else:
            SeleniumTesting.log.info('No se localizo error alguno dentro de la plataforma owa')
        
        return existe_error
        

    # cuando se ingresa correctamen al OWA, se localizan las listas de folders
    # que contiene el usuario en sesion
    @staticmethod
    def obtener_carpetas_en_sesion(driver):
        lista_de_carpetas_localizadas = []
        lista_nombres_de_carpetas_formateadas = []
        clase_css_carpeta_owa_2016 = "_n_C4"
        clase_css_carpeta_owa_2013 = '_n_Z6'
        xpath_carpeta_owa_2010 = "//a[@name='lnkFldr']"
        se_encontraron_carpetas = False
        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        tiempo_de_finalizacion = 0

        while tiempo_de_finalizacion < 60:
            
            time.sleep(10)

            if SeleniumTesting.verificar_elemento_encontrado_por_clase_js(driver, clase_css_carpeta_owa_2016):
                SeleniumTesting.owa_descubierto = 2016
                se_encontraron_carpetas = True  
            elif SeleniumTesting.verificar_elemento_encontrado_por_clase_js(driver, clase_css_carpeta_owa_2013):
                SeleniumTesting.owa_descubierto = 2013
                se_encontraron_carpetas = True  
            elif SeleniumTesting.verificar_elemento_encontrado_por_xpath(driver, xpath_carpeta_owa_2010):
                SeleniumTesting.owa_descubierto = 2010
                se_encontraron_carpetas = True
            
            tiempo_de_finalizacion = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio

            if tiempo_de_finalizacion % 20 == 0:
                SeleniumTesting.navegar_a_sitio(SeleniumTesting.url_owa_exchange)
                driver.refresh()

            if se_encontraron_carpetas:
                SeleniumTesting.log.info('Se localizan con exito las carpetas dentro de la plataforma OWA, en un lapso aproximado'\
                    ' de {} seg'.format(FormatUtils.truncar_float_cadena(tiempo_de_finalizacion)))
                break
            else:
                SeleniumTesting.log.info('Fue imposible localizar las carpetas dentro de la plataforma OWA, se intentara nuevamente')
                SeleniumTesting.log.info('Titulo actual de la plataforma: {}'.format(driver.title))
                SeleniumTesting.log.info('URL actual de la plataforma: {}'.format(driver.current_url))
            

        if se_encontraron_carpetas == False:
            tiempo_de_finalizacion = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio
            SeleniumTesting.log.error('Han transcurrido mas de {} seg sin localizar'\
                ' las carpetas dentro de la plataforma OWA'.format(FormatUtils.truncar_float_cadena(tiempo_de_finalizacion)))
            SeleniumTesting.log.error('Title actual de la plataforma: {}'.format(driver.title))
            SeleniumTesting.log.error('Url actual de la plataforma: {}'.format(driver.current_url))
            
        else:
            SeleniumTesting.log.info('Plataforma OWA version {} identificada'.format(SeleniumTesting.owa_descubierto))
            time.sleep(4)
            if SeleniumTesting.owa_descubierto == 2010:
                lista_de_carpetas_localizadas = driver.find_elements_by_xpath(xpath_carpeta_owa_2010)
            elif SeleniumTesting.owa_descubierto == 2013:
                script_js = '''
                        var elementos = document.getElementsByClassName('_n_Z6');
                        return elementos;
                        '''
                lista_de_carpetas_localizadas = driver.execute_script(script_js)
            elif SeleniumTesting.owa_descubierto == 2016:
                script_js = '''
                        var elementos = document.getElementsByClassName('_n_C4');
                        return elementos;
                        '''
                lista_de_carpetas_localizadas = driver.execute_script(script_js)


        for carpeta in lista_de_carpetas_localizadas:
            
            if SeleniumTesting.owa_descubierto == 2010:
                nombre_de_carpeta = carpeta.text
            else:
                nombre_de_carpeta = FormatUtils.remover_backspaces(
                    carpeta.get_attribute('innerHTML'))
        
            SeleniumTesting.log.info('Se obtiene la carpeta: {}'.format(nombre_de_carpeta))
            lista_nombres_de_carpetas_formateadas.append(nombre_de_carpeta)

        return lista_nombres_de_carpetas_formateadas


    # ejecuta la navegacion de cada una de las carpetas que tiene la sesion de correo electronico
    # se establece como parametro el numero de segundos en que se estara ejecutando la navegacion
    # entre carpetas (lo estipulado con 2 min -> 120 s)
    @staticmethod
    def navegacion_de_carpetas_por_segundos(lista_carpetas, 
                                            driver, 
                                            result_list, 
                                            numero_de_segundos=120):
                                   
        result_navegacion_carpetas = Result()
        result_navegacion_carpetas.inicializar_tiempo_de_ejecucion()
        tiempo_por_verificar = numero_de_segundos + Temporizador.obtener_tiempo_timer()
        tiempo_de_inicio = Temporizador.obtener_tiempo_timer()
        segundos = 0

        # verifica se tenga al menos una carpeta
        if len(lista_carpetas) == 0:
            result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
            result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = 'No fue posible localizar las carpetas dentro de la sesi\u00f3n Exchange OWA'
            result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas
            SeleniumTesting.log.info('No se localizaron carpetas por navegar dentro de la sesion en la plataforma Exchange OWA')

            return result_list
        
        # verifica que no haya algun mensaje de error en la plataforma, en caso contrario
        # se muestra el mensaje de error que aparace en la plataforma dentro del result   
        elif SeleniumTesting.verificar_error_plataforma(driver):

            result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
            result_navegacion_carpetas.establecer_tiempo_de_ejecucion()
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = 'No fue posible realizar la navegacion entre carpetas, se presenta '\
                                                       'el siguiente error dentro de la plataforma: '\
                                                       '{}'.format(SeleniumTesting.txt_mensaje_error_encontrado_owa)            
            result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas

            return result_list


        while Temporizador.obtener_tiempo_timer() <= tiempo_por_verificar:
            for carpeta in lista_carpetas:
                segundos = Temporizador.obtener_tiempo_timer() - tiempo_de_inicio

                if segundos > numero_de_segundos:
                    SeleniumTesting.log.info(
                        'Ha transcurrido un lapso aproximado de 2 minutos, se procede a cerrar la sesion dentro de la plataforma OWA')
                    break

                SeleniumTesting.log.info(
                    'Ingresando a la carpeta: {}'.format(carpeta))

                try:

                    if SeleniumTesting.owa_descubierto == 2016:
                        script_click_carpeta = \
                        '''
                            var carpeta = document.querySelector("span._n_C4[title='{}']");
                            return carpeta;
                        '''.format(carpeta)

                        elemento_html_carpeta = driver.execute_script(script_click_carpeta)
                        elemento_html_carpeta.click()
                        time.sleep(6)
                    elif SeleniumTesting.owa_descubierto == 2010:
                        elemento_html_carpeta = driver.find_element_by_xpath('//a[@name="lnkFldr"][@title="{}"]'.format(carpeta))
                        time.sleep(3)
                        SeleniumTesting.verificar_dialogo_de_interrupcion(
                            driver, result_navegacion_carpetas)
                        time.sleep(3)
                        elemento_html_carpeta.click()
                    elif SeleniumTesting.owa_descubierto == 2013:
                        script_click_carpeta = \
                        '''
                            var carpeta = document.querySelector("span._n_Z6[title='{}']");
                            return carpeta;
                        '''.format(carpeta)

                        elemento_html_carpeta = driver.execute_script(script_click_carpeta)
                        elemento_html_carpeta.click()
                        time.sleep(6)

                except StaleElementReferenceException as e:
                    SeleniumTesting.log.error(
                        'Una de las carpetas no se localiza dentro del DOM de la plataforma OWA, se intentara ingresar nuevamente')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    
                    driver.refresh()
                    SeleniumTesting.log.error('Sucedio error al refrescar la plataforma OWA')
                    time.sleep(3)
                except ElementClickInterceptedException as e:
                    SeleniumTesting.log.error(
                        'No fue posible navegar a la carpeta seleccionada, se tiene un elemento HTML interfiriendo en la '\
                        'navegacion de la carpeta, se intentara ingresar nuevamente')
                    
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    
                    driver.refresh()
                    SeleniumTesting.log.error('Sucedio error al refrescar la plataforma OWA')
                    time.sleep(3)
                except NoSuchElementException as e:
                    SeleniumTesting.log.error(
                        'No fue posible localizar la carpeta por navegar dentro de la plataforma OWA, se intentara ingresar nuevamente')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))

                    driver.refresh()
                    SeleniumTesting.log.error('Sucedio error al refrescar la plataforma OWA')

                    time.sleep(3)
                except TimeoutException as e:
                    SeleniumTesting.log.error(
                        'Se presenta error de tiempo de carga en la plataforma OWA, se intentara actualizar la plataforma nuevamente')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    driver.refresh()
                    time.sleep(3)
                except WebDriverException as e:
                    SeleniumTesting.log.error(
                        'Se presenta error del webdriver para la navegacion web dentro de la plataforma OWA')
                    SeleniumTesting.log.error('error: {}'.format(e.msg))
                    time.sleep(3)

        result_navegacion_carpetas.finalizar_tiempo_de_ejecucion()
        result_navegacion_carpetas.establecer_tiempo_de_ejecucion()

        # verifica que no haya algun mensaje de error en la plataforma, en caso contrario
        # se muestra el mensaje de error que aparace en la plataforma dentro del result
        if SeleniumTesting.verificar_error_plataforma(driver):
            result_navegacion_carpetas.validacion_correcta = False
            result_navegacion_carpetas.mensaje_error = 'No fue posible realizar la navegacion entre carpetas, se presenta '\
                                                       'el siguiente error dentro de la plataforma: '\
                                                       '{}'.format(SeleniumTesting.txt_mensaje_error_encontrado_owa)
        else:
            result_navegacion_carpetas.validacion_correcta = True
            result_navegacion_carpetas.mensaje_error = constantes_json.OUTPUT_EXITOSO_2_1

        result_list.result_validacion_navegacion_carpetas = result_navegacion_carpetas
        
        return result_list

    # verifica que no aparezca el dialogo de interrupcion (dialogo informativo que en algunas ocasiones
    # aparece cuando se ingresa a una carpeta con correos nuevos)
    @staticmethod
    def verificar_dialogo_de_interrupcion(driver, result):
        if len(driver.find_elements_by_id('divPont')) > 0:
            SeleniumTesting.log.info(
                'Se ha encontrado un dialogo informativo, se procede a cerrarlo')

            try:
                time.sleep(4)
                boton_remover_dialogo = driver.find_element_by_id('imgX')
                boton_remover_dialogo.click()
            except ElementClickInterceptedException:
                SeleniumTesting.log.error(
                    'Se encontro un dialogo informativo pero fue imposible cerrarlo.')
                SeleniumTesting.log.error(
                    'Se intenta nuevamente el cierre del dialogo')
                SeleniumTesting.verificar_dialogo_de_interrupcion(
                    driver, result)

    # al usar el driver PhantomJS, las excepciones se muestran en un formato json,
    # la funcion detecta si la cadena de la excepcion es un json, de ser correcto,
    # intenta obtener solamente el mensaje general del error, ignorando las demas
    # propiedades que contengan el json
    @staticmethod
    def formatear_excepcion(ex):

        cadena_excepcion = str(ex)
        ex_json = None
        is_ex_json = False
        
        SeleniumTesting.log.info('Analizando el mensaje del error: {}'.format(cadena_excepcion))

        try:
            SeleniumTesting.log.info('Verificando si el error tiene el atributo msg')
            cadena_excepcion = ex.msg
            SeleniumTesting.log.info('Se obtiene el mensaje del atributo msg: {}'.format(cadena_excepcion))
        except AttributeError as e:
            SeleniumTesting.log.error('La excepcion no tiene el atributo msg'.format(e))

        try:
            SeleniumTesting.log.info('Verificando si el mensaje del error es un JSON')
            ex_json = json.loads(cadena_excepcion)
            SeleniumTesting.log.info('La excepcion es una estructura JSON')
            is_ex_json = True
        except ValueError as e:
            SeleniumTesting.log.info('La excepcion no es una estructura JSON: {}'.format(e))

        if is_ex_json:
            try:
                SeleniumTesting.log.info('Obteniendo el mensaje del error')
                cadena_excepcion = ex_json['errorMessage']
                SeleniumTesting.log.info('Mensaje de error obtenido: {}'.format(cadena_excepcion))
            except KeyError as e:
                SeleniumTesting.log.error('No se encontro el mensaje de error dentro del JSON')
        
        return cadena_excepcion


    # Cierra la sesion desde el aplicativo y termina la sesion en el webdriver
    @staticmethod
    def cerrar_sesion(driver, result_list):

        timeout_cierre_sesion = 10
        resultado_cierre_sesion = Result()
        resultado_cierre_sesion.inicializar_tiempo_de_ejecucion()
        url_actual = ''
        elemento_html_btn_cerrar_sesion = None
        cierre_sesion_exitosa = False
        title_cierre_sesion = "Outlook"

        try:
            driver.refresh()
            time.sleep(5)

            # verifica que no haya algun dialogo que impida el cierre de sesion
            SeleniumTesting.verificar_dialogo_de_interrupcion(
                driver, resultado_cierre_sesion)

            # intenta salir de la sesion ejecutando un script js
            # el cual simula un clic en el boton de cierre de sesion

            if SeleniumTesting.owa_descubierto == 2010:
                time.sleep(6)
                elemento_html_btn_cerrar_sesion = driver.find_element_by_id('lo')
                time.sleep(2)
                elemento_html_btn_cerrar_sesion.click()
                time.sleep(4)
            elif SeleniumTesting.owa_descubierto == 2016:
                time.sleep(4)
                boton_cierre_sesion_owa_2016 = driver.execute_script(\
                '''
                    var btn_cierre_sesion = document.querySelector('div.ms-Icon--person');
                    return btn_cierre_sesion;
                ''')

                time.sleep(4)
                boton_cierre_sesion_owa_2016.click()
                time.sleep(8)

                boton_cierre_sesion_owa_2016 = driver.execute_script(\
                '''
                    var btn_cierre_sesion = document.evaluate('//span[text()="Cerrar sesi\u00f3n"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    return btn_cierre_sesion;
                ''')

                boton_cierre_sesion_owa_2016.click()

            elif SeleniumTesting.owa_descubierto == 2013:

                boton_cierre_sesion_owa_2013 = driver.execute_script(\
                '''
                    var btn_cierre_sesion = document.querySelector('div._hl_d')
                    return btn_cierre_sesion;
                ''')

                boton_cierre_sesion_owa_2013.click()
                time.sleep(8)

                boton_cierre_sesion_owa_2013 = driver.execute_script(\
                '''
                    var btn_cierre_sesion = document.evaluate('//span[text()="Cerrar sesi\u00f3n"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    return btn_cierre_sesion;
                ''')

                if boton_cierre_sesion_owa_2013 is None:
                    SeleniumTesting.log.info('No se localiza el boton con el texto cierre de sesion, se intentara'\
                        ' localizar el boton con la leyenda \'Sign out\'')
                    
                    boton_cierre_sesion_owa_2013 = driver.execute_script(\
                    '''
                        var btn_cierre_sesion = document.evaluate('//span[text()="Sign out"]', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return btn_cierre_sesion;
                    ''')

                boton_cierre_sesion_owa_2013.click()
                

            # obtiene la url actual como una cadena
            time.sleep(2)
            url_actual = driver.current_url
            SeleniumTesting.log.info('Se cierra la sesion, obteniendo la siguiente url de cierre de sesion: {}'
                                     .format(url_actual))
            driver.refresh()
            SeleniumTesting.log.info("Se obtiene el siguiente titulo de la url actual: {}".format(driver.title))
            time.sleep(2)

            # verifica que nos encontremos en la pagina de cierre de sesion del OWA
            # verifica que el title de la pagina contenfa Outlook
            condicion_input_user_presente = EC.title_contains(title_cierre_sesion)
            WebDriverWait(driver, timeout_cierre_sesion).until(condicion_input_user_presente)
            cierre_sesion_exitosa = True

        except NoSuchElementException as e:

            SeleniumTesting.log.error('Error al salir de la sesion, no fue posible localizar el boton de cierre'\
                                      ' de sesion dentro de la plataforma del OWA')
            
            resultado_cierre_sesion.mensaje_error = 'Error al salir de la sesion, no fue posible localizar el boton de cierre de '\
                                                    'sesion dentro de la plataforma del OWA: {}'.format(SeleniumTesting.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        except ElementClickInterceptedException as e:
           
            SeleniumTesting.log.error('Error al salir de la sesion, no fue posible cerrar la sesion dentro '\
                                      'de la plataforma del OWA, se tiene un elemento HTML interfiriendo '\
                                      'el cierre de sesion')
            
            SeleniumTesting.log.error('Se intentara nuevamente el cierre de sesion')
            
            driver.refresh()
            time.sleep(2)
            SeleniumTesting.cerrar_sesion(driver, result_list)

        except TimeoutException as e:

            SeleniumTesting.log.error('Error al salir de la sesion, no fue posible cerrar la sesion dentro '\
                                      'de la plataforma del OWA, se presenta un error de tiempo de carga '\
                                      'dentro de la plataforma: {}'.format(SeleniumTesting.formatear_excepcion(e)))

            resultado_cierre_sesion.mensaje_error = 'Error al salir de la sesion, no fue posible cerrar la sesion dentro '\
                                      'de la plataforma del OWA, se presenta un error de tiempo de carga '\
                                      'dentro de la plataforma: {}'.format(SeleniumTesting.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        except WebDriverException as e:

            SeleniumTesting.log.error('Error al salir de la sesion, se presenta un error de comunicacion con '\
                                      'el webdriver de navegacion para la plataforma OWA: {}'\
                                      .format(SeleniumTesting.formatear_excepcion(e)))

            resultado_cierre_sesion.mensaje_error = 'Error al salir de la sesion, se presenta un error de comunicacion con '\
                                      'el webdriver de navegacion para la plataforma OWA: {}'\
                                      .format(SeleniumTesting.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        except AttributeError as e:

            SeleniumTesting.log.error('Error al salir de la sesion, no fue posible localizar el boton de cierre'\
                                      ' de sesion dentro de la plataforma del OWA')
            
            resultado_cierre_sesion.mensaje_error = 'Error al salir de la sesion, no fue posible localizar el boton de cierre de '\
                                                    'sesion dentro de la plataforma del OWA: {}'.format(SeleniumTesting.formatear_excepcion(e))

            resultado_cierre_sesion.validacion_correcta = False

        finally:

            # verifica que no haya algun mensaje de error en la plataforma, en caso contrario
            # se muestra el mensaje de error que aparace en la plataforma dentro del result
            if SeleniumTesting.verificar_error_plataforma(driver):
                resultado_cierre_sesion.validacion_correcta = False
                resultado_cierre_sesion.mensaje_error = 'No fue posible cerrar la sesion, se presenta '\
                                                        'el siguiente error dentro de la plataforma: '\
                                                        '{}'.format(SeleniumTesting.txt_mensaje_error_encontrado_owa)
                cierre_sesion_exitosa = False

            SeleniumTesting.log.info('Se procede a cerrar la sesion del WebDriver')
            driver.close()
            driver.quit()

        if cierre_sesion_exitosa:
            SeleniumTesting.log.info('Se cierra con exito la sesion dentro de la plataforma OWA')
            resultado_cierre_sesion.mensaje_error = constantes_json.OUTPUT_EXITOSO_3_1
            resultado_cierre_sesion.validacion_correcta = True

        resultado_cierre_sesion.finalizar_tiempo_de_ejecucion()
        resultado_cierre_sesion.establecer_tiempo_de_ejecucion()
        result_list.result_validacion_cierre_sesion = resultado_cierre_sesion

        return result_list
