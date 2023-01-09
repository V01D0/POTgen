from xml.dom import minidom
import copy
import sys
import os
from pathlib import Path
from google.cloud import translate_v2 as translate
import requests
from bs4 import BeautifulSoup
# import shutil
import xml.etree.ElementTree as ET


file_name = sys.argv[1]
xml_file  = minidom.parse(sys.argv[1])

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
	print(name)
	for i in range(child_nodes):
		original_texts.update({name:string.childNodes[i].data})
		# print(string.childNodes[i].name)
		# original_texts.append(string.childNodes[i].data)

# print(original_texts)

TRANS = translate.Client()
SOUP = BeautifulSoup(DATA, "html.parser")

for lang in SOUP.find_all('code'):
    translated_texts = copy.deepcopy(original_texts)
    curlang = str(lang.getText())
    if curlang == 'en' or curlang == 'la' or curlang == 'ceb':
        continue
    if curlang == 'zh-CN' or curlang == 'zh-TW':
        continue
    current_directory = os.getcwd()
    values_directory = os.path.join(current_directory, f"values-{curlang}")
    if not os.path.exists(values_directory):
        # print(values_directory)
        os.mkdir(values_directory)
        with open (file_name) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for k,v in translated_texts.items():
                translated_string = TRANS.translate(v,source_language='en',target_language=curlang)
                strings = xml_file.getElementsByTagName("strings")
                for elem in root.iter():
                    try:
                        elem.text = elem.text.replace(v, translated_string)
                    except AttributeError:
                        print("errrrrr")
            tree.write(f'{values_directory}/strings.xml', encoding='utf-8')
            # for k,v in translated_texts:
            #     translated_string = TRANS.translate(v,source_language='en',target_language=curlang)
            #     strings = xml_file.getElementsByTagName("strings")
            #     for string in strings:
            #         if string.getAttribute("name") == k:
            #             string.childNodes[0].data = translated_string
        # print(strings.getAttribute("name"))
