from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import requests
import sys
import traceback
import xlsxwriter #要保留, 才能寫入xlsx
import os
import xlrd #讀取xlsx用

def get_url():
    headers = {
        'Accept': 'text/html',
        'User-Agent': 'Googlebot',
        'From': 'sonic760408@gmail.com'
    }

    r = requests.get('https://shop.greattree.com.tw/greattree/', headers=headers)
    # print(r)

    # print(type(r.text))
    # print(len(r.text))

    soup = BeautifulSoup(r.text, 'html.parser')

    # print(soup.title)

    '''
    for link in soup.find_all('a'):
        print(link.get('href'))
    '''

    # 找出所有商品分類連結
    # print(soup.find_all("div", class_="MENU"))

    '''
    print(soup.find("a", title="Special:Statistics").contents)
    '''
    #主分類
    aList = []
    titleList = []
    for link in soup.find_all("a", class_="title"):
        aList.append(link.get('href'))
        titleList.append(link.text)

    #子分類
    for link in soup.find_all("a", class_="title-2"):
        aList.append(link.get('href'))
        titleList.append(link.text)
    # print(*aList, sep='\n')
    return aList, titleList


def format_url(myurls, titleList):

    root_url = "https://shop.greattree.com.tw/greattree/"

    filter_urls = []
    remove_index = []

    for item in myurls:
        if " ../greattree/" in item:
            item = item.replace("../greattree/", "")
            item = root_url + item.strip()
        elif " /greattree/" in item:
            item = item.replace("/greattree/", "")
            item = root_url + item.strip()
        elif root_url not in item:
            item = root_url + item.strip()
        filter_urls.append(item.strip())

    for i in range(len(filter_urls)):
        if "https://shop.greattree.com.tw/greattree/index.php?action=product_sort" not in filter_urls[i]:
            #print("NOT FORMAT URL: {url}, index = {index}".format(url=filter_urls[i], index=i))
            remove_index.append(i)

    for i in range(len(remove_index) - 1, -1, -1): #負向迴圈, 包括0, 所以last index要設定-1(last index在for loop不包括)
        try:
            #print("WILL BE REMOVE URL: {url}, index = {index}".format(url=filter_urls[i], index=remove_index[i]))
            filter_urls.pop(remove_index[i])
            titleList.pop(remove_index[i])
        except IndexError:
            print("Index Out of Range")

    '''
    for item in filter_urls:
        if "https://shop.greattree.com.tw/greattree/index.php?action=product_sort" not in item:
            try:
                filter_urls.remove(item)
            except ValueError:
                print("filter_urls has no match string")
        else:
            print(item)
    '''
    for i in range(len(filter_urls)):
        print("Name: {name}, URL: {url}".format(name=titleList[i], url=filter_urls[i]))

    return filter_urls, titleList

#爬蟲
def getHtmlFromWeb(url):

    i = 0
    itemname = []
    itemprice = []
    #title = ''
    page = 1 #starting page
    headers = {
        'Accept': 'text/html',
        'User-Agent': 'Googlebot',
        'From': 'sonic760408@gmail.com'
    }

    while 1:
        #test_url = url + "&page=2"
        test_url = url + "&page="+str(page)
        print("url: {test_url}".format(test_url=test_url))
        r = requests.get(test_url, headers=headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        #title = soup.title
        items = soup.find_all('div', {'class': 'search-product-title'})

        #print(title.text)

        #取商品名
        for item in items:
            itemname.append(item.text)

        '''
        for item in items:
            if item.parent.name == 'price price_color':
                print('hello {name}, hello {text}'.format(name=name, text=text))
        '''

        #取商品價格(特價)
        items = soup.find_all('div', class_="price price_color")

        for item in items:
            #print(item.text.rstrip()) #清除換行符號
            #print(item.text.split('$'))

            try:
                price = item.text.split('$')[1]
            except Exception:
                price = None
            itemprice.append(price)

        #for item in itemprice:
        #    print('{item}'.format(item=item))

        '''
        print('itemname length: {itemname}, itemprice length: {itemprice}'\
              .format(itemname=len(itemname), itemprice=len(itemprice)))
        '''

        if len(itemname) != len(itemprice):
            print(" LEN ERROR, itemname:{itemname}, itemprice:{itemprice}"
                  .format(itemname=len(itemname),itemprice=len(itemprice)))
            return None, None, None

        #跳出機制
        #i = i + 1
        #if i == 1:
        #    break

        #找下一頁
        mynext = ''
        next = soup.find_all('li', {'class': 'next'})
        for Sub in next:
            if Sub.find("a") is None:
                mynext = None
                break
            else:
                try:
                    mynext = Sub.find("a").get('href')
                    #print("mynext: {mynext}".format(mynext=mynext))
                    break
                    #print(Sub.find("a").get('href'))
                except Exception as e:
                    mynext = None
                    break

        if mynext is None:
            break
        elif mynext == "javascript:void(0);":
            break
        else:
            page = page + 1

        #避免無窮迴圈
        if page > 50:
            break

        time.sleep(3)
    #end while

    return itemname, itemprice


def exportToXlsxFile_url(titles, urls):
    try:
        #print("Name: {name}, Price: {price}".format(name=itemname[i], price=itemprice[i]))

        #確認title格式 "[ ] : * ? / \"
        # 寫入到xlsx
        # Create a Pandas dataframe from some data.
        df = pd.DataFrame({'標題': titles, '網址': urls})

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('url.xlsx', engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name="網址", index=True)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    except Exception as e:
        #    print(e)
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        print("Exception in exportToXlsxFile_url: {errMsg}".format(errMsg=errMsg))


def exportToXlsxFile(title, itemname, itemprice, writer):
    try:
        print("分類: {title}".format(title=title))
        for i in range(len(itemname)):
            #print("Name: {name}, Price: {price}".format(name=itemname[i], price=itemprice[i]))

            #確認title格式 "[ ] : * ? / \"
            title  = title.replace("/", " ")
            # 寫入到xlsx
            # Create a Pandas dataframe from some data.
            df = pd.DataFrame({'品名': itemname, '價格': itemprice})

            # Create a Pandas Excel writer using XlsxWriter as the engine.
            #writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')

            # Convert the dataframe to an XlsxWriter Excel object.
            df.to_excel(writer, sheet_name=title, index=False)

            # Close the Pandas Excel writer and output the Excel file.
            #writer.save()

    except Exception as e:
        #    print(e)
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        print("Exception in exportToXlsxFile: {errMsg}".format(errMsg=errMsg))


def GetTenderData(start_date='108/1/1', end_date='108/12/31', keyword='高雄市政府', max_items=100):
    url = 'https://web.pcc.gov.tw/prkms/prms-searchBulletionClient.do?root=tps'

    data = {'tmpQuerySentence': None,
            'timeRange': f'{start_date}-{end_date}',
            'querySentence': f'{keyword}',
            'tenderStatusType': '決標',
            'sortCol': 'TENDER_NOTICE_DATE',
            'timeRangeTemp': f'{start_date}-{end_date}',
            'd-7095067-p': '1',
            'sym': 'on',
            'itemPerPage': f'{max_items}'}

    r = requests.post(url, data=data)

    patterns = [
        'style="width:18%;text-align:left">(.*?)</td>',
        '<div class="wordwrap">(.*?)</div>',
        '</a>[\s\S]*?width:9%;text-align:left;min-width:8%;">(.*?)</td>',
        '"width:15%;text-align:left;min-width:40px;">([\s\S]*?)</td>',
        'href="(.*?pkAtmMain.*?)"'
    ]

    agency_name = re.findall(patterns[0], r.text)
    project_name = re.findall(patterns[1], r.text)
    project_announce_date = re.findall(patterns[2], r.text)
    FF_date_t = re.findall(patterns[3], r.text)
    FF_date = [re.findall('\d\d\d\/\d\d\/\d\d', i)[0] for i in FF_date_t]
    Success = ['無法決標' not in i for i in FF_date_t]
    Detail_url = ['https://web.pcc.gov.tw' + u for u in re.findall(patterns[4], r.text)]

    col_names = ['機關名稱', '標案名稱', '標案公告日期', '決標或無法決標日期', '是否決標?', '標案網址']

    df = pd.DataFrame([agency_name, project_name, project_announce_date, FF_date, Success, Detail_url]).T
    df.columns = col_names
    df.to_excel('政府電子採購網資料.xlsx', index=False)


if __name__ == '__main__':

    urls = []
    titleList = []
    if os.path.isfile('url.xlsx'):
        dframe = pd.read_excel('url.xlsx')
        titleList = dframe['標題'].tolist()
        urls = dframe['網址'].tolist()
        #print(titleList)
        #print(urls)
    else:
        # 取得alits
        urls, titleList = get_url()
        time.sleep(3)
        # format_url
        urls, titleList = format_url(urls, titleList)

    #print("url len: {len}".format(len=len(urls)))

    i = 0
    for i in range(len(urls)):
        print("Name: {name}, URL: {url}".format(name=titleList[i], url=urls[i]))

    exportToXlsxFile_url(titleList, urls)

    #目前先用3筆url
    #urls = [urls[0], urls[1], urls[2]]
    #爬蟲

    i = 0
    #open excel writer
    try:
        writer = pd.ExcelWriter('result.xlsx', engine='xlsxwriter')

        # 取得一份web資料
        for i in range(len(urls)):
        #for i in range(20):
            itemname, itemprice = getHtmlFromWeb(urls[i])
            exportToXlsxFile(titleList[i], itemname, itemprice, writer)
            time.sleep(5)

        #close
        writer.save()
    except Exception as e:
        #print(e)
        error_class = e.__class__.__name__  # 取得錯誤類型
        detail = e.args[0]  # 取得詳細內容
        cl, exc, tb = sys.exc_info()  # 取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1]  # 取得Call Stack的最後一筆資料
        fileName = lastCallStack[0]  # 取得發生的檔案名稱
        lineNum = lastCallStack[1]  # 取得發生的行號
        funcName = lastCallStack[2]  # 取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        print("Exception in __main__: {errMsg}".format(errMsg=errMsg))

