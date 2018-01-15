import json

import itertools
from pathlib import Path

import requests
from bs4 import BeautifulSoup

wiki_base ="https://pl.wiktionary.org/wiki/"
col_r_meski = 0
col_r_zenski = 2
col_r_nijaki = 3
col_l_mnog = 4

def fetch_html_for_word(word: str):
    fetch_html(wiki_base + word)

def fetch_html(url: str):
    page = requests.get(url)
    filename = url.split('/')[-1] + ".html"
    with open('html/' + filename, 'wb') as f:
        f.write(page.text.encode('utf8'))

def load_html_file_for_word(word: str):
    with open('html/' + word + ".html", 'rb') as f:
        soup = BeautifulSoup(f, "lxml")
    return soup



def does_file_exist(word: str):
    filename = Path("html/" + word + ".html")
    return filename.is_file()

def get_html_for_word(word: str):
    if not does_file_exist(word):
        fetch_html_for_word(word)
    return load_html_file_for_word(word)

def init_lemko_word(word: str):
    return {word: {'deklinacja': {'meski': {'rowny': {}, 'wyzszy': {}, 'najwyzszy': {}},
                                  'zenski': {'rowny': {}, 'wyzszy': {}, 'najwyzszy': {}},
                                  'nijaki': {'rowny': {}, 'wyzszy': {}, 'najwyzszy': {}}
                                  }}}

def find_row_elements(przypadek, table):
    elements = []
    for td in table.find(title=przypadek).parent.parent.findAll('td')[1:]:
        if td.has_attr('colspan'):
            n = td['colspan']
            elements = list(itertools.chain(elements, [td.string] * int(n)))
        else:
            elements = list(itertools.chain(elements, [td.string]))
    return elements


def koniugacja_meski(table):
    return koniugacja_dla_rodzaju_num(col_r_meski, table)

def koniugacja_zenski(table):
    return koniugacja_dla_rodzaju_num(col_r_zenski, table)

def koniugacja_nijaki(table):
    return koniugacja_dla_rodzaju_num(col_r_nijaki, table)

def koniugacja_l_mnoga(table):
    return koniugacja_dla_rodzaju_num(col_l_mnog, table)

def koniugacja_dla_rodzaju_num(rodzaj: int, table):
    przypadki = ["mianownik", "dopełniacz", "celownik", "biernik", "narzędnik", "miejscownik", "wołacz"]
    conj = [find_row_elements(przypadki[i], table)[rodzaj] for i in range(0, 7)]
    return conj

def koniugacja_dla_rodzaju_str(rodzaj_str: str, table):
    rodzaje = {'meski': col_r_meski, 'zenski': col_r_zenski, 'nijaki': col_r_nijaki}
    return koniugacja_dla_rodzaju_num(rodzaje[rodzaj_str], table)

def do_next_word(word):
    soup = get_html_for_word(word)
    table = get_table_rowny(soup)
    table_wyzszy = get_table_wyzszy(soup)
    table_najwyzszy = get_table_najwyzszy(soup)

    lemko_word = init_lemko_word(word)
    lemko_word = do_conjugation(lemko_word, table, 'rowny')
    lemko_word = do_conjugation(lemko_word, table_wyzszy, 'wyzszy')
    lemko_word = do_conjugation(lemko_word, table_najwyzszy, 'najwyzszy')
    print(lemko_word)
    save_data_in_file(lemko_word)


def save_data_in_file(lemko_word):
    with open("data/polish_words.json", "r", encoding="utf8") as file:
        lemko_dict = json.load(file)
    lemko_dict.update(lemko_word)
    with open('data/polish_words.json', 'wb') as file:
        file.write(json.dumps(lemko_dict, indent=2, sort_keys=True, ensure_ascii=False).encode('utf8'))

def get_table_najwyzszy(soup):
    table = get_table_rowny(soup)
    return table.find_all('table')[1]

def get_table_wyzszy(soup):
    table = get_table_rowny(soup)
    return table.find_all('table')[0]

def get_table_rowny(soup):
    return get_table(soup)

def get_table(soup):
    html = soup.html
    table = html.find("table", attrs={"class": "odmiana"})
    return table

def do_conjugation(lemko_word, table, stopien):
    lemko_word = conjugation_step('meski', table, 0, stopien, lemko_word)
    lemko_word = conjugation_step('zenski', table, 0, stopien, lemko_word)
    lemko_word = conjugation_step('nijaki', table, 0, stopien, lemko_word)
    lemko_word = conjugation_step('meski', table, 1, stopien, lemko_word)
    return lemko_word

def conjugation_step(rodzaj_str: str, table, liczba, stopien, lemko_word):
    if liczba == 1:
        conj = koniugacja_l_mnoga(table)
    else:
        conj = koniugacja_dla_rodzaju_str(rodzaj_str, table)
    dict_conj = {liczba: dict(zip(range(0, 7), conj))}
    word = list(lemko_word.keys())[0]
    lemko_word[word]['deklinacja'][rodzaj_str][stopien].update(dict_conj)
    return lemko_word


word = "zielony"
# do_next_word(word)
# words = ["dąb", "stać", "koło", "droga"]
do_next_word(word)

# TODO
# obsługa czasownika i rzeczownika