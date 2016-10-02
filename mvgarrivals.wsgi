#!mvv_venv/bin/python

activate_this = '/var/www/mvgarrivals/mvv_venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import sys
#sys.path.insert(0, "/var/www/mvgarrivals/")
sys.path.append("/var/www/mvgarrivals/")


from mvvdisplay import app
from mvvdisplay.scraper import MVGClient
import sys
import logging
from flask import json

logging.basicConfig(stream=sys.stderr)



default_station = 'Haderner Stern'

mvg_client = MVGClient(station=default_station)
mvg_client.connect()


@app.route('/')
@app.route('/<station>')
def show_arrivals(station=None):
    if station:
        mvg_client.station = station
    arrivals = mvg_client.arrivals

    return json.jsonify(arrivals)



application = app
application.secret_key = 'afdafdhqnewqiusdodufabfafdjq3w2134jkalkdfa'

