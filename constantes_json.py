import os.path
import datetime

# paths
PATH_BASE_PROYECTO = ''
NOMBRE_BASE_FILE_LOG = 'Log_Exchange_OWA'
PATH_ABSOLUTO_LOG = ''
DIR_BASE_LOG = ''
EXTENSION_FILE_LOG = '.log'
DEV_NULL = '/dev/null'
NOMBRE_ARCHIVO_CONFIG_INI = 'config.ini'
PATH_ARCHIVO_CONFIG_INI = ''

# bandera JSON invalido
JSON_INVALIDO = 'JsonInvalido'

# banderas para los estatus en cada validacion
STATUS_CORRECTO = 'SUCCESS'
STATUS_FALLIDO = 'FAILED'

# nombres de cada paso
PASO_1 = "Inicio de Sesi\u00f3n en OWA"
PASO_2 = "Navegaci\u00f3n entre carpetas"
PASO_3 = "Validaci\u00f3n de Cierre de Sesi\u00f3n en OWA"

# nombres de cada sub-paso
PASO_1_1 = "Inicio de sesi\u00f3n dentro del portal OWA"
PASO_2_1 = "Navegaci\u00f3n entre carpetas del correo electr\u00f3nico"
PASO_3_1 = "Cierre de sesi\u00f3n dentro del portal OWA"

# resultados finales/outputs exitosos
OUTPUT_EXITOSO_1_1 = "Se ingresa correctamente la sesi\u00f3n dentro del portal OWA"
OUTPUT_EXITOSO_2_1 = "Se navega exitosamente entre las carpetas del correo electr\u00f3nico"
OUTPUT_EXITOSO_3_1 = "Se cierra exitosamente la sesi\u00f3n dentro del portal OWA"

# resultados finales/outputs fallidos
OUTPUT_FALLIDO_1_1_ = "Se ingresa correctamente la sesi\u00f3n dentro del portal OWA"
OUTPUT_FALLIDO_2_1 = "Se navega exitosamente entre las carpetas del correo electr\u00f3nico"
OUTPUT_FALLIDO_3_1 = "Se cierra exitosamente la sesi\u00f3n dentro del portal OWA"

# Mensajes de validacion
VALDACION_CORRECTA_PASO_1_1 = "Se valid\u00f3 e ingreso exitosamente a la sesi\u00f3n"
VALDACION_CORRECTA_PASO_2_1 = "Se navega correctamente en las carpetas del correo electr\u00f3nico"
VALDACION_CORRECTA_PASO_3_1 = "Se cierra correctamente la sesi\u00f3n"

# establece todas las constantes al inicio del script
def configurar_paths_constantes(nombre_modulo):
    global PATH_BASE_PROYECTO
    global DIR_BASE_LOG
    global NOMBRE_ARCHIVO_CONFIG_INI
    global PATH_ARCHIVO_CONFIG_INI
    
    PATH_BASE_PROYECTO = os.path.dirname(os.path.abspath(nombre_modulo))
    DIR_BASE_LOG = os.path.join(PATH_BASE_PROYECTO, 'Logs')

    # se establece el path del archivo config.ini
    PATH_ARCHIVO_CONFIG_INI = os.path.join(PATH_BASE_PROYECTO, NOMBRE_ARCHIVO_CONFIG_INI)

