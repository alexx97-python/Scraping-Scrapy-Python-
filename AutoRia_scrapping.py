import requests
from bs4 import BeautifulSoup
import csv
import os
from time import sleep

HEADERS = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
     'accept' : '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text(strip=True))
    return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')

    cars = []
    for item in items:
        sleep(1)
        price_ua = item.find('span', class_='grey size13')
        if price_ua:
            price_ua = price_ua.get_text(strip=True)
        else:
            price_ua = 'The price in this currency should be сlarified'
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'price': item.find('span', class_='green').get_text(strip=True),
            'price_ua': price_ua,
            'city': item.find('div', class_='proposition_region').get_text(strip=True),
            'additional_information': item.find('div', class_='proposition_information').get_text(strip=True),
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Model', 'Link', 'Price USD', 'Price UA', 'City', 'Additional information'])
        for item in items:
            writer.writerow([
                item['title'],
                item['link'],
                item['price'],
                item['price_ua'],
                item['city'],
                item['additional_information']
            ])


def parse():
    URL = input('Please, enter the valid link from AutoRia that should be parsed: ')
    URL = URL.strip()
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'The process of parsing {page} from {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        print(f'The parsing is finished. The number of items we got is {len(cars)}')
        print(cars)
        save_file(cars, FILE)
        os.startfile(FILE)
    else:
        print("Something is wrong!")


parse()
