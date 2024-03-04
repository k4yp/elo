import pickle
import requests
from bs4 import BeautifulSoup

def scrape_climbers(start_page, end_page):
    for i in range(start_page, end_page + 1):
        with open('climbers.pkl', 'rb') as f:
            climbers = pickle.load(f)

        body = requests.get(f'https://www.thecrag.com/climbing/world/climbers/using-stat/boulder-rating/?page={i}')

        soup = BeautifulSoup(body.text, 'html.parser')
        climbers_class = soup.find_all('a', class_='grade-slider-user')

        for climber in climbers_class:
            climbers.append(climber['href'][9:])

        with open('climbers.pkl', 'wb') as f:
            pickle.dump(climbers, f)

        print(f'Scraped page {i}')

def scrape_climber(username):
    logbook = requests.get(f'https://www.thecrag.com/ascents/with-route-gear-style/boulder/by/{username}')
    pages =  BeautifulSoup(logbook.text, 'html.parser').find('div', class_='pagination')

    try:
        pages_num = len(pages.find_all('li')) - 2
    except:
        pages_num = 1

    for i in range(1, pages_num + 1):
        logbook_page = requests.get(f'https://www.thecrag.com/ascents/with-route-gear-style/boulder/by/{username}?page={i}')
        routes = BeautifulSoup(logbook_page.text, 'html.parser').find_all('tr', class_='actionable')

        for route in routes:
            route_id = route['data-nid']
            print(route_id)

# with open('climbers.pkl', 'wb') as f:
    # pickle.dump([], f)

# scrape_climbers(1,96)

with open('climbers.pkl', 'rb') as f:
    loaded_climbers = pickle.load(f)

for climber in loaded_climbers:
    scrape_climber(climber)