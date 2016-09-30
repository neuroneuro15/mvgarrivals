from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
from collections import namedtuple


station = "Haderner Stern"
chromedriver_path = './drivers/chromedriver_linux64'

Arrival = namedtuple("Arrival", "dest type mins")

class MVGClient:

    def __init__(self, station):

        self.station = station

        url_fmt_str = "http://www.mvg-live.de/MvgLive/MvgLive.jsp#haltestelle={station}&gehweg=0&zeilen=7&ubahn=true&bus=true&tram=true&sbahn=false"
        self.url = url_fmt_str.format(station=station)
        self.browser = webdriver.Chrome(executable_path=chromedriver_path)


    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.browser.quit()

    def connect(self):
        """Send the browser to the url"""
        self.browser.get(self.url)

        try:
            WebDriverWait(self.browser, timeout=3).until(
                EC.presence_of_element_located((By.CLASS_NAME, "departureViewHaltestellenColumn"))
            )
        except TimeoutException:
            raise TimeoutError("Arrivals Table either not loaded in time, or not available at all.")

    @property
    def arrivals(self):
        """
            Returns an arrival list of ("to_Station", minutes) from the bs4 soup
            of www.mvg-live.de site.
            Expects the data to already be present in the text.
        """
        soup = bs4.BeautifulSoup(self.browser.page_source, 'lxml')

        arrivals = []
        tables = soup.findAll('table', attrs={'class': 'content'})

        for row in tables[1].findAll('tr')[2:]:
            data = [col.text for col in row.findAll('td')]

            # images/size30/produkt/U-Bahn.gif
            # images/size30/produkt/Nachteule.gif
            traintype_img = row.find('td').img['src']
            traintype = 'ubahn' if 'U-Bahn' in traintype_img else 'bus'

            arrival = Arrival(dest=data[2], type=traintype, mins=int(data[4]))
            arrivals.append(arrival)

        return arrivals



if __name__ == '__main__':

    with MVGClient(station='Haderner Stern') as client:
        arrivals = client.arrival_data
        print(arrivals)