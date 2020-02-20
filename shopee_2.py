import time
import requests
import json


def shopeeAPI_Scraper(keyword, n_items):
    url1 = f'https://shopee.tw/api/v2/search_items/?by=relevancy&keyword={keyword}&limit={n_items}'
    headers = {'User-Agent': 'Googlebot', }
    r = requests.get(url1, headers=headers)
    api1_data = json.loads(r.text)

    for i in range(n_items):
        itemid = api1_data['items'][i]['itemid']
        shopid = api1_data['items'][i]['shopid']

        url2 = f'https://shopee.tw/api/v2/item/get?itemid={itemid}&shopid={shopid}'
        r = requests.get(url2, headers=headers)
        api2_data = json.loads(r.text)
        output = api1_data['items'][i]['name'].ljust(50) + ': ' + str(api2_data['item']['price'] / 100000)
        print(output)
        time.sleep(0.2)


shopeeAPI_Scraper(keyword='溜冰鞋', n_items=10)
