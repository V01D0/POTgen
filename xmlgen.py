#!/usr/bin/python3

from xml.dom import minidom
import copy
import sys
import os
from pathlib import Path
from google.cloud import translate_v2 as translate
import mtranslate
import requests
from bs4 import BeautifulSoup
# import shutil
from tqdm import tqdm
import xml.etree.ElementTree as ET


file_name = sys.argv[1]
xml_file = minidom.parse(sys.argv[1])

strings = xml_file.getElementsByTagName('string')
original_texts = {}

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

# print(strings[0].getAttribute("name"))
# exit()

for string in strings:
	child_nodes = len(string.childNodes)
	name = string.attributes['name'].value
	# print(name)
	for i in range(child_nodes):
		original_texts.update({name: string.childNodes[i].data.replace("\\'", "'")})
		# print(string.childNodes[i].name)
		# original_texts.append(string.childNodes[i].data)

# print(original_texts)

api = True
try:
	TRANS = translate.Client()
except:
	api = False
	print("API not supported")

SOUP = BeautifulSoup(DATA, "html.parser")

skip = ['en', 'la', 'ceb', 'zh', 'he', 'mni-Mtei', 'fil', 'jv']

# print(len(SOUP.find_all('code')))

for lang in tqdm(SOUP.find_all('code')):
	# print(len(SOUP.find_all('code')))
	translated_texts = copy.deepcopy(original_texts)
	curlang = str(lang.getText())
	if curlang in skip:
		continue
	current_directory = os.getcwd()
	values_directory = os.path.join(current_directory, f"values-{curlang}")
	if not os.path.exists(values_directory):
		with open(file_name) as f:
			tree = ET.parse(f)
			root = tree.getroot()
			for k, v in translated_texts.items():
				if api:
					translated_string = TRANS.translate(
						v, source_language='en', target_language=curlang)
				else:
					translated_string = mtranslate.translate(v, curlang)
				translated_string = translated_string.replace("'", "\\'")
				translated_string = translated_string.replace("...", "…")
				for element in root.findall("string"):
					if element.text.replace("\\'", "'") == v:
						element.text = translated_string
			os.mkdir(values_directory)
			tree.write(f'{values_directory}/strings.xml', encoding='utf-8', xml_declaration=True)
	else:
		continue
