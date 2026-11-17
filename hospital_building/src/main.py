from flask import Flask, request
from provider.db_provider import DbProvider
from store.DuplicateKeyException import DuplicateKeyException
from util.utillogs import UtilLogs
import logging
import json
import os
from datetime import datetime


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

level = os.getenv("LOG_LEVEL", "DEBUG")

PYLOG_LEVEL = UtilLogs.pylog_level(level)
#ROSLOG_LEVEL = UtilLogs.roslog_level(level)
UtilLogs.ros_logger_format(__name__, level)
log = logging.getLogger(__name__)

@app.route("/area/<id>", methods=['GET'])
def areaId(id) :
    cod=200
    gpolig = []

    log.debug("Ricerca un Poligono dll'area: %s" %id)

    try :
        
        gpolig = DbProvider.getPoligonArea(id)

        if gpolig is not None:
            log.debug("Poligono : %s" %gpolig)
        else :
            msg = "POLIGONO NON TROVATO"
            gpolig = { "Errore" : msg } 

    except Exception as e :
            cod=500
            log.debug("Error PoligonArea: %s" %e) 
            gpolig = { "Errore" : str(e) }  
            return gpolig, cod

    return gpolig, cod


# Formatta data nel formato richiesto
def data_attuale_formattata():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")



# Precedente gestione dove l'area non era legata all'utente
@app.route("/area/modify", methods=['POST'])
def modify_area() :
    
    msg = "modify poligon area done"
    cod=200
    poligon=None
    
    log.debug("Modifica AREA da esterno")

    item = request.json
    log.debug("Modifica poligono AREA %s" %item)
   
    try :
        if item["name"] == None or item["geom"] == None or item["geom"]["coordinates"] == None :
            log.debug("Nessun AREA o Poligono da modificare") 
    except Exception as e :
            cod=400
            msg="Nessun AREA o Poligono da modificare"
            log.debug("Errore: Nessun AREA o Poligono da modificare", str(e)) 
            return {"Errore" : msg}, cod 
    
    id=item["name"]
    poligon = item["geom"]

    try :
            results = DbProvider.modifyArea(id, poligon)       
    except Exception as e :
            cod=500
            log.debug("Area modify Error: %s" %str(e))  
            return {"Error Area modify:": str(e)}, cod
    
    return {"message: ":msg}, cod




@app.route("/syncBuilding", methods=['POST'])
   
def syncBuilding() :

         msg = "Struttura inserita"
         cod=200
         poligon=None
         
         log.debug("Inserimento Struttura")
     
         item = request.json
         log.debug("Parametri struttura: %s" %item)
        
         try :
             if item["id"] == None :
                 log.debug("Nessuna struttura da inserire") 
         except Exception as e :
                 cod=400
                 msg="Nessuna struttura da inserire"
                 log.debug("Errore: Nessuna struttura da inserire", str(e)) 
                 return {"Errore" : msg}, cod 
         
         id=item["id"]

         obj = {
                "id_building" : id,
                "nome": "San Camillo",
                "tipologia": "ospedale/hub",
                "citta": "roma",
                "provincia": "RM",
                "piani":[
                            {
                            "piano": 0,
                            "stanze": [
                                {
                                "stanza1": [
                                    {
                                    "nome":"letto1", 
                                    "nomePoi": "letto1",
                                    "cfPaziente": "ksrrst34isnsn91q"
                                    }, 
                                    {
                                    "nome":"letto2", 
                                    "nomePoi": "letto2",
                                    "cfPaziente": ""
                                    } 
                                ]
                                },
                                {
                                "stanza2": [
                                    {
                                    "nome":"letto3", 
                                    "nomePoi": "letto3",
                                    "cfPaziente": "xsrrst34isnsn91q"
                                    }
                                ]
                                }
                            ]
                            }
                        ]
                }
     
         try :
                 results = DbProvider.syncBuilding(obj)       
         except Exception as e :
                 cod=500
                 log.debug("Struttura Error: %s" %str(e))  
                 return {"Error Struttura:": str(e)}, cod
         
         return cod, {"message: ":msg}
    
    
    


if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
