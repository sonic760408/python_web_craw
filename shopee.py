import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

url = 'https://shopee.tw/search?keyword=PS4%20pro%20%E4%B8%BB%E6%A9%9F'
# 使用user-agent
headers = {
    'User-Agent': 'Googlebot',
    'From': 'sonic760408@gmail.com'
}

r = requests.get(url, headers=headers, allow_redirects=True)
print(r.status_code)
print(r.history)
print(r.url)

soup = BeautifulSoup(r.text, 'html.parser')
items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
print(len(items))

contents = soup.find_all("div", class_="_1NoI8_ _16BAGk")
prices = soup.find_all("span", class_="_341bF0")
all_items = soup.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")
links = [i.find('a').get('href') for i in all_items]

for c, p, l in zip(contents, prices, links):
    print(c.contents[0])
    print(p.contents[0])
    print('https://shopee.tw/'+l)
    print('*---------------------------------*')

