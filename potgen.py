#!/usr/bin/python3

"""
POTgen
This script generates .po files for a given .pot file
@author : V01D0
@copyright : https://pryv8.org
"""

import sys
import datetime
from pathlib import Path
from langcodes import Language
from googletrans import Translator
import requests
import polib
from bs4 import BeautifulSoup

if len(sys.argv) <= 1:
    print(f"POT file doesn't exist, can't continue...")
    sys.exit()

POT_FILE = Path(sys.argv[1])

if POT_FILE.is_file() is not False:
    POT_DATA = polib.pofile(POT_FILE)
else:
    print(f"POT file {POT_FILE} doesn't exist, can't continue...")
    sys.exit()

NOW = datetime.datetime.now(datetime.timezone.utc)
DATE = str(NOW.year).zfill(4) + "-" + str(NOW.month).zfill(2) + "-" + str(NOW.day).zfill(2)
DATE += " " + str(NOW.hour).zfill(2) + ":" + str(NOW.minute).zfill(2) + "+0000"

POT_DATA.metadata['Report-Msgid-Bugs-To'] = '<https://github.com/evilbunny2008/geocaching/issues>'
POT_DATA.metadata['Last-Translator'] = '<https://github.com/evilbunny2008/geocaching/issues>'
POT_DATA.metadata['PO-Revision-Date'] = DATE
POT_DATA.metadata['Content-Type'] = 'text/plain; charset=UTF-8'
POT_DATA.metadata['Plural-Forms'] = 'nplurals=2; plural=n > 1;'

FILENAME = Path("google.langs.html")
if FILENAME.is_file():
    F2 = open(FILENAME, "r")
    DATA = F2.read()
    F2.close()
else:
    print("google.langs doesn't exist... downloading...")
    R = requests.get("https://cloud.google.com/translate/docs/languages")
    DATA = R.text
    F2 = open(FILENAME, "wt")
    F2.write(DATA)
    F2.close()

TRANS = Translator()

SOUP = BeautifulSoup(DATA, "html.parser")

for lang in SOUP.find_all('code'):
    curlang = str(lang.getText())
    if curlang == 'en' or curlang == 'la':
        continue

    filename = Path(curlang + ".po")
    if filename.is_file():
        print(filename, " already exists, skipping...")
        continue

    language = Language.get(curlang).language_name('en')

    POT_DATA.metadata['Language-Team'] = language + ' <' + curlang + '@li.org>'
    POT_DATA.metadata['Language'] = curlang
    print("Generating " + curlang + ".po")

    for i in range(len(POT_DATA)):
        tmpstr = POT_DATA[i].msgid.replace('%1', '__')
        POT_DATA[i].msgstr = TRANS.translate(tmpstr, dest=curlang, src='en').text
        POT_DATA[i].msgstr = POT_DATA[i].msgstr.replace('__', '%1')

    F2 = open(filename, 'wt')
    F2.write(str(POT_DATA))
    F2.close()
