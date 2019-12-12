#!/usr/bin/python
# encoding: utf-8
from bs4 import BeautifulSoup
import requests
import sys
import re

ip = sys.argv[1]
url = "http://" + ip + "/status_gen.html"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, features="lxml")
soup_result = soup.findAll('th')

for i in soup_result:
    if "Device Name" in i:
        text = i.nextSibling.nextSibling.text
        result = text.replace(" ", "").replace("\n", "")
        print(result)
