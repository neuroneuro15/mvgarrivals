from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
from collections import namedtuple
from functools import partial
from os import path
import os

driver_path = path.join(path.dirname(__file__), 'drivers')
#driver_path = '/usr/local/


log_path = path.join(path.dirname(__file__), 'logs')

backends = {'chrome': partial(webdriver.Chrome, executable_path=path.join(driver_path, 'chromedriver_linux64')),
            'phantomjs': partial(webdriver.PhantomJS, executable_path=path.join(driver_path, 'phantomjs_linux64'), service_log_path=os.path.devnull),
            }

class MVGClient:

    timeout = 5


    def __init__(self, station, backend='phantomjs'):
        """
        Client that connects a selenium browser to the mvg-live.de web site and gets arrival data.
        :param station: str, station name (ex: 'Haderner Stern"
        :param backend: str, ['chrome', 'phantomjs_linux64']
        """


        self.browser = backends[backend]() if type(backend) == str else backend
        self._station = station



    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.close()
        self.browser.quit()

    @property
    def station(self):
        return self._station

    @station.setter
    def station(self, name):
        self._station = name
        self.connect(attempts=2)  # need to change the url to fill out the form, and run it twice for some reason.

    @property
    def url(self):
        fmt_str = "http://www.mvg-live.de/MvgLive/MvgLive.jsp#haltestelle={station}&gehweg=0&zeilen=7&ubahn=true&bus=true&tram=true&sbahn=false"
        return fmt_str.format(station=self._station)

    def connect(self, attempts=1):
        """Send the browser to the url"""

        for attempt in range(attempts):
            self.browser.get(self.url)


        try:
            WebDriverWait(self.browser, timeout=self.timeout).until(
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

        refresh_button = soup.find('div', attrs={'class': 'gwt-Hyperlink show_details'}).a
        refresh_div = self.browser.find_element_by_class_name('gwt-Hyperlink')
        refresh_div.click()

        arrival_table = soup.findAll('table', attrs={'class': 'content'})[1]


        arrivals = []
        for row in arrival_table.findAll('tr')[2:]:
            data = [col.text for col in row.findAll('td')]

            # images/size30/produkt/U-Bahn.gif
            # images/size30/produkt/Nachteule.gif
            traintype_img = row.find('td').img['src']
            traintype = 'ubahn' if 'U-Bahn' in traintype_img else 'bus'

            arrival = dict(dest=data[2], type=traintype, mins=int(data[4]))
            arrivals.append(arrival)


        return arrivals



if __name__ == '__main__':

    station = "Haderner Stern"

    with MVGClient(station='Haderner Stern') as client:
        arrivals = client.arrival_data
        print(arrivals)
