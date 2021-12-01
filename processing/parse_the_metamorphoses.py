from bs4 import BeautifulSoup
import requests
import unicodedata
import re
import os 
import json
import itertools


base_url = 'https://ovid.lib.virginia.edu/trans'
init_page = 'Metamorph.htm'
output_file = 'data/metamorphoses.json'


def normalize_text(text):
    text = re.sub("(\s+)",' ', text).strip()
    text = unicodedata.normalize('NFKD', text)

    return text
    

def make_url(base_url, page):
    url = os.path.join(base_url, page)

    return url


def make_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as err:
        print(err)    

    html = response.content
    soup = BeautifulSoup(html)

    return soup


def get_all_books(soup):
    links = soup.center.font.find_all('a')
    links = [a['href'] for a in links if 'Metamorph' in a['href']]

    return links 


def book_generator(counter, soup):
    elem = soup.find_all('h4')
    start = elem[0]

    book = []

    running = True
    while running:
        if start is None:
            running = False

        elif start.next_element.name == 'center' :
            running = False

        elif start.name == 'h4':
            chapter = normalize_text(start.text)
            chapter = re.sub("Bk.*(\d+)(?!.*\d)", '', chapter).strip()

            start = start.next_sibling        

        elif start.name == 'p':
            text = normalize_text(start.text)
            
            if start != elem[0]:
                book.append({
                    'book': counter,
                    'chapter': chapter,
                    'text': text
                })
                start = start.next_sibling

        else:
            start = start.next_sibling

    return book


if __name__ == '__main__':
    init_url = make_url(base_url, init_page)
    init_soup = make_soup(init_url)

    links = get_all_books(init_soup)

    books = []
    counter = 1
    for link in links:
        url = make_url(base_url, link)
        soup = make_soup(url)

        book = book_generator(counter, soup)
        books.append(book)
        counter += 1

    books = list(itertools.chain(*books))

    with open(output_file,'w+', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False)
