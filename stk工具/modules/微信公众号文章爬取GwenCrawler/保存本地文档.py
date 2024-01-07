import hashlib
import os
import queue
import shutil
import threading
import time
import uuid
import configparser
import datetime

from ArticlesList import ArticlesList
from ParseArticles import ParseArticles

class 爬取文档到本地():
 
    def __init__(self):
        pass

    def get_today_from_config(self,day=''):
        if(day is None or day ==''):
            daytime=datetime.datetime.now().strftime("%Y%m%d")
            print(daytime)
        else:
            daytime=day
        conf = configparser.ConfigParser()
        conf.read('conf/cookies.cfg',encoding='utf-8')

        fake_ids = [(key[:-8],conf.get("weixin", key)) for key in conf.options("weixin") if "_fake_id" in key]
        print(fake_ids)
        for gzh, fkid in fake_ids:
            print('开始爬取 ',gzh,fkid)
            articles_ins = ArticlesList(gzh)
            list_file = articles_ins.get_articles_list_update(start=daytime)#获取标题和连接
            parser = ParseArticles(list_file)#
            file_names = parser.run(path='./articles/'+gzh)#保存路径
            





if __name__ == '__main__':
    #没有调试有道云笔记，这里先保存到本地
    #在配置文件中设置截取起始日期到最新爬取！
    # articles_ins = ArticlesList('波段之门')
    # print("Start from date {}:".format(articles_ins.cut_date))
    # list_file = articles_ins.get_articles_list()#获取标题和连接
    # parser = ParseArticles(list_file)#
    # file_names = parser.run(path='./articles/波段之门')#保存路径


    #爬取的不再爬取了，要判断一下
    #读取本地文件时间列表，得到没有爬取的

    
    # articles_ins = ArticlesList('板块风云')
    # list_file = articles_ins.get_articles_list_update(start='20231014')#获取标题和连接
    # parser = ParseArticles(list_file)#
    # file_names = parser.run(path='./articles/板块风云')#保存路径
    
    


    爬取文档到本地().get_today_from_config(day='20240107')
    #爬取文档到本地().get_today_from_config(day='')


#自动下载后，同步到github上，然后有链接，被有到道云或其他地方引用
#无法自动保存到有道云，但是可以自动同步到github上，只要能保存引用就好了