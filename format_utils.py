import constantes_json
import configparser
import logging
import json

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


    

    