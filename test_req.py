# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

r = requests.get('https://en.wikipedia.org/')
print(r)
print('requests %s' % r)

print('requests type: %s' % type(r.text))
print('requests len: %s' % len(r.text))

soup = BeautifulSoup(r.text, 'html.parser')

print('title %s' % soup.title)

for link in soup.find_all('a'):
    print(link.get('href'))

print('div otd-footer %s' % soup.find_all("div", class_="otd-footer"))

print('Special:Statistics %s' % soup.find("a", title="Special:Statistics").contents)