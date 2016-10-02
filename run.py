from mvvdisplay import app
from mvvdisplay.scraper import MVGClient

from flask import json


default_station = 'Haderner Stern'

with MVGClient(station=default_station) as mvg_client:

    @app.route('/')
    @app.route('/<station>')
    def show_arrivals(station=None):
        if station:
            mvg_client.station = station
        arrivals = mvg_client.arrivals

        return json.jsonify(arrivals)


    if __name__ == '__main__':
        app.run()
