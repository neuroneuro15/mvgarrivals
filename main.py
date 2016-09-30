from webdata import MVGClient


station = "Haderner Stern"

with MVGClient(station=station) as client:
    print(client.arrivals)