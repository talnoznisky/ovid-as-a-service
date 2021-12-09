import requests
import unicodedata
import re
import os 
import json

import spacy
from bs4 import BeautifulSoup

from spacy.language import Language

base_url = 'https://ovid.lib.virginia.edu/trans'
init_page = 'Metamorph.htm'
output_file = 'data/metamorphoses.json'

# init spacy
nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])


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
    soup = BeautifulSoup(html, features='lxml')

    return soup


def get_all_books(soup):
    links = soup.center.font.find_all('a')
    links = [a['href'] for a in links if 'Metamorph' in a['href']]

    return links 


def book_generator(book_counter, chapter_counter, line_counter, soup):
    elem = soup.find_all('h4')
    start = elem[0]
    book = []

    running = True
    while running:
        if start is None:
            running = False

        elif start.next_element.name == 'center' or start is None:
            running = False

        elif start.name == 'h4':
            chapter = normalize_text(start.get_text())
            chapter = re.sub("Bk.*(\d+)(?!.*\d)", '', chapter).strip()
            chapter_counter += 1
            start = start.find_next()      

        elif start.name == 'p' and len(start.text) > 0:
            if start != elem[0]:
                text = normalize_text(start.text)
                sents = list(nlp(text).sents)
                for sent in sents:
                    book.append({
                        'line': line_counter,
                        'book': book_counter,
                        'chapter': chapter_counter,
                        'chapter_name': chapter,
                        'text': str(sent)
                    })
                    line_counter += 1
            start = start.find_next()

        else:
            start = start.find_next()

    return book


def write_jsonl(data, output_path, append):
    mode = 'a+' if append else 'w'
    with open(output_path, mode, encoding='utf-8') as f:
        for line in data:
            json_record = json.dumps(line, ensure_ascii=False)
            f.write(json_record + '\n')


if __name__ == '__main__':
    init_url = make_url(base_url, init_page)
    init_soup = make_soup(init_url)

    links = get_all_books(init_soup)

    book_counter = 1
    chapter_counter = 0
    line_counter = 0

    for link in links:
        append = True if book_counter > 1 else False
        
        url = make_url(base_url, link)
        soup = make_soup(url)

        book = book_generator(book_counter, chapter_counter, line_counter, soup)
        write_jsonl(book, output_file, append)

        book_counter += 1
        line_counter += len(book)
