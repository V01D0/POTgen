#!/usr/bin/python3

"""
POTgen
This script generates .po files for a given .pot file
@author : V01D0
@copyright : https://pryv8.org
"""

from bs4 import BeautifulSoup
import re
from googletrans import Translator
import requests
import datetime
import fileinput
from langcodes import Language
from pathlib import Path

filename = Path("google.langs")
if filename.is_file():
    print("google.langs does exist... not downloading...")
    f2 = open(filename,"r+")
    data = f2.read()
    f2.close()
else:
    print("google.langs doesn't exist... downloading...")
    r = requests.get("https://cloud.google.com/translate/docs/languages")
    data = r.text
    f2 = open(filename, "wt")
    f2.write(data)
    f2.close()

soup = BeautifulSoup(data, "html.parser")

"""
Some general observation
* Really needs to get the header from the most recent POT file
* If POT POT-Creation-Date is later than the PO-Revision-Date this script
    needs to pull missing msgid's from pot file and merge in the po files
"""

head = """
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the geocaching.evilbunny package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: geocaching.evilbunny\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2020-05-24 12:19+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: 8bit\\n"
"Plural-Forms: nplurals=2; plural=n > 1;\n"
"""

for lang in soup.find_all('code'):
    curlang = str(lang.getText())
    if curlang == 'en':
        continue;

    heading = head
    filename = curlang+".po"
    f2 = open(filename,"wt")
    now = datetime.datetime.now(datetime.timezone.utc)
    date = str(now.year).zfill(4) + "-" + str(now.month).zfill(2) + "-" + str(now.day).zfill(2)
    date += " " + str(now.hour).zfill(2) + ":" + str(now.minute).zfill(2) + "+0000"
    language = Language.get(curlang).language_name('en')
    heading = heading.replace('SOME DESCRIPTIVE TITLE.', f"{language} translation for geocaching.evilbunny")
    heading = heading.replace('YEAR-MO-DA HO:MI+ZONE', date)
    heading = heading.replace('FULL NAME <EMAIL@ADDRESS>', f"Google Translate <{curlang}@li.org>")
    heading = heading.replace('LANGUAGE <LL@li.org>', f"LANGUAGE <{curlang}@li.org>")
    heading = heading.replace('Language: ', f"Language: {curlang}")
    heading = heading.replace('CHARSET', f"UTF-8")
    f2.write(heading)
    f2.close()
