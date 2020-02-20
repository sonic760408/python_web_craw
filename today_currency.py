import pandas
import openpyxl
from bs4 import BeautifulSoup

url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'
dfs = pandas.read_html(url)
currency = dfs[0]
currency = currency.iloc[:, 0:5]

currency.columns = ['幣別', u'現金匯率-本行買入', u'現金匯率-本行賣出', u'即期匯率-本行買入', u'即期匯率-本行買入']
currency[u'幣別'] = currency[u'幣別'].str.extract('\((\w+)\)')

print(currency)
type(currency)
currency.to_excel(r'currency.xlsx')


