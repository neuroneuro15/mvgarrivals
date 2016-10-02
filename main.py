from mvvdisplay.scraper import MVGClient

with MVGClient(station='Haderner Stern') as client:
    for arrival in client.arrivals:
        print(arrival)
