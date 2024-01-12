#https://note.youdao.com/s/bhnffVZ0
#https://zhuanlan.zhihu.com/p/379062852
#两个笔记类似思路，根据笔记中，开发者工具中，网络中，https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=MjM5NDY3ODI4OA==&type=9&query=&token=1983840068&lang=zh_CN&f=json&ajax=1
#这里链接自己在23.12.30日，没找到，
#没有类似找到fakeid。猜测是公共号防止爬取，隐藏了这个fake_id,而不是删除，要是删除fake_id,整个微信公众号架构要调整很多，所以猜测是隐藏了
#找了很久，巧合是在第二个文章中，有之前北邮家教部公众号的的fakeid，如下
#https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin=0&count=5&fakeid=MjM5NDY3ODI4OA==&type=9&query=&token=1983840068&lang=zh_CN&f=json&ajax=1
#fakeid=MjM5NDY3ODI4OA，，，，其次我把token=198384006  替换成当下自己浏览器的，就能使用这个链接，内容是对的
#就是说格式一直没有变，隐藏了fakeid而已
#所以，问题变成了，怎么找公众号fakeid，尝试了一下，不好找，后来想到思路是，fakeid=MjM5NDY3ODI4OA不变，
#那网页打开北邮家教部某个文章，在返回响应中，应该有个fakeid，https://mp.weixin.qq.com/s/_0_1R2Fsa3UgkwdIKvX3qQ
#结果没有fake，但是搜索MjM5NDY3ODI4OA是有的出现很多次， _g.msg_link = "http://mp.weixin.qq.com/s?__biz=MjM5NDY3ODI4OA==&amp;mid=2652705234&amp;idx=1&amp;sn=c990dfc896d0a155e9a7b17d32e81a1b&amp;chksm=bd6da2ad8a1a2bbb0ce27f5a6b17eadd280b6a383bc1e5a42867932af9ef2dfbdd31072dd45e#rd";
#__biz 来看其后fakeid   这就提供一方法，就是通过公众号文章，寻找fakeid，然后再利用这的代码，就可以了！
#目前看，微信会根据网上爬取方式来调整架构，反爬取，关闭了很多自动化功能！！





# -*- coding: utf-8 -*-
from datetime import datetime ,timedelta
import random
import time
import configparser
import pandas as pd
import requests
import json
import os,sys

class ArticlesList:
    def __init__(self,公众号名字):
        self.公众号名字=公众号名字
        self.BEGIN = '0'
        conf = configparser.ConfigParser()
        conf.read('conf/cookies.cfg',encoding='utf-8')
        # cut_date is the start date for this running
        self.cut_date = conf.get("weixin", "cut_date")
        #print(self.cut_date)
        cookie = conf.get("weixin", "cookie")
        token = conf.get("weixin", "token")
        fake_id = conf.get("weixin", 公众号名字)
        user_agent = conf.get("weixin", "user_agent")
        #print(cookie)
        #print(user_agent)
        self.FAKEID = fake_id
        # 使用Cookie，跳过登陆操作
        self.headers = {
            "Cookie": cookie,
            "User-Agent": user_agent,
        }
        self.TOKEN = token

        self.data = {
            "token": token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": "1",
            "action": "list_ex",
            "begin": "0",
            "count": "5",
            "query": "TeacherGwen",
            "fakeid": fake_id,
            "type": "9",
        }
        
        print('第一步  手动登录网站：https://mp.weixin.qq.com/')       
        # print("【weixin token】: ", token) 
        # print("【weixin fake_id】: ", fake_id)
        # print("【weixin user_agent】: ", user_agent)
        # print("【weixin cookie】: ", cookie)
        #没找到方法手动登录后自动获取这些，以后用空再说吧


    def get_articles_list_csv_update(self):
        #根据csv最新时间开始，更新到当下今日
        path='articles/'+self.公众号名字+'/'
        list_file = path +self.公众号名字+ ".csv"#爬取代码的时间文章列表

        if  os.path.exists(list_file):
            df = pd.read_csv(list_file)
            #lines = df.values.tolist()
            time_list = df["date"].tolist()

            if(len(time_list)>0):#非空
                csvend=datetime.strptime(str(time_list[0]), '%Y%m%d  %H:%M:%S')
                # csvstart=datetime.strptime(str(time_list[len(time_list)-1]), '%Y%m%d')  
            else:
                csvend=datetime.now()#只更新今天的
                df=None
        else:
            csvend= datetime.now() - timedelta(days=1)#只更新今天的
            df=None
        #print(csvend)
        content_list = []
        break_flag = False
        for i in range(10000):#大数替换While True，防止出不来
            self.BEGIN = str(i * 5)
            print("Get page " + str(i + 1))
            # url里面包含了参数信息，不需要用data，如果url不带信息只有data参数也不行。
            # 目标url
            url = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={BEGIN}&count=5&fakeid={FAKEID}==&type=9&query=&token={TOKEN}&lang=zh_CN&f=json&ajax=1".format(
                BEGIN=self.BEGIN, FAKEID=self.FAKEID, TOKEN=self.TOKEN)
            s = requests.Session()
            #print(url)
            # 使用get方法进行提交
            # content_json = requests.get(url, headers=headers, payload=data).json()
            res = requests.request("GET", url, headers=self.headers)

            if res.status_code == 200:
                content_json = res.json()
                if res.cookies.get_dict():  
                    # 保持cookie有效。这样做的目的通常是为了在后续的请求中保持会话的状态，特别是如果服务器使用 cookies 来管理用户的身份验证或会话信息。
                    #通过这种方式，s 对象将持有先前响应中获取的任何 cookies，这在后续的请求中将继续有效，模拟了用户在同一会话中进行多个请求的行为。
                    s.cookies.update(res.cookies)
                if 'app_msg_list' in content_json.keys():
                    # 返回了一个json，里面是每一页的数据
                    #print(type(content_json['app_msg_list']))
                    for item in content_json["app_msg_list"]:
                        #print(item)
                        # 提取每页文章的标题及对应的url
                        items = []
                        #print(item['update_time'],type(item['update_time']))
                        #tupTime = time.localtime(item['update_time'])
                        tupTime=datetime.fromtimestamp(item['update_time'])
                        #print(type(tupTime))
                        #print(tupTime,type(tupTime))
                        #cut_date_struct = datetime.strptime( , "%Y%m%d")
                        #print(tupTime,cut_date_struct)
                        # standardTime = time.strftime("%Y-%m-%d %H:%M:%S", tupTime)
                        #print(tupTime,csvend)
                        #print(tupTime,csvend)
                        if tupTime <= csvend:
                            break_flag = True
                            break
                        standardTime = tupTime.strftime("%Y%m%d %H:%M:%S")  # 获得日期
                        items.append(standardTime)
                        items.append(item["title"])
                        items.append(item["link"])
                        content_list.append(items)

                    if break_flag:
                        break
                    sleep_time = random.randint(5, 15)  # 随机sleep时间
                    time.sleep(sleep_time)
                else:
                    print("更新token 和cookies")
                    print('方法是，第一步：登录 https://mp.weixin.qq.com/ 首页网址中就有，类似https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=2097716489')
                    print('取出 token,存入conf/cookies.cfg中，对应项目中')

                    print('第二步：内容与互动-草稿箱-新的创作-写新图文  ')
                    print('F12开发者模式，点击“网络”，CTRL+R,看到‘名称’中，点击appmsgxxxx,表头，请求表头，复制其中cookie到存入conf/cookies.cfg中，对应项目中')
                    break
            else:
                print("Can't access to Weixin Dingyuehao.")

        #print(content_list)


        path='articles/'+self.公众号名字+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        list_file = path + self.公众号名字 + ".csv"#爬取代码的时间文章列表
        #print(df)
        if(df is None or len(df)==0):
            if(len(content_list)==0):
                print("最新文件列表保存成功1")
                return list_file
            else:
                name = [ 'date', 'title','link']
                test = pd.DataFrame(columns=name, data=content_list)
                test.to_csv(list_file, mode='w', encoding='utf-8',index=False)
                print("最新文件列表保存成功1")
                return list_file
        else:#合并，新的内容放在最前面
            if(len(content_list)==0):
                print("最新文件列表保存成功1")
                return list_file
            else:
                test=pd.concat([pd.DataFrame(content_list), df], ignore_index=True)#更新内容前放
                test.to_csv(list_file, mode='w', encoding='utf-8',index=False)
                print("最新文件列表保存成功1")
                return list_file



    #通过csv判断跟新爬取页
    def get_articles_list(self,start=None):#end 没有用了，因为无论是啥，都会先更新最新的，
        #读取csv，看最早和最晚时间t1，t2，爬取过中间就不会不应噶确实，
        #根据start，end，判断，是否爬取过，重新确定，判定爬取结束时间
        self.get_articles_list_csv_update()#无论输入如何，最新的都应该保存，其次后续分类计算page页码

        if(start is None or start == ''):
            start =self.cut_date
        inputstart=datetime.strptime(start , '%Y%m%d')
        #inputend = datetime.strptime(end , '%Y%m%d')

        path='articles/'+self.公众号名字+'/'
        list_file = path +self.公众号名字+ ".csv"#爬取代码的时间文章列表
        if  os.path.exists(list_file):
            df = pd.read_csv(list_file)
            #print(df)
            #lines = df.values.tolist()
            if(len(df)==0):
                csvstart=datetime.now()
                df=None
            else:
                time_list = df["date"].tolist()
                #csvend=datetime.strptime(time_list[0], '%Y%m%d')
                csvstart=datetime.strptime(str(time_list[len(time_list)-1]), '%Y%m%d %H:%M:%S')
        else:
            csvstart=datetime.now()-timedelta(days=1)#只更新今天的
            df=None

        print('csvstart: ',csvstart)

        if(inputstart >= csvstart):
            print("没有需要更新的文章列表")#都在csv里了，无序爬取
            return list_file
        if(df is None or len(df)==0):
            startpagenum=0
        else:
            startpagenum=int(len(df)/5)

        content_list = []   
        break_flag = False
        for i in range(startpagenum,10000,1):#大数替换While True，防止出不来
            self.BEGIN = str(i * 5)
            print("Get page " + str(i + 1))
            # url里面包含了参数信息，不需要用data，如果url不带信息只有data参数也不行。
            # 目标url
            # url = "https://mp.weixin.qq.com/cgi-bin/appmsg" # incorrect. It's just search the articles.
                  #https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&token=2097716489&lang=zh_CN&timestamp=1703931836753
            url = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={BEGIN}&count=5&fakeid={FAKEID}==&type=9&query=&token={TOKEN}&lang=zh_CN&f=json&ajax=1".format(
                BEGIN=self.BEGIN, FAKEID=self.FAKEID, TOKEN=self.TOKEN)
            s = requests.Session()
            #print(url)
            # 使用get方法进行提交
            # content_json = requests.get(url, headers=headers, payload=data).json()
            res = requests.request("GET", url, headers=self.headers)

            if res.status_code == 200:
                content_json = res.json()
                if res.cookies.get_dict():  
                    # 保持cookie有效。这样做的目的通常是为了在后续的请求中保持会话的状态，特别是如果服务器使用 cookies 来管理用户的身份验证或会话信息。
                    #通过这种方式，s 对象将持有先前响应中获取的任何 cookies，这在后续的请求中将继续有效，模拟了用户在同一会话中进行多个请求的行为。
                    s.cookies.update(res.cookies)
                if 'app_msg_list' in content_json.keys():
                    # 返回了一个json，里面是每一页的数据
                    for item in content_json["app_msg_list"]:
                        # 提取每页文章的标题及对应的url
                        items = []
                        #tupTime = time.localtime(item['update_time'])
                        tupTime=datetime.fromtimestamp(item['update_time'])

                        #cut_date_struct = time.strptime(self.cut_date, "%Y%m%d")
                        #print(tupTime,cut_date_struct)


                        if tupTime < inputstart:#合并后的开始时间
                            break_flag = True
                            break
                        standardTime = tupTime.strftime("%Y%m%d  %H:%M:%S")  # 获得日期
                        items.append(standardTime)
                        items.append(item["title"])
                        items.append(item["link"])
                        content_list.append(items)     

                    
                    if break_flag:
                        break
                    sleep_time = random.randint(5, 15)  # 随机sleep时间
                    time.sleep(sleep_time)
                else:
                    print("更新token 和cookies")
                    print('方法是，第一步：登录 https://mp.weixin.qq.com/ 首页网址中就有，类似https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=2097716489')
                    print('取出 token,存入conf/cookies.cfg中，对应项目中')

                    print('第二步：内容与互动-草稿箱-新的创作-写新图文  ')
                    print('F12开发者模式，点击“网络”，CTRL+R,看到‘名称’中，点击appmsgxxxx,表头，请求表头，复制其中cookie到存入conf/cookies.cfg中，对应项目中')
                    break
            else:
                print("Can't access to Weixin Dingyuehao.")

        #print(content_list)
        name = ['date','title', 'link']
        # test = pd.DataFrame(columns=name, data=content_list)
        # this_date = datetime.now()
        # this_date = this_date.strftime(format='%Y%m%d')

        path='articles/'+self.公众号名字+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        list_file = path  +self.公众号名字+ ".csv"#爬取代码的时间文章列表
        if(df is None):
            if(len(content_list)==0):
                print("文件列表保存成功")
                return list_file
            else:
                test = pd.DataFrame(columns=name, data=content_list)
                test.to_csv(list_file, mode='w', encoding='utf-8',index=False)
                print("文件列表保存成功")
                return list_file
        else:#合并，新的内容放在最前面
            if(len(content_list)==0):
                print("文件列表保存成功")
                return list_file
            else:
                #print(df)
                #print(content_list)
                test=pd.concat([ df,pd.DataFrame(columns=name, data=content_list)], ignore_index=True)#更新内容后放
                #print(test)
                test.to_csv(list_file, mode='w', encoding='utf-8',index=False)
                print("最新文件列表保存成功")
                return list_file


    #通过本地文件夹获取要爬取页码，认为文件夹时间段内是完整，不缺失的，
    def get_articles_list_file_update(self,start=None):#爬取特定日子，不都爬取
        self.get_articles_list_csv_update()#无论输入如何，最新的都应该保存，其次后续分类计算page页码
        if(start is None or start == ''):
            start=self.cut_date 
            inputstart=datetime.strptime(start , '%Y%m%d')
        else:
            inputstart=datetime.strptime(start , '%Y%m%d')
        #inputend = datetime.strptime(end , '%Y%m%d')

        path='articles/'+self.公众号名字+'/'
        list_file = path +self.公众号名字+ ".csv"#爬取代码的时间文章列表
        if  os.path.exists(list_file):
            df = pd.read_csv(list_file)
            #lines = df.values.tolist()
            if(len(df)==0):
                csvstart=datetime.now()
            else:
                time_list = df["date"].tolist()
                #csvend=datetime.strptime(time_list[0], '%Y%m%d')
                csvstart=datetime.strptime(str(time_list[len(time_list)-1]), '%Y%m%d %H:%M:%S')
        else:
            csvstart=datetime.now()
            df=None

        if(inputstart > csvstart):
            #crawt=[inputstart,csvstart]#因为即使end<csvstart,也无法只爬取【start，end],无法精确算出到底多少页，所以所以还跌爬取end到csvstart
        #else:
            print("没有需要更新的文章列表")#都在csv里了，无序爬取
            return list_file

        path='articles/'+self.公众号名字+'/'
        if not os.path.exists(path):
            os.makedirs(path)
            #self.cut_date=start
            folders=[]
        else:
            folders = [folder for folder in os.listdir(path) if os.path.exists(os.path.join(path, folder+'/'+folder+'.html'))]#已经爬取过的
        
        if len(folders)>0:
            filestart=  datetime.strptime(min(folders), '%Y%m%d')
            fileend= datetime.strptime(max(folders), '%Y%m%d')  


        startpagenum=0
        if(fileend < csvstart):
            if(df is None or len(df)==0):
                startpagenum=0
            else:
                startpagenum=int(len(df)/5)
        elif(filestart < csvstart):
            if(inputstart >= filestart):
                print("没有需要更新的文章列表")#都在csv里了，无序爬取
                return list_file
            #需要爬取
            if(df is None or len(df)==0):
                csvdays=[]
            else:
                csvdays=df["date"].tolist()
                csvdays=[str(item)for item in csvdays]
                csvdays_temp=[ item[:8]  for item in csvdays]
            #合并日期，
            templen=list(set(folders) | set(csvdays_temp))#已经有title或者已经爬取的日期
            startpagenum=int(templen/5)
        else:
            if(inputstart >= filestart):
                print("没有需要更新的文章列表")#都在csv里了，无序爬取
                return list_file                
            if(df is None or len(df)==0):
                startpagenum=0
            else:
                startpagenum=int(len(df)/5)


        content_list = []   
        break_flag = False
        #print('startpagenum:',startpagenum)
        for i in range(startpagenum,10000,1):#大数替换While True，防止出不来
            self.BEGIN = str(i * 5)
            print("Get page " + str(i + 1))
            # url里面包含了参数信息，不需要用data，如果url不带信息只有data参数也不行。
            # 目标url
            # url = "https://mp.weixin.qq.com/cgi-bin/appmsg" # incorrect. It's just search the articles.
                  #https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit_v2&action=edit&isNew=1&type=77&token=2097716489&lang=zh_CN&timestamp=1703931836753
            url = "https://mp.weixin.qq.com/cgi-bin/appmsg?action=list_ex&begin={BEGIN}&count=5&fakeid={FAKEID}==&type=9&query=&token={TOKEN}&lang=zh_CN&f=json&ajax=1".format(
                BEGIN=self.BEGIN, FAKEID=self.FAKEID, TOKEN=self.TOKEN)
            s = requests.Session()
            #print(url)
            # 使用get方法进行提交
            # content_json = requests.get(url, headers=headers, payload=data).json()
            res = requests.request("GET", url, headers=self.headers)

            if res.status_code == 200:
                content_json = res.json()
                if res.cookies.get_dict():  
                    # 保持cookie有效。这样做的目的通常是为了在后续的请求中保持会话的状态，特别是如果服务器使用 cookies 来管理用户的身份验证或会话信息。
                    #通过这种方式，s 对象将持有先前响应中获取的任何 cookies，这在后续的请求中将继续有效，模拟了用户在同一会话中进行多个请求的行为。
                    s.cookies.update(res.cookies)
                if 'app_msg_list' in content_json.keys():
                    # 返回了一个json，里面是每一页的数据
                    for item in content_json["app_msg_list"]:
                        # 提取每页文章的标题及对应的url
                        items = []
                        tupTime = time.localtime(item['update_time'])
                        tupTime=datetime.fromtimestamp(item['update_time'])

                        if tupTime < inputstart:#合并后的开始时间
                            break_flag = True
                            break
                        standardTime = tupTime.strftime("%Y%m%d  %H:%M:%S")  # 获得日期
                        items.append(standardTime)
                        items.append(item["title"])
                        items.append(item["link"])
                        content_list.append(items)
                    if break_flag:
                        break
                    sleep_time = random.randint(5, 15)  # 随机sleep时间
                    time.sleep(sleep_time)
                else:
                    print("更新token 和cookies")
                    print('方法是，第一步：登录 https://mp.weixin.qq.com/ 首页网址中就有，类似https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=2097716489')
                    print('取出 token,存入conf/cookies.cfg中，对应项目中')

                    print('第二步：内容与互动-草稿箱-新的创作-写新图文  ')
                    print('F12开发者模式，点击“网络”，CTRL+R,看到‘名称’中，点击appmsgxxxx,表头，请求表头，复制其中cookie到存入conf/cookies.cfg中，对应项目中')
                    break
            else:
                print("Can't access to Weixin Dingyuehao.")

        #print(content_list)
        name = [ 'date','title', 'link']
        test = pd.DataFrame(columns=name, data=content_list)
        this_date = datetime.now()
        this_date = this_date.strftime(format='%Y%m%d')

        path='articles/'+self.公众号名字+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        list_file = path  +self.公众号名字+ ".csv"#爬取代码的时间文章列表
        if(df is None):
            if(len(content_list)==0):
                print("文件列表保存成功")
                return list_file
            else:
                name = ['date','title' , 'link']
                test = pd.DataFrame(columns=name, data=content_list)
                test.to_csv(list_file, mode='w', encoding='utf-8',index=False)
                print("文件列表保存成功")
                return list_file
        else:#合并，新的内容放在最前面
            if(len(content_list)==0):
                print("文件列表保存成功")
                return list_file
            else:
                test=pd.concat([ df,pd.DataFrame(columns=name, data=content_list)], ignore_index=True)#更新内容后放
                #print(test)
                test.to_csv(list_file, mode='w', encoding='utf-8',index=False)
                print("最新文件列表保存成功")
                return list_file


    def 去掉重复项(self):
        #由于每页不能精准定位，所以会有重复项目，但是不多，所以可以最后处理csv就是了，页可以不处理问题不大
        pass



if __name__ == '__main__':
    ArticlesList(公众号名字='波段之门').get_articles_list_csv_update()
    ArticlesList(公众号名字='波段之门').get_articles_list()
    ArticlesList(公众号名字='波段之门').get_articles_list_file_update()
    # #(1)  csv为空，死后时间设置，可能永远无法爬取，
    # （）一天多个文章，爬取不到第二三骗；额

    pass