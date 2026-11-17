from provider.db_provider import DbProvider
from reader.ReadMeteo import ReadMeteo
from util.utillogs import UtilLogs
import logging
import os

level = os.getenv("LOG_LEVEL", "DEBUG")
UtilLogs.ros_logger_format(__name__, level)
log = logging.getLogger(__name__)


def area(item):
    cod = 200
    ret = "OK"

    log.debug("Impostazione AREA %s" % item)
    msg = "added area id " + item["id_area"]

    if item["id_area"] == None or item["latitude"] == None or item["longitude"] == None:
        cod = 400
        msg = "Nessun AREA,latitude,longitude impostata"
        return {"Errore": msg}, cod

    try:
        ret = DbProvider.storeArea(item)

    except Exception as e:
        cod = 500
        log.debug("ERRORE AREA: %s" % e)
        msg = "Errore AREA impostata"
        return {"message": msg}, cod

    return {"message": msg}, cod


def meteoArea(id_area):
    cod = 200

    log.debug("Ricerca meteo nell'area: %s" % id_area)

    try:
        citta = DbProvider.getDescrArea(id_area)
        log.debug("DOPO CITTA: %s" % citta)

        meteo = DbProvider.getMeteo(id_area)
        if meteo is None:
            meteo = {}
        else:
            meteo["city"] = citta
            log.debug("METEO: %s" % meteo)

    except Exception as e:
        cod = 500
        log.debug("Error GET MeteoArea: %s" % e)
        msg = {"Errore": str(e)}
        return msg, cod

    return meteo, cod


def creaMeteoArea(id_area, item):
    cod = 200

    log.debug("Creazione meteo nell'area: %s" % id_area)

    if id_area == None:
        cod = 400
        msg = "Area non impostata"
        return {"Errore": msg}, cod

    msg, cod = ReadMeteo.sync_meteo(id_area)

    return {"message": msg}, cod


def deleteMeteoArea(id_area):
    cod = 200

    log.debug("Delete meteo nell'area: %s" % id_area)

    if id_area == None:
        cod = 400
        msg = "Area non impostata"
        return {"Errore": msg}, cod

    msg = "delete meteo per area " + id_area

    try:
        area_cfg = DbProvider.getArea(id_area)

        if id_area == area_cfg:
            DbProvider.deleteMeteo(id_area)

        else:
            cod = 500
            log.debug("Dati input mancanti MeteoArea")
            msg = {"Dati input mancanti MeteoArea"}
            return msg, cod

    except Exception as e:
        cod = 500
        log.debug("Error Delete MeteoArea: %s" % e)
        msg = {"Errore": str(e)}
        return msg, cod

    return {"message": msg}, cod
