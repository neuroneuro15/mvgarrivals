from webdata import MVGClient


station = "Haderner Stern"

with MVGClient(station=station, backend='phantomjs') as client:
    print(client.arrivals)