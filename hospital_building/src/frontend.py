from flask import Flask, request
from provider.db_provider import DbProvider
from reader.ReadMeteo import ReadMeteo
from poller.MeteoPoller import MeteoPoller
from store.DuplicateKeyException import DuplicateKeyException
from util.utillogs import UtilLogs
import logging
import json
import os
import time
 

app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

level = os.getenv("LOG_LEVEL", "DEBUG")

PYLOG_LEVEL = UtilLogs.pylog_level(level)
#ROSLOG_LEVEL = UtilLogs.roslog_level(level)
UtilLogs.ros_logger_format(__name__, level)
log = logging.getLogger(__name__)

@app.route("/area", methods=['POST'])
def area() :
    cod=200
    ret="OK" 

    item = request.json
    log.debug("Impostazione AREA %s" %item)
    msg="added area id " + item["id_area"]
   
    if item["id_area"] == None or item["latitude"] == None or item["longitude"] == None :
         cod=400
         msg="Nessun AREA,latitude,longitude impostata"
         return {"Errore" : msg}, cod 

    try :

        ret = DbProvider.storeArea(item)
        
    except Exception as e :
            cod=500
            log.debug("ERRORE AREA: %s" %e)  
            msg="Errore AREA impostata"
            return {"message": msg}, cod
                
    return {"message": msg} , cod

@app.route("/area/<id_area>", methods=['GET'])
def meteoArea(id_area) :
    cod=200

    log.debug("Ricerca meteo nell'area: %s" %id_area)

    try :
        
        citta = DbProvider.getDescrArea(id_area)
        log.debug("DOPO CITTA: %s" %citta)
        
        meteo = DbProvider.getMeteo(id_area)
        if meteo is None:
            meteo={}
        else:
             meteo["city"]=citta
             log.debug("METEO: %s" %meteo)

    except Exception as e :
            cod=500
            log.debug("Error GET MeteoArea: %s" %e) 
            msg = { "Errore" : str(e) }  
            return msg, cod

    return meteo, cod

@app.route("/meteocitta/<id_area>", methods=['POST'])
def creaMeteoArea(id_area) :
    cod=200
   
    log.debug("Creazione meteo nell'area: %s" %id_area)
    
    item = request.json
    
    if id_area == None :
         cod=400
         msg="Area non impostata"
         return {"Errore" : msg}, cod 
         
    msg, cod = ReadMeteo.sync_meteo(id_area)

    return {"message": msg}, cod

@app.route("/deletemeteo/<id_area>", methods=['GET'])
def deleteMeteoArea(id_area) :
    cod=200

    log.debug("Delete meteo nell'area: %s" %id_area)
    
    if id_area == None :
         cod=400
         msg="Area non impostata"
         return {"Errore" : msg}, cod 

    msg="delete meteo per area " + id_area

    try:
        area_cfg = DbProvider.getArea(id_area)

        if id_area == area_cfg :

            DbProvider.deleteMeteo(id_area)

        else:
            cod=500
            log.debug("Dati input mancanti MeteoArea") 
            msg = { "Dati input mancanti MeteoArea" }  
            return msg, cod

    except Exception as e :
            cod=500
            log.debug("Error Delete MeteoArea: %s" %e) 
            msg = { "Errore" : str(e) }  
            return msg, cod

    return {"message": msg}, cod

class Bundle:

    def __init__(self) -> None:
        self.poller = MeteoPoller()

    def start(self, ip_address=None, port=None):

        self.poller.start()
        app.run(host=ip_address, debug=False, port=port, use_reloader=False)

    def stop(self):
        self.poller.stop()

if __name__ == "__main__":
    # Only for debugging while developing
    app.run(host='0.0.0.0', debug=True, port=80)
