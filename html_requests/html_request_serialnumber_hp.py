#!/usr/bin/python
# encoding: utf-8
from bs4 import BeautifulSoup
import requests
import sys
import urllib3
urllib3.disable_warnings()

ip = sys.argv[1]
url = "https://" + ip + "/hp/device/DeviceInformation/View"
response = requests.get(url, verify=False)
soup = BeautifulSoup(response.text, features="lxml")
result = soup.find('p', {'id': 'DeviceSerialNumber'}).text
print(result)
