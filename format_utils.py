import datetime
import constantes_json
import configparser
import logging
import json
import string
import random
import os.path

class FormatUtils:

    CADENA_VACIA = ''
    BACKSPACE = '&nbsp;'
    ESPACIO = ' '
    log = logging.getLogger(__name__)

    # funcion encargada de leer las propiedades/secciones del archivo de configuracion config.ini
    @staticmethod
    def lector_archivo_ini():
        config = None

        try:
            config = configparser.ConfigParser()
            config.read(constantes_json.PATH_ARCHIVO_CONFIG_INI)
        except configparser.Error as e:
            FormatUtils.log.error('sucedio un error al leer el archivo de configuracion: {}'.format(e))
        
        return config
            

    # remueve los espacios en los textos de los elementos HTML
    @staticmethod
    def remover_backspaces(cadena):
        return cadena.replace(FormatUtils.BACKSPACE, FormatUtils.ESPACIO)


    # verifica que una cadena sea un formato valido JSON. En caso exitoso
    # la funcion devuelve True, en caso contrario False
    @staticmethod
    def cadena_a_json_valido(cadena=''):
        try:
            obj_json = json.loads(cadena)
            return True
        except ValueError as e:
            FormatUtils.log.error('El texto "{}" no es un objeto JSON valido: {}'.format(cadena, e.msg))
            return False

    @staticmethod
    def generar_nombre_log(correo_a_verificar):
        
        fecha = datetime.datetime.now()
        microsegundos_cadena = str(fecha.microsecond)
        microsegundos_cadena = microsegundos_cadena[:2]
        fecha_cadena = fecha.strftime('%Y_%m_%d_%H_%M_%S')
        fecha_cadena = '{}_{}'.format(fecha_cadena, microsegundos_cadena)

        abs_path_log = FormatUtils.CADENA_VACIA
        correo_formateado = FormatUtils.formatear_correo(correo_a_verificar)
        caracteres_aleatorios = FormatUtils.generar_caracteres_random()

        abs_path_log = '{}_{}_{}_{}{}'.format(
                        constantes_json.NOMBRE_BASE_FILE_LOG,
                        fecha_cadena,
                        caracteres_aleatorios, 
                        correo_formateado,
                        constantes_json.EXTENSION_FILE_LOG)
        
        abs_path_log = os.path.join(constantes_json.DIR_BASE_LOG ,abs_path_log)
        constantes_json.PATH_ABSOLUTO_LOG = abs_path_log

    @staticmethod
    def formatear_correo(correo):

        if correo is None:
            correo = ''
        else:
            correo = correo.strip()

        return correo.split('@')[0]

    @staticmethod
    def generar_caracteres_random():
        resultado = FormatUtils.CADENA_VACIA

        # establace los caracteres random
        cha1 = random.choice(string.ascii_letters)
        cha2 = random.choice(string.ascii_letters)
        cha3 = random.choice(string.ascii_letters)

        # establece los numeros random
        num1 = random.randint(0,9)
        num2 = random.randint(0,9)
        num3 = random.randint(0,9)

        list_caracteres = [cha1, cha2, cha3, num1, num2, num3]
        random.shuffle(list_caracteres)

        for caracter in list_caracteres:
            if isinstance(caracter, int):
                resultado += str(caracter)
            else:
                resultado += caracter

        return resultado


    

    