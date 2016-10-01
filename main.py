from webdata import MVGClient

station = "Haderner Stern"

with MVGClient(station=station, backend='phantomjs') as client:
    for arrival in client.arrivals:
        print(arrival)



