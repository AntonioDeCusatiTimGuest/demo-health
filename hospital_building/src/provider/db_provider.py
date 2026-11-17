from store.client import Client
from util.utillogs import UtilLogs
from store.DuplicateKeyException import DuplicateKeyException
import logging
import os



level = os.getenv("LOG_LEVEL", "DEBUG")

PYLOG_LEVEL = UtilLogs.pylog_level(level)
UtilLogs.ros_logger_format(__name__, level)
log = logging.getLogger(__name__)

db = Client()

class DbProvider :
  
   
   def syncBuilding(obj) :
        # db = Client()
        
        try :
            db.insert("Building",obj)
        except DuplicateKeyException as e :
            log.debug("Errore DB : %s"  %(e))
            return False

        return True
   
   def creaAntenna(obj) :
        # db = Client()
        
        try :
            db.insert("Antenna",obj)
        except DuplicateKeyException as e :
            log.debug("Errore DB : %s"  %(e))
            return False

        return True
   
   def creaArea(obj) :
        # db = Client()
        
        try :
            query = {    
                    'id': obj['id'],
                }
     
            res = db.find_one("Area", query)
        
            log.debug(res)

            if res is None:
                db.insert("Area",obj)
            else:
                log.debug("Area già presente!!")
        except DuplicateKeyException as e :
            log.debug("Errore DB : %s"  %(e))
            return False

        return True
     
   def modifyArea(id_area, poligon) :
        # db = Client()
        
        query = {
                    "id": id_area
                }
        update = {
                    "$set": {"poligon": poligon}
                }

        try :
            db.update_one("Area", query, update)
        except DuplicateKeyException as e :
            log.debug("Errore DB modify area: %s"  %str(e))
            return False

        return True
   

   @staticmethod
   def getPoligonArea(id_area) :

        # db = Client()
        log.debug("getArea DB: %s" %id_area)
        
        results = db.find("Area",
                            {
                            "id": id_area
                            }
                        )
        
        l=[] 
        if results is not None :
            for r in results :
                l.append({ "poligon" : r['poligon']}) 
                break

        return l
   
   @staticmethod
   def getArea(utente) :
        l=[] 
        msg=""
        # db = Client()
        log.debug("getArea DB: %s" %utente)
        
        # 1. Trova gli accessi attivi per l'utente
        query = {
                "nome": utente, 
                "user_attivo": True, 
                "ant_attiva": True
                }
        accessi = list(db.find("Accesso",
                           query
                        ))

        if len(accessi) == 0 :
            log.debug("Nessun accesso attivo.")
            msg="Nessun accesso attivo."
            return l, msg
        
        antenna_ids=[]

        if len(accessi) == 1 :
            antenna_ids.append(accessi[0]["antenna"]) 
        else :
            for a in accessi:
                antenna_ids.append(a["antenna"]) 

        if len(antenna_ids) == 0 :
            log.debug("Nessuna antenna attiva.")
            msg="Nessun antenna attiva trovata."
            return l, msg
        
        log.debug(f"Antenna IDs trovati: {antenna_ids}")

        area_ids=[]
        if len(antenna_ids) == 1 :
            antenna=antenna_ids[0]
       
            query = {"id": antenna}
            # 2. Trova le antenne corrispondenti
            antenne = db.find_one("Antenna",
                            query
                            )
            area_ids.append(antenne["areaId"]) 
        else :
            query = {"id": {"$in": antenna_ids}}
            # 2. Trova le antenne corrispondenti
            antenne = db.find("Antenna",
                            query
                            )
            
            for ant in antenne:
                area_ids.append(ant["areaId"]) 

        if len(area_ids) == 0:
            log.debug("Nessuna area trovata per le antenne.")
            msg="Nessuna area trovata per le antenne."
            return l, msg

        if len(area_ids) == 1 :
            area=area_ids[0]
            log.debug("Area: %s" %area)
            query={"id": area}

            # 3. Trova l' area corrispondente
            aree = db.find_one("Area",
                            query)
            
            if aree is not None :
                    l.append({ "area" : aree["id"], "active" : True}) 
        else :
            query={"id": {"$in": area_ids}}

            # 3. Trova le aree corrispondenti
            aree = db.find("Area",
                            query)
            
            if aree is not None :
                for r in aree :
                    l.append({ "area" : r["id"], "active" : True}) 
            
        return l, msg
   
   @staticmethod
   def getAllAree() :
        l=[] 
        msg=""
        # db = Client()
        log.debug("getAllAree DB")
        
        # 1. Trova gli accessi attivi
        query = {
                "user_attivo": True, 
                "ant_attiva": True
                }
        accessi = list(db.find("Accesso",
                           query
                        ))

        if len(accessi) == 0 :
            log.debug("Nessun accesso attivo.")
            msg="Nessun accesso attivo."
            return l, msg
        
        antenna_ids=[]

        if len(accessi) == 1 :
            antenna_ids.append((accessi[0]["antenna"], accessi[0]["ant_modello"])) 
        else :
            for a in accessi:
                antenna_ids.append([a["antenna"], a["ant_modello"]]) 

        if len(antenna_ids) == 0 :
            log.debug("Nessuna antenna attiva.")
            msg="Nessun antenna attiva trovata."
            return l, msg
        
        log.debug(f"Antenna IDs trovati: {antenna_ids}")

        area_ids=[]
        
        if len(antenna_ids) == 1 :
            antenna=antenna_ids[0][0]
            modello=antenna_ids[0][1]
       
            query = {"id": antenna}
            # 2. Trova le antenne corrispondenti
            antenne = db.find_one("Antenna",
                            query
                            )
            l.append({
                            "topics": antenne["id"],
                            "modello": modello,
                            "areaId": antenne["areaId"]
                        }) 
        else :
            query = {"id": {"$in": [ants[0] for ants in antenna_ids]}}
            projection = {"id": 1, "areaId": 1, "_id": 0}
            # 2. Trova le antenne corrispondenti
            antenne = db.find("Antenna",
                            query,
                            projection
                            )
            
            for ant in antenne:
                modello = next((ants[1] for ants in antenna_ids if ants[0] == ant["id"]), None)
                l.append({
                            "topics": ant["id"],
                            "modello": modello,
                            "areaId": ant["areaId"]
                        }) 
                

        if len(l) == 0:
            log.debug("Nessun topics/area trovato")
            msg="Nessun topics/area trovato"
            l.append({
                        "topics": "DroneDetection",
                        "areaId": None
                    }) 
            return l, msg
            
        return l, msg
   
   @staticmethod
   def getAreaAntenne(utente) :
        l=[] 
        msg=""
        # db = Client()
        log.debug("getArea DB: %s" %utente)
        
        # 1. Trova gli accessi attivi per l'utente
        query = {
                "email": utente, "active": True
                }
        accessi = db.find("Accesso",
                           query
                        )
        log.debug("DOPO prima FIND")
        antenna_ids=[]
        for a in accessi:
            antenna_ids.append(a['antenna']) 

        if not antenna_ids:
            log.debug("Nessun accesso attivo trovato.")
            msg="Nessun accesso attivo trovato."
            return l, msg
        
        log.debug(f"Antenna IDs trovati: {antenna_ids}")
        query = {"id": {"$in": antenna_ids}}
        projection = {"id": 1, "areaId": 1, "_id": 0}        
        # 2. Trova le antenne corrispondenti
        antenne = db.find("Antenna",
                          query,
                          projection
                        )
        antenne = list(antenne)
        log.debug(f"Antenne trovate: {antenne}")
        area_ids=[]
        for ant in antenne:
            area_ids.append(ant['areaId']) 

        if not area_ids:
            log.debug("Nessuna area trovata per le antenne.")
            msg="Nessuna area trovata per le antenne."
            return l, msg
        
        antenne_map = {ant1["id"]: ant1["areaId"] for ant1 in antenne}

        query={"id": {"$in": area_ids}}

        # 3. Trova le aree corrispondenti
        aree = db.find("Area",
                        query)
        
        if aree is not None :
            for antenna_id in antenna_ids:
                area_id = antenne_map.get(antenna_id)
                if area_id:  # solo se antenna trovata in Antenna
                    l.append({
                        "active": True,
                        "antenna": antenna_id,
                        "area": area_id
                    })

        return l, msg