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
    num_archivos_eliminados = 0
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

    # funcion encargada de truncar un decimal en caso de tener una notacion cientifica, en caso de ser asi
    # se trunca el decimal a un maximo de 12 decimales
    @staticmethod
    def truncar_float_cadena(cifra_decimal):
        num = cifra_decimal

        FormatUtils.log.info('formateando el valor {}'.format(cifra_decimal))
        if isinstance(cifra_decimal, str):
            try:
                num = float(cifra_decimal)
            except ValueError as e:
                num = 0
                FormatUtils.log.error('no es posible convertir {} a un valor decimal'.format(cifra_decimal))
        
        num = round(num, 12)
        num = '{:.12f}'.format(num)
        FormatUtils.log.info('resultado con formato: {}'.format(num))
        return num

    # funcion encargada de obtener el tamanio de un directorio (el resultado los da en MB)
    @staticmethod
    def obtener_tamanio_folder(master_path=''):
        tamanio_total = 0
        for dirpath, dirnames, filenames in os.walk(master_path):
            for f in filenames:
                try:
                    fp = os.path.join(dirpath, f)
                    tamanio_total += os.path.getsize(fp)
                except OSError as e:
                    continue
                    # FormatUtils.log.error('Sucedio un error al obtener '\
                    #                       'el peso del archivo {} : {}'.format(fp,e))                    
        
        # regresa el tamnanio del folder en MB
        return int(tamanio_total/(1024*1024))

    # funcion encargada de obtener una lista de paths absolutos en donde residen los archivos del 
    # directorio que se adjunta como argumento
    @staticmethod
    def obtener_lista_paths_archivos(master_path=''):
        list_files = []

        for dirpath, dirnames, filenames in os.walk(master_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                list_files.append(fp)
        
        # se obtienen los paths de los archivos dentro del folder Logs
        return list_files

    # funcion encargada de verificar si el archivo a eliminar sobrepasa la regla
    # de un cierto numero de horas, si rebasa el numero de horas establecido, el archivo
    # se elimina 
    @staticmethod
    def verificar_diferencia_fecha_archivo_eliminacion(horas=1, path_archivo=''):
        fecha_ahora = datetime.datetime.now()
        fecha_archivo = None
        diferencia_en_horas = 0
        num_archivos_eliminado = 0

        try:
            fecha_archivo = datetime.datetime.fromtimestamp(os.path.getmtime(path_archivo))
            diferencia_en_horas = fecha_ahora - fecha_archivo
            diferencia_en_horas = int(divmod(diferencia_en_horas.total_seconds(), 3600)[0])

            if(diferencia_en_horas > horas):
                os.remove(path_archivo)
                FormatUtils.num_archivos_eliminados += 1

        except OSError as e:
            # FormatUtils.log.error('Sucedio un error al intentar obtener la fecha de'\
            #     ' modificacion de archivo: {}'.format(e))
            return
        except TypeError as e:
            # FormatUtils.log.error('sucedio un error al intentar obtener la diferencia de fechas: {}'
            #     .format(e))
            return

    # es la funcion prinpal en donde comienza la depuracion del folder de logs,
    # solo se pasa como argumento el directorio base de los logs, para 
    # comenzar las verificaciones necesarias para la depuracion de los logs
    @staticmethod
    def verificacion_depuracion_de_logs(master_path=''):
        tamanio_folder = FormatUtils.obtener_tamanio_folder(master_path)
        list_archivos_paths = []

        if tamanio_folder >= 15:
            FormatUtils.log.info('El folder ya supero los 15MB, (peso actual de {}MB) se'\
                                 ' procede a depurar el folder'.format(tamanio_folder))
            list_archivos_paths = FormatUtils.obtener_lista_paths_archivos(master_path)
            for f in list_archivos_paths:
                FormatUtils.verificar_diferencia_fecha_archivo_eliminacion(1,f)
            FormatUtils.log.info('Numero de archivos eliminados: {}'.format(FormatUtils.num_archivos_eliminados))
        else:
            FormatUtils.log.info('El folder tiene un peso de {}MB, no es necesario depurar'
                                 .format(tamanio_folder))


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


    

    