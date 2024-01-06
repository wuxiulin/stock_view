# -*- coding: utf-8 -*-
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import time
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning


# ====================开盘啦风口概念====================================================================================================================
def fengkoulSpider(flag, engine, *args):
    print("开始抓取龙虎榜风口概念")
    url = 'https://pclhb.kaipanla.com/w1/api/index.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    # 空DataFrame定义，用于存储：风口概念；空list定义，分别用于存储：股票代码
    tuyere = pd.DataFrame();
    code_list = []
    date_list = []

    # 实例化session，维持会话
    session = requests.Session()
    # 禁用安全请求警告
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    if flag == "Y":
        print("开始抓取当前开盘啦龙虎榜风口概念数据")
        cur_date = str(current)
        date_list.append(cur_date)

    elif flag == "N":
        print("开始抓取历史开盘啦龙虎榜风口概念数据")
        st = datetime.datetime.strptime(start, '%Y-%m-%d')
        ed = datetime.datetime.strptime(end, '%Y-%m-%d')
        for i in range((ed - st).days + 1):
            cur_date = st + datetime.timedelta(days=i)
            date_list.append(cur_date)

    # 构造URL请求表单，用于获取开盘啦当天龙虎榜列表，暂时忽略参数：'Index': 0
    data = {'c': 'LongHuBang', 'a': 'GetStockList', 'st': 300, 'Time': cur_date, 'UserID': 399083, 'Token': '71aef0e806e61ad3169ddc9473e37886'}

    # 模拟发送post请求，并实现json格式数据转换
    html_list = json.loads(session.post(url=url, headers=headers, data=data).text)['list']

    # 开始解析龙虎榜列表数据
    for html in html_list:
        code = html['ID']
        fengkou = html['FengKou']
        # 存储解析完成的code、fengkou
        code_list.append(code)
        tuyere = tuyere.append({'code': code, 'trade_date': cur_date, 'fengkou': fengkou}, ignore_index=True)

    print("开盘啦龙虎榜风口概念数据解析完成")
    print("开始存储开盘啦龙虎榜风口概念数据")
    exist_tuyere = pd.read_sql('select * from inst_tuyere_concept', engine)
    tuyere = tuyere[['code', 'trade_date', 'fengkou']]
    tuyere = tuyere.append(exist_tuyere, ignore_index=True, sort=False)
    tuyere.drop_duplicates(keep=False, inplace=True)
    tuyere.to_sql('inst_tuyere_concept', engine, if_exists='append', index=False, chunksize=10000)

    print(tuyere)
    print("本次存储开盘啦龙虎榜风口概念数据%s条" % tuyere.shape[0])
    print("开盘啦龙虎榜风口概念数据存储完成")
    print("---------------------------------")

    return date_list, code_list


def tagSpider(engine, date_list, code_list):
    print("开始抓取开盘啦龙虎榜营业部标签数据")
    url = 'https://pclhb.kaipanla.com/w1/api/index.php'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3314.0 Safari/537.36 SE 2.X MetaSr 1.0'}

    # 空DataFrame定义，用于存储：营业部标签
    depart_tag = pd.DataFrame()

    # 实例化session，维持会话
    session = requests.Session()
    print(date_list)
    print(code_list)
    for cur_date in date_list:

        for code in code_list:
            print("正在抓取%s-%s龙虎榜营业部明细数据" % (cur_date, code))
            # 构造URL请求表单，用于获取单只个股龙虎榜明细数据
            data = {'c': 'Stock', 'a': 'GetNewOneStockInfo', 'StockID': code, 'Time': date_list, 'UserID': '399083', 'Token': '71aef0e806e61ad3169ddc9473e37886'}

            # 模拟发送post请求，并实现json格式数据转换
            html_list = json.loads(session.post(url=url, headers=headers, data=data).text)['List'][0]

            # 开始解析
            buy_list = html_list['BuyList']
            sell_list = html_list['SellList']
            for sell in sell_list:
                buy_list.append(sell)

            # 由于部分营业部无标签，执行报错，此处采用try...except结构
            for depart in buy_list:
                try:
                    tag = depart['GroupIcon'][0]
                    yybname = depart['Name']
                    depart_tag = depart_tag.append({'yybname': yybname, 'tag': tag}, ignore_index=True)
                except Exception as parse_error:
                    print("html解析过程报错，错误信息为：%s" % parse_error)

    print("正在存储%s龙虎榜营业部明细数据" % cur_date)
    # 连接获取sql存储数据，求差集
    exist_tag = pd.read_sql('select * from department_label', engine)
    depart_tag = depart_tag[['yybname', 'tag']]
    depart_tag = depart_tag.append(exist_tag, ignore_index=True)
    depart_tag.drop_duplicates(keep=False, inplace=True)

    # 完成数据存储
    depart_tag.to_sql('department_label', engine, if_exists='replace', index=False)

    print(depart_tag)
    print("本次存储开盘啦营业部特色标签数据%s条" % depart_tag.shape[0])
    print("---------------------------------")


# ====================主函数====================================================================================================================================
if __name__ == '__main__':
    print("开盘啦营业部特色标签爬虫程序开始执行")
    print("--------------------------------------------")
    begin = time.time()

    # 创建Pandas读写数据库引擎
    engine = create_engine('mysql://root:123456@127.0.0.1/quant?charset=utf8')

    flag = input("是否获取当天数据，选择Y/N：")
    if flag == "Y":
        current = time.strftime("%Y-%m-%d", time.localtime())
        con_list = fengkoulSpider(flag, engine, current)
        date_list, code_list = fengkoulSpider(flag, engine, current)

    elif flag == "N":
        start = input("时间格式为：1949-10-01，请输入起始时间:")
        end = input("时间格式为：1949-10-01，请输入截止时间：")
        date_list, code_list = fengkoulSpider(flag, engine, start, end)

    tagSpider(engine, date_list, code_list)
    ed = time.time()
    print('本次程序共执行%0.2f秒.' % ((ed - begin)))
    print("开盘啦营业部特色标签爬虫程序执行完成")