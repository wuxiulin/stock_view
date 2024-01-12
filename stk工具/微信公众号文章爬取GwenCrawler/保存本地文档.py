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

def 今日更新_爬取微信公众号文章到本地(day):#
    #为空表示今天
    if(day is None or day ==''):
        daytime=datetime.datetime.now().strftime("%Y%m%d")
        print(daytime)
    else:
        daytime=day
    #读取配置文件
    conf = configparser.ConfigParser()
    conf.read('conf/cookies.cfg',encoding='utf-8')

    exclude_keys = ['cookie', 'token', 'user_agent','cut_date']
    fake_ids = [(key, conf.get("weixin", key)) for key in conf.options("weixin") if key not in exclude_keys]
    #print(fake_ids)


    for gzh, fkid in fake_ids:
        print('开始爬取 ',gzh,fkid)
        #获取文章列表
        articles_ins = ArticlesList(gzh)
        #
        list_file = articles_ins.get_articles_list_csv_update()#获取标题和连接
        parser = ParseArticles(list_file)#
        file_names = parser.daily_run(path='./articles/'+gzh)#保存路径
            


def 多日更新_爬取微信公众号文章到本地(day):#
    #为空表示今天
    if(day is None or day ==''):
        daytime=datetime.datetime.now().strftime("%Y%m%d")
        print(daytime)
    else:
        daytime=day
    #读取配置文件
    conf = configparser.ConfigParser()
    conf.read('conf/cookies.cfg',encoding='utf-8')

    exclude_keys = ['cookie', 'token', 'user_agent','cut_date']
    fake_ids = [(key, conf.get("weixin", key)) for key in conf.options("weixin") if key not in exclude_keys]
    #print(fake_ids)


    for gzh, fkid in fake_ids:
        print('开始爬取 ',gzh,fkid)
        #获取文章列表
        articles_ins = ArticlesList(gzh)
        #
        list_file = articles_ins.get_articles_list_csv_update()#获取标题和连接
        parser = ParseArticles(list_file)#
        file_names = parser.daily_run(path='./articles/'+gzh)#保存路径



if __name__ == '__main__':

    #由于微信公众号对每个token每天访问超链接那个地方的限制，好像是100次还是什么就是不让你爬取！
    #所以珍惜每天这有限次数，首先是更新今日，历史的有空然后再说！

    #，在cfg增加最新爬取时间，
    # 代码优化防止重复爬取，





    #没有调试有道云笔记，这里先保存到本地
    #在配置文件中设置截取起始日期到最新爬取！
    # articles_ins = ArticlesList('波段之门')
    # print("Start from date {}:".format(articles_ins.cut_date))
    # list_file = articles_ins.get_articles_list()#获取标题和连接
    # parser = ParseArticles(list_file)#
    # file_names = parser.run(path='./articles/波段之门')#保存路径


    #爬取的不再爬取了，要判断一下
    #读取本地文件时间列表，得到没有爬取的

    
    # articles_ins = ArticlesList('顾子明说')
    # list_file = articles_ins.get_articles_list_update(start='20210101',index=300)#获取标题和连接
    # parser = ParseArticles(list_file)#
    # file_names = parser.run(path='./articles/顾子明说')#保存路径
    
    


    #爬取文档到本地().get_today_from_config(day='20240107')
    今日更新_爬取微信公众号文章到本地(day='')


#自动下载后，同步到github上，然后有链接，被有到道云或其他地方引用
#无法自动保存到有道云，但是可以自动同步到github上，只要能保存引用就好了
#