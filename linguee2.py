# FR-EN translator using multiple methods

import sys
import os

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
try:
    import simplejson as json
except (ImportError):
    import json
from urllib.parse import quote
from bs4 import BeautifulSoup
import string
# from wiktionaryparser import WiktionaryParser
import requests

DICT_LANGUAGE = {"de": "German",
                 "en": "English",
                 "fr": "French",
                 "es": "Spanish",
                 "pt": "Portuguese",
                 "it": "Italian",
                 "ru": "Russian",
                 "ja": "Japanese",
                 "zh": "Chinese",
                 "pl": "Polish",
                 "nl": "Dutch",
                 "sv": "Swedish",
                 "da": "Danish",
                 "fi": "Finnish",
                 "el": "Greek",
                 "cs": "Czech",
                 "ro": "Romanian",
                 "hu": "Hungarian",
                 "sk": "Slovak",
                 "bg": "Bulgarian",
                 "sl": "Slovene",
                 "lt": "Lithuanian",
                 "lv": "Latvian",
                 "et": "Estonian",
                 "mt": "Maltese"
                 }

TYPES = {"noun": ["noun, masculine", "noun, neuter", "noun, feminine", "noun", 'noun,\xa0masculine', "noun,\xa0neuter",
                  "noun,\xa0feminine"],
         "adjective": ["adjective"],
         "verb": ["verb"]}


def linguee(word, from_l, to_l, type=None):
    #
    # crawl through linguee for a definition.
    # will create new functions for API calls to Collins, Oxford, Glosbed etc when I get API keys for them approved
    #
    # will rely on Glosbed as a secondary look-up service, with Collins next and Linguee as a last option.
    #
    word = word.lower()
    from_l = DICT_LANGUAGE[from_l].lower() if len(from_l) == 2 else from_l.lower()
    to_l = DICT_LANGUAGE[to_l].lower() if len(to_l) == 2 else to_l.lower()

    short_from = from_l if len(from_l) == 2 else list(DICT_LANGUAGE.keys())[
        list(DICT_LANGUAGE.values()).index(from_l.capitalize())]
    short_to = to_l if len(to_l) == 2 else list(DICT_LANGUAGE.keys())[
        list(DICT_LANGUAGE.values()).index(to_l.capitalize())]

    linguee_link = "http://www.linguee.com/{}-{}/search?source=auto&query={}".format(from_l, to_l, quote(word))
    page = urlopen(linguee_link)
    soup = BeautifulSoup(page, "lxml")

    definitions = list()

    def1 = soup.find_all('a', class_="dictLink featured")
    for element in def1:
        if bool(element.find_parent(class_='lemma_content')) * bool(element.find_parent(attrs={
                "data-source-lang": short_from.upper()})):
            if bool(type) and any(bool(element.parent.find(attrs={"title": t})) for t in TYPES[type]):
                definitions.append(element.get_text())
            elif not bool(type):
                definitions.append(element.get_text())

    def2 = soup.find_all('a', class_="dictLink")
    for element in def2:
        if bool(element.find_parent(class_='lemma_content')) * bool(element.find_parent(
                attrs={"data-source-lang": short_from.upper()})) * bool(element.find_parent(
                class_='translation_group')) * bool(element.find_parent(class_='exact')):
            if bool(type) and any(bool(element.parent.find(attrs={"title": t})) for t in TYPES[type]):
                definitions.append(element.get_text())
            elif not bool(type):
                definitions.append(element.get_text())
    directory = "dictionary"
    if not os.path.exists(directory):
        os.makedirs(directory)

    writepath = r"{}/{}.txt".format(directory, word)
    mode = 'a+' if os.path.exists(writepath) else 'w+'

    if definitions is not None:
        with open(writepath, mode) as file2:
            file2.write("{};TR-{}-{};{};\n".format(word, short_from, short_to, definitions))
            file2.close()
    else:
        definitions = "word not found"
    return definitions


if __name__ == "__main__":
    lang_from = "de"
    lang_to = "en"
    key = "Messwert"

    definitions1 = linguee(key, lang_from, lang_to, "noun")
    definitions2 = list()
    for definition in definitions1:
        print("{},{},{}".format(definition, lang_to, lang_from))
        definition_ = linguee(definition, lang_to, lang_from, "noun")
        definitions2.append(definition_)

    print(definitions2)
