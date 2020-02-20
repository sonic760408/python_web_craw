import requests
import re
import pandas as pd


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

GetTenderData()