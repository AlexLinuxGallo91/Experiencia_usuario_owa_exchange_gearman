from python3_gearman import GearmanWorker
import inicio
import sys

######################################################################################
##                         WORKER PYTHON GEARMAN UX OWA                             ##
##                                                                                  ##
##  Modulo/Worker en python el cual realiza el flujo/test de cada una de las plata- ##
##  formas del OWA Exchange 2010, 2013 y 2016.                                      ##
##                                                                                  ##
######################################################################################

# se define el worker, host y puerto al que estara a la escucha de cada peticion
# para realizar un nuevo Job
host = 'localhost'
puerto = '4730'
worker = GearmanWorker(['{}:{}'.format(host, puerto)])

# funcion encarga de comunicarse al modulo de experiencia de usuario OWA
# el cual como resultado se obtiene una cadena en formato JSON
def exchange_owa_2010(gearman_worker, gearman_job):
    response = inicio.main(cadena_json=gearman_job.data)
    return response
  
worker.register_task('exchange_owa_2010', exchange_owa_2010)
worker.work()

# Omitir estas lineas, solo se usan para testeo
# argumentos = sys.argv[1:]
# inicio.main(argumentos[0])
