import constantes_json 
import json

# Clase el cual guarda cada uno estados de las pruebas que se realizaran en cada uno de los steps/orders 

class JsonPorEnviar:

    @staticmethod
    def establecerEstructuraPrincipalJson(correo, cuerpo_principal_json):
        raiz = {}
        raiz.update({'node':correo})
        raiz.update({'body':cuerpo_principal_json})

        return raiz

    @staticmethod
    def establecerRaizJson():
        raiz = {}
        raiz.update({"start":""})
        raiz.update({"end":""})
        raiz.update({"status":""})
        raiz.update({"time":0})
        raiz.update({"steps":[]})

        return raiz

    @staticmethod
    def generarNodoPadre(order, name='', status='', 
                         output=[], start="", end="", time=0):
        nodoPadre = {}
        nodoPadre.update({"order":order})
        nodoPadre.update({"name":name})
        nodoPadre.update({"status":status})
        nodoPadre.update({"output":output})
        nodoPadre.update({"start":start})
        nodoPadre.update({"end":end})
        nodoPadre.update({"time":0})
        
        return nodoPadre

    @staticmethod
    def generarNodoHijo(order, name='', status='', 
                         output=""):
        nodoHijo = {}
        nodoHijo.update({"order":order})
        nodoHijo.update({"name":name})
        nodoHijo.update({"status":status})
        nodoHijo.update({"output":output})
        
        return nodoHijo

    @staticmethod
    def generar_nuevo_template_json():
        # genera el nodo raiz
        json_a_enviar = JsonPorEnviar.establecerRaizJson()

        # establece las 3 evaluaciones principales
        json_a_enviar["steps"].append(JsonPorEnviar.generarNodoPadre(1))
        json_a_enviar["steps"].append(JsonPorEnviar.generarNodoPadre(2))
        json_a_enviar["steps"].append(JsonPorEnviar.generarNodoPadre(3))

        # establece cada uno los steps de cada evaluacion
        json_a_enviar["steps"][0]["output"] = [JsonPorEnviar.generarNodoHijo(1)]
        json_a_enviar["steps"][1]["output"] = [JsonPorEnviar.generarNodoHijo(1)]
        json_a_enviar["steps"][2]["output"] = [JsonPorEnviar.generarNodoHijo(1)]

        json_a_enviar["steps"][0]["name"] = constantes_json.PASO_1
        json_a_enviar["steps"][1]["name"] = constantes_json.PASO_2
        json_a_enviar["steps"][2]["name"] = constantes_json.PASO_3

        json_a_enviar["steps"][0]["output"][0]["name"] = constantes_json.PASO_1_1
        json_a_enviar["steps"][1]["output"][0]["name"] = constantes_json.PASO_2_1
        json_a_enviar["steps"][2]["output"][0]["name"] = constantes_json.PASO_3_1

        return json_a_enviar
