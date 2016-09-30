from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import bs4
from time import sleep
from contextlib import closing

station = "Haderner Stern"
chromedriver_path = './chromedriver_linux64'


url_fmt_str = "http://www.mvg-live.de/MvgLive/MvgLive.jsp#haltestelle={station}&gehweg=0&zeilen=7&ubahn=true&bus=true&tram=true&sbahn=false"
url = url_fmt_str.format(station=station)


def extract_arrival_data(soup):
    """
    Returns an arrival list of ("to_Station", minutes) from the bs4 soup 
    of www.mvg-live.de site.  
    Expects the data to already be present in the text.
    """
    arrivals = []
    tables = soup.findAll('table', attrs={'class': 'content'})

    for row in tables[1].findAll('tr')[2:]:
        data = [col.text for col in row.findAll('td')]
        arrivals.append([data[2], int(data[4])])

    return arrivals



with closing(webdriver.Chrome(executable_path=chromedriver_path)) as browser:
    browser.get(url)
    sleep(2)

    soup = bs4.BeautifulSoup(browser.page_source, 'lxml')

    arrivals = extract_arrival_data(soup=soup)
    print(arrivals)


