from temporizador import Temporizador
from format_utils import FormatUtils
import constantes_json

class Result:

    def __init__(self):
        self.validacion_correcta = False
        self.mensaje_error = ''
        self.tiempo_inicio_de_ejecucion = 0
        self.tiempo_fin_de_ejecucion = 0
        self.tiempo_total_de_la_ejecucion = 0
        self.datetime_inicial = ''
        self.datetime_final = ''

    def establecer_tiempo_de_ejecucion(self):
        tiempo_inicial = self.tiempo_inicio_de_ejecucion
        tiempo_final = self.tiempo_fin_de_ejecucion
        self.tiempo_total_de_la_ejecucion = tiempo_final - tiempo_inicial

    def inicializar_tiempo_de_ejecucion(self):
        self.datetime_inicial = Temporizador.obtener_fecha_tiempo_actual()
        self.tiempo_inicio_de_ejecucion = Temporizador.obtener_tiempo_timer()

    def finalizar_tiempo_de_ejecucion(self):
        self.datetime_final = Temporizador.obtener_fecha_tiempo_actual()
        self.tiempo_fin_de_ejecucion = Temporizador.obtener_tiempo_timer()
        self.establecer_tiempo_de_ejecucion()

    def __str__(self):
        cadena = ''
        cadena += 'validacion_correcta : {self.validacion_correcta}\n'.format(self=self)
        cadena += 'mensaje_error : {self.mensaje_error}\n'.format(self=self)
        cadena += 'tiempo_inicio_de_ejecucion : {self.tiempo_inicio_de_ejecucion}\n'.format(self=self)
        cadena += 'tiempo_fin_de_ejecucion : {self.tiempo_fin_de_ejecucion}\n'.format(self=self)
        cadena += 'tiempo_total_de_la_ejecucion : {self.tiempo_total_de_la_ejecucion}\n'.format(self=self)
        cadena += 'datetime_inicial : {self.datetime_inicial}\n'.format(self=self)
        cadena += 'datetime_final : {self.datetime_final}\n'.format(self=self)

        return cadena
    
class EvaluacionStepsJson:

    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_inicio_sesion(result_url, 
                                      result_sesion, 
                                      objeto_json):
        result_final = Result()

        # valida el estatus de ambos steps
        if result_url.validacion_correcta == False:
            result_final.mensaje_error = result_url.mensaje_error
            result_final.validacion_correcta = False
        elif result_sesion.validacion_correcta == False:
            result_final.mensaje_error = result_sesion.mensaje_error
            result_final.validacion_correcta = False
        else:
            result_final.mensaje_error = result_sesion.mensaje_error
            result_final.validacion_correcta = True
        
        # establece el datetime de inicio
        result_final.datetime_inicial = result_url.datetime_inicial

        # establece el datetime final
        result_final.datetime_final = result_sesion.datetime_final

        # establece el tiempo total de la ejecucion de ambos steps
        result_final.tiempo_inicio_de_ejecucion = result_url.tiempo_inicio_de_ejecucion
        result_final.tiempo_fin_de_ejecucion = result_sesion.tiempo_fin_de_ejecucion
        
        # establece el tiempo total de ejecucion
        result_final.establecer_tiempo_de_ejecucion()

        objeto_json['steps'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            result_final.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][0]['output'][0]['output'] = result_final.mensaje_error

        objeto_json['steps'][0]['output'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            result_final.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][0]['start'] = result_final.datetime_inicial
        objeto_json['steps'][0]['end'] = result_final.datetime_final
        objeto_json['steps'][0]['time'] = result_final.tiempo_total_de_la_ejecucion

        return objeto_json


    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_navegacion_carpetas(validacion_result, objeto_json):

        objeto_json['steps'][1]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][1]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][1]['output'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][1]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][1]['end'] = validacion_result.datetime_final
        objeto_json['steps'][1]['time'] = validacion_result.tiempo_total_de_la_ejecucion
        
        return objeto_json


    # validacion para verificar el inicio de sesion correctamente
    @staticmethod
    def validacion_json_cierre_sesion(validacion_result, objeto_json):

        objeto_json['steps'][2]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][2]['output'][0]['output'] = validacion_result.mensaje_error
        objeto_json['steps'][2]['output'][0]['status'] = constantes_json.STATUS_CORRECTO if \
            validacion_result.validacion_correcta else constantes_json.STATUS_FALLIDO

        objeto_json['steps'][2]['start'] = validacion_result.datetime_inicial
        objeto_json['steps'][2]['end'] = validacion_result.datetime_final
        objeto_json['steps'][2]['time'] = validacion_result.tiempo_total_de_la_ejecucion

        return objeto_json


    @staticmethod
    def establecer_fecha_tiempo_de_inicio(objeto_json):
        objeto_json['start'] = Temporizador.obtener_fecha_tiempo_actual()
        return objeto_json


    @staticmethod
    def establecer_tiempo_de_finalizacion(objeto_json):
        objeto_json['time'] = Temporizador.obtener_tiempo_timer()
        # objeto_json['status'] = constantes_json.STATUS_CORRECTO
        objeto_json['end'] = Temporizador.obtener_fecha_tiempo_actual()

        return objeto_json


    @staticmethod
    def formateo_de_tiempos(objeto_json):
        for i in range(3):
            objeto_json['steps'][i]['time'] = FormatUtils.truncar_float_cadena(objeto_json['steps'][i]['time'])

        objeto_json['time'] = FormatUtils.truncar_float_cadena(objeto_json['time'])

        return objeto_json


    @staticmethod
    def formar_cuerpo_json(result_list, objeto_json, correo):
        
        # se establece el tiempo final de ejecucion
        objeto_json = EvaluacionStepsJson.establecer_tiempo_de_finalizacion(objeto_json)

        # validaciones de cada step
        objeto_json = EvaluacionStepsJson.validacion_json_inicio_sesion(
            result_list.result_validacion_ingreso_url, 
            result_list.result_validacion_acceso_portal_owa,
            objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_navegacion_carpetas(
            result_list.result_validacion_navegacion_carpetas, objeto_json)

        objeto_json = EvaluacionStepsJson.validacion_json_cierre_sesion(
            result_list.result_validacion_cierre_sesion, objeto_json)

        tiempo_inicio_de_sesion = objeto_json['steps'][0]['time']
        tiempo_navegacion_carpetas = objeto_json['steps'][1]['time']
        tiempo_cierre_de_sesion = objeto_json['steps'][2]['time']

        suma_total_tiempo = tiempo_inicio_de_sesion + tiempo_navegacion_carpetas + \
                            tiempo_cierre_de_sesion

        objeto_json['time'] = suma_total_tiempo

        # Verifica si todos los estatus fueron exitosos o faliidos
        estatus_global =  objeto_json['steps'][0]['status'] and \
            objeto_json['steps'][1]['status'] and objeto_json['steps'][2]['status']

        objeto_json['status'] = estatus_global

        # Establece el correo concatenandolo en cada ouput en el objeto JSON
        objeto_json['steps'][0]['output'][0]['name'] += ' : {}'.format(correo.correo)
        objeto_json['steps'][1]['output'][0]['name'] += ' : {}'.format(correo.correo)
        objeto_json['steps'][2]['output'][0]['name'] += ' : {}'.format(correo.correo)

        # Formatea los tiempos a doce decimales (con el fin de no notificar con 
        # notacion cientifica)
        objeto_json = EvaluacionStepsJson.formateo_de_tiempos(objeto_json)

        return objeto_json


class ValidacionResultList:

    def __init__(self):
        self.result_tiempo_de_ejecucion = Result()
        
        # establece el tiempo de inicio de ejecucion
        self.result_validacion_ingreso_url = Result()
        self.result_validacion_acceso_portal_owa = Result()
        self.result_validacion_navegacion_carpetas = Result()
        self.result_validacion_cierre_sesion = Result()


    def __str__(self):
        v_url = 'validacion url: {}'.format(self.result_validacion_ingreso_url.validacion_correcta)
        
        v_portal_owa = 'validacion ingreso portal owa {}'.format(self.
                                            result_validacion_acceso_portal_owa.validacion_correcta)
        
        v_n_carpetas = 'validacion navegacion carpetas: {}'.format(self.
                                            result_validacion_navegacion_carpetas.validacion_correcta)

        v_cierre_sesion = 'validacion cierre sesion: {}'.format(self.result_validacion_cierre_sesion.
                                            validacion_correcta)

        return '{}\n{}\n{}\n{}\n'.format(v_url, v_portal_owa, v_n_carpetas, v_cierre_sesion)