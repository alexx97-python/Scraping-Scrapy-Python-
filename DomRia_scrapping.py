import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import os

HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'}
HOST = 'https://dom.ria.com'


def get_html(URL, params=None):
    r = requests.get(URL, headers=HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='page-item mhide')
    if pagination:
        return int(pagination[-1].get_text(strip=True))
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('section', class_='ticket-clear')

    flats = []
    for item in items:
        #sleep(1)
        flats.append({
            'price_ua': item.find('b', class_='green size22').get_text(strip=True),
            'rooms': item.find('li', class_='mt-5 i-block').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'location': item.find('span', class_='tit_inner').get_text(strip=True),
        })
    return flats


def parse():
    URL = input('Please, input the valid link for DomRia to parse all flats: ')
    URL.strip()
    html = get_html(URL)

    if html.status_code == 200:
        flats = []
        pages = get_pages_count(html.text)
        for page in range(1, pages + 1):
            print(f'The process of parsing {page} from {pages}...')
            html = get_html(URL, params={'page': page})
            flats.extend(get_content(html.text))
        print(f'The parsing is finished. The number of items we got is {len(flats)}')
    print(flats)



parse()
