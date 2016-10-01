from webdata import MVGClient


# station = "Haderner Stern"
stations = ["Haderner Stern", "Sendlinger Tor", "Laimer Platz"]


with MVGClient(station=stations[2], backend='chrome') as client:

    for station in stations:
        client.station = station

        print("\nArrivals at Station {}".format(station))
        for arrival in client.arrivals:
            print(arrival)



