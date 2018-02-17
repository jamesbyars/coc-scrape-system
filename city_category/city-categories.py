from bs4 import BeautifulSoup
import requests
import random
import time
import json
import pika

BASE_URL = "https://www.chamberofcommerce.com"
QUEUE_HOSTNAME = 'queue'
STORE_QUEUE_NAME = 'store'
CITY_QUEUE_NAME = 'cities'
CATEGORY_QUEUE_NAME = 'categories'

BUSINESS_DATA_TYPE = 'city-business-category'


def get_page_html(url):
    sleep_time = random.randint(1, 3)
    time.sleep(sleep_time - 1)
    page = requests.get(url)
    return BeautifulSoup(page.text, 'html.parser')


def categories_for_city(city):
    url = city['city_url'] + '/cats/2'
    print("Category URL: {}".format(url))
    soup = get_page_html(url)
    categories = soup.select("#content > div > div.main-content > div.directory.white-box > ul > li > a")
    cats = []
    for cat in categories:
        category_data = {"city_name": city['city'], 'city_category_url': BASE_URL + cat['href'], 'state': city['state'],
                         'category_title': cat.text, '_type': BUSINESS_DATA_TYPE}
        cats.append(category_data)

    return cats


connection = pika.BlockingConnection(pika.ConnectionParameters(QUEUE_HOSTNAME))
channel = connection.channel()


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

    data = json.loads(body)
    city_category = categories_for_city(data)

    for category in city_category:
        print('PRODUCED CITY CATEGORY {}'.format(category))
        channel.basic_publish(exchange='', routing_key=CATEGORY_QUEUE_NAME, body=json.dumps(category))
        channel.basic_publish(exchange='', routing_key=STORE_QUEUE_NAME, body=json.dumps(category))

    # connection.close()


channel.basic_consume(callback, queue=CITY_QUEUE_NAME, no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()
