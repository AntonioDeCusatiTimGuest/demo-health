from flask import Flask, request
from poller.MeteoPoller import MeteoPoller
from util.utillogs import UtilLogs
import service
import logging
import os


app = Flask(__name__)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

level = os.getenv("LOG_LEVEL", "DEBUG")

PYLOG_LEVEL = UtilLogs.pylog_level(level)
#ROSLOG_LEVEL = UtilLogs.roslog_level(level)
UtilLogs.ros_logger_format(__name__, level)
log = logging.getLogger(__name__)

@app.route("/area", methods=['POST'])
def area():
    return service.area(request.json)

@app.route("/area/<id_area>", methods=['GET'])
def meteoArea(id_area):
    return service.meteoArea(id_area)

@app.route("/meteocitta/<id_area>", methods=['POST'])
def creaMeteoArea(id_area):
    return service.creaMeteoArea(id_area, request.json)

@app.route("/deletemeteo/<id_area>", methods=['GET'])
def deleteMeteoArea(id_area):
    return service.deleteMeteoArea(id_area)

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
