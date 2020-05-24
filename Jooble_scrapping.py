import requests
from bs4 import BeautifulSoup
from time import sleep
import csv
import os

#URL = 'https://ua.jooble.org/%D1%80%D0%BE%D0%B1%D0%BE%D1%82%D0%B0-junior-python-developer/%D0%A5%D0%B0%D1%80%D0%BA%D1%96%D0%B2?date=2'
HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
FILE = 'jobs.csv'


# This way we get the html code from the link we want to be parsed
def get_html(URL, params=None):
    r = requests.get(URL, headers=HEADERS, params=params)
    r.encoding = 'utf8'
    return r


# This function gets the number of pages
def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('div', id='bl_bot').find_all('a')
    print(pagination)
    if pagination:
        return int(pagination[-1].get_text(strip=True))
    return 1


# This is how we got all the needed content from one page
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vacancy_wrapper')

    jobs = []
    for item in items:
        sleep(1)
        if item.find('span', class_='employer-widget_company'):
            company = item.find('span', class_='employer-widget_company').get_text(strip=True)
        else:
            company = 'It was not mentioned in the description. Should be clarified'

        jobs.append({
            'title': item.find('h2', class_='position').get_text(strip=True),
            'company': company,
            'link': item.find('a').get('href'),
            'city': item.find('span', class_='serp_location__region').get_text(strip=True),
        })

    return jobs


def save_file(items, path):
    with open(path, 'w', encoding='utf-8', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Job_Title', 'Employer', 'Link', 'City'])
        for job in items:
            writer.writerow([
                job['title'],
                job['company'],
                job['link'],
                job['city']
            ])


def parse():
    URL = input('Please, enter the valid link from Jooble with list of available positions: ')
    html = get_html(URL)
    if html.status_code == 200:
        print('Parsing of web-page has started')
        jobs = get_content(html.text)
        save_file(jobs, FILE)
        print('Parsing has been finished. The new site will be opened in a while.')
        os.startfile(FILE)
    return print(jobs)


parse()