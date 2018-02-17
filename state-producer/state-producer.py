from bs4 import BeautifulSoup
import requests
import random
import time
import json
import pika

BASE_URL = "https://www.chamberofcommerce.com"
QUEUE_HOSTNAME = 'queue'
QUEUE_NAME = 'states'
STORE_QUEUE_NAME = 'store'
CITY_QUEUE_NAME = 'cities'


def get_page_html(url):
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time - 1)
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def states():
    # Get all states
    soup = get_page_html("https://www.chamberofcommerce.com/business-directory")

    states_selector = "#content > div > div.main-content > div.big-section > div > div > div.box.visible.white-box > ul > li > h3 > a"

    states_soup = soup.select(states_selector)

    states = []
    for state in states_soup:
        state_dict = {'name': state.text, 'state_url': BASE_URL + state['href'], '_type': 'us-state'}
        states.append(state_dict)
        # print('PRODUCED STATE {}'.format(state_dict['name']))

    # print(states)

    return states


def get_top_cities_of_state(state):
    print("\n\nState\n{}\n".format(state))
    soup = get_page_html(state.get('state_url'))

    top_city_links = soup.select(".directory.white-box")
    if top_city_links:
        top_city_links = top_city_links[0].select('ul > li > a')

    def parse_text_and_href(link):
        return {'city': link.text, 'city_url': BASE_URL + link['href'], 'tags': ['top-state-city'],
                'state': state.get('name'), '_type': 'us-city'}

    return list(map(parse_text_and_href, top_city_links))


connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOSTNAME))
channel = connection.channel()

states = states()
for state in states:
    channel.basic_publish(exchange='', routing_key=STORE_QUEUE_NAME, body=json.dumps(state))
    for top_city in get_top_cities_of_state(state):
        ## Store the city
        channel.basic_publish(exchange='', routing_key=STORE_QUEUE_NAME, body=json.dumps(top_city))
        ## Queue the city for scraping
        channel.basic_publish(exchange='', routing_key=CITY_QUEUE_NAME, body=json.dumps(top_city))

connection.close()
