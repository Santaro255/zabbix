#!/usr/bin/python
# encoding: utf-8
from bs4 import BeautifulSoup
import requests
import sys
import re

ip = sys.argv[1]
url = "http://" + ip + "/machine_status.html"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, features="lxml")
soup_result = soup.findAll('h2')

for i in soup_result:
    if "Total Counts" in i:
        text = i.text
        result = re.findall('\d+', text)
        print(result[0])
