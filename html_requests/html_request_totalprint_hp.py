#!/usr/bin/python
# encoding: utf-8
from bs4 import BeautifulSoup
import requests
import sys
import urllib3
urllib3.disable_warnings()

ip = sys.argv[1]
url = "https://" + ip + "/hp/device/InternalPages/Index?id=UsagePage"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, features="lxml")
soup_result = soup.find('td', {'id': 'UsagePage.ImpressionsByMediaSizeTable.Print.A4.Total'}).text
result = soup_result.replace(",", "")
print(result)
