from python3_gearman import GearmanWorker
import inicio
import sys

######################################################################################
##                                                                                  ##
##                         WORKER PYTHON GEARMAN UX OWA                             ##
##                                                                                  ##
##  Modulo/Worker en python el cual realiza el flujo/test de cada una de las plata- ##
##  formas del OWA Exchange 2010, 2013 y 2016.                                      ##
##                                                                                  ##
##                                                                                  ##
##                                                                                  ##
######################################################################################

# se define el worker, host y puerto al que estara a la escucha de cada peticion
# para realizar un nuevo Job
host = '127.0.0.1'
puerto = '4773'
worker = GearmanWorker(['{}:{}'.format(host, puerto)])

# funcion encarga de comunicarse al modulo de experiencia de usuario OWA
# el cual como resultado se obtiene una cadena en formato JSON
def exchange_owa_2010(gearman_worker, gearman_job):
    print('generando test owa')
    response = inicio.main(cadena_json=gearman_job.data)
    print('finalizando test owa')
    return response

worker.register_task('exchange_owa_2010', exchange_owa_2010)
worker.work()

# # Omitir estas lineas, solo se usan para testeo
# argumentos = sys.argv[1:]
# resp = inicio.main(argumentos[0])
# print(resp)
