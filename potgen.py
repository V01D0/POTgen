"""
Binary Triangle
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

r = requests.get("https://cloud.google.com/translate/docs/languages")
data = r.text
soup = BeautifulSoup(data,"html.parser")

heading = """
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR THE PACKAGE'S COPYRIGHT HOLDER
# This file is distributed under the same license as the geocaching.evilbunny package.
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
#, fuzzy
msgid ""
msgstr ""
"Project-Id-Version: app.name\\n"
"Report-Msgid-Bugs-To: \\n"
"POT-Creation-Date: 2020-05-24 12:19+0000\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"Language: \\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=CHARSET\\n"
"Content-Transfer-Encoding: 8bit\\n"
"""

for lang in soup.find_all('code'):
    lang = str(lang.getText())
    filename = lang+".po"
    f2 = open(filename,"wt")
    now = datetime.datetime.now()
    date = str(now.year) + "-" + str(now.month) + "-" + str(now.day) + " " + str(now.hour) + ":" + str(now.minute) + "+0000"
    f2.write(heading)
    f2.close()
    f2 = open(filename,"r+")
    data = f2.read()
    data = data.replace('YEAR-MO-DA HO:MI+ZONE',date)
    data = data.replace('FULL NAME <EMAIL@ADDRESS>', f"Google Translate {lang}@li.org")
    data = data.replace('LANGUAGE <LL@li.org>', f"LANGUAGE <{lang}@li.org>")
    data = data.replace('Language: ', f"Language: {lang}")
    f2.write(data)
