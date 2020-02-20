import time
import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_target_urls(max_url=300):
    url = 'http://hk.racing.nextmedia.com/fullresult.php?date=20190123&page=01'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(r.text)
    options_text = str(soup.find_all('select')[0])
    # 為了確保沒有其他的網址被抓進來，多做一次確認
    date_urls_temp = re.findall('option value="(.*?)">', options_text)
    date_urls = [url for url in date_urls_temp if 'fullresult.php?date=' in url]

    all_target_urls = []
    for url in date_urls:
        r_date = requests.get('http://hk.racing.nextmedia.com/' + url)
        soup = BeautifulSoup(r_date.text, 'html.parser')
        urls_temp = [link.get('href') for link in soup.find_all('a')]
        all_target_urls += [u for u in urls_temp if 'fullresult.php?date' in u]
        print('已獲得{}個目標網址'.format(len(all_target_urls)))
        time.sleep(0.5)
        if len(all_target_urls) >= max_url:
            print('已獲得至少{}個目標網址'.format(max_url))
            return all_target_urls


def parse_url(url):
    url = 'http://hk.racing.nextmedia.com/' + url
    data = pd.read_html(url)

    game_id = re.findall('date=(.*?)&', url)[0] + '_' + re.findall('page=(.*?)$', url)[0]
    # 場地
    temp0 = data[1].iloc[1, 0]
    env = temp0.split('\xa0')[0:5] + re.findall("([A-Z]\d?)跑道", temp0) + re.findall("跑道評分\((.*?)\)",
                                                                                    temp0) + re.findall("場地:(.*?) ",
                                                                                                        temp0)
    env += re.findall("總場次:(\d+)", temp0) + re.findall("度地儀指數:.*?(\d+.\d+)", temp0)
    if re.findall("硬度計指數:.*?(\d+.\d+)", temp0):
        env += re.findall("硬度計指數:.*?(\d+.\d+)", temp0)
    else:
        env += ['缺值']
    env += re.findall("標準時間:.*?(\d+.\d+.\d+)", temp0)
    env.insert(0, game_id)

    # 比賽細節
    columns = ['馬號', '馬名', '歲', '騎師', '負磅', '檔', '評分', '廄', '馬匹體重',
               '賠率(隔夜)', '賠率(隔夜)', '賠率(隔夜)', '獨贏票(萬)', '位置票(萬)', '位置賠率',
               '走位', '名次', '分段時間', '總時間', '勝負距離']

    detail = data[2].iloc[2:-2, :].reset_index(drop=True)
    detail.columns = columns
    detail.insert(loc=0, column='game_id', value=[game_id] * len(detail))

    return env, detail


all_urls = get_target_urls()

envs = []
details = []
env_column = ["game_id", "場次", "班次", "跑道長度",
              "地形1", "地形2", "跑道", "跑道評分",
              "場地", "總場次", "度地儀指數", "硬度計指數",
              "標準時間"]

print('Start to parse data from {} urls:'.format(len(all_urls)))
n = 0
for url in all_urls:
    env, detail = parse_url(url)
    envs.append(env)
    details.append(detail)
    n += 1
    print('You have parsed data from {} urls!'.format(n))
    time.sleep(0.5)

env_data = pd.DataFrame(envs)
env_data.columns = env_column
env_data.to_excel('horse_gambling_env.xlsx', index=False)
pd.concat(details, axis=0).to_excel('horse_gambling.xlsx', index=False)

print('Congrates! All is well!!')