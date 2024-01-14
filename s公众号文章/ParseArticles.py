# -*- coding: utf-8 -*-
import datetime
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup
from chinese_calendar import is_workday
from lxml import etree
import webbrowser

import os,sys
class ParseArticles():
    def __init__(self, list_file):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"}
        self.list_file = list_file

        self.html_tmpt='''
                    <!DOCTYPE html>
                    <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <title>HTML Template</title>
                        </head>
                        <body>
                        {}
                        </body>
                    </html>
                    '''



    def get_url_list(self):
        file_path = self.list_file

        if( not  os.path.exists(file_path)):
            return []
        df = pd.read_csv(file_path)
        lines = df.values.tolist()
        # url_list = df["link"].tolist()
        # time_list = df["create_time"].tolist()
        return lines

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        return response.content.decode()

    def parse_date_format(self, article_date):
        # 原来根据title来解析日期，后面直接有了date这一列，注释这一段。
        # if '早读' in title:
        #     p = re.compile(r'^(\d+)\.(\d+)早读', re.S)
        # else:
        #     p = re.compile(r'\|(\d+)\.(\d+)', re.S)
        #
        # title_date = re.search(p, title)
        # if title_date:
        #     date = str(title_date.group(1)).zfill(2) + str(title_date.group(2)).zfill(2)
        #     year = str(datetime.datetime.now().year)
        #     this_date = datetime.datetime.strptime(year + date, "%Y%m%d").date()
        #     self.pre_date = this_date
        # else:
        #     if self.pre_date:
        #         this_date = self.pre_date
        #     else:
        #         this_date = datetime.datetime.today().date()
        this_date = datetime.datetime.strptime(str(article_date)[:8], "%Y%m%d").date()
        weekday = this_date.weekday() + 1  # 周几
        year_int = this_date.isocalendar()[0]
        week_int = this_date.isocalendar()[1]
        day_int = this_date.isocalendar()[2]
        week_begin = (this_date - datetime.timedelta(day_int - 1)).strftime(format='%Y%m%d')
        week_end = (this_date + datetime.timedelta(7 - day_int)).strftime(format='%Y%m%d')
        file_name = str(year_int) + 'Y' + str(week_int) + 'W_' + week_begin + '-' + week_end
        return this_date, weekday, file_name

    # 在src字符串里，从end出往前找，找到第count个sub子字符串。
    def rfind_n_substr(self, src, sub, count, end):
        index = src.rfind(sub, 0, end)
        if index != -1 and count > 1:
            return self.rfind_n_substr(src, sub, count - 1, index - 1)
        return index




    def parse_content(self, article_date, title, html_str,path):  # 提取数据
        #print(path,article_date,type(article_date))
        savepath=path+'/'+str(article_date)[:8]#公众号名字的文件夹+时间
        if not os.path.exists(savepath):
            os.makedirs(savepath)



        item = {}
        item['title'] = title
        item['date'] = article_date
        this_date, weekday, file_name = self.parse_date_format(article_date)
        result, html_content = '', ''
        soup = BeautifulSoup(html_str, 'html.parser')
        #看网页源码，内容都在<div id=js_content>中
        html_content_arrs=[ k for k in soup.find_all('div') if k.has_attr('id') and k['id'] == 'js_content']

        if len(html_content_arrs) !=1:
            print(len(html_content_arrs))
            print('网页有问题')
            return
        else:
            html_content = html_content_arrs[0]

       # print(str(html_content))

        #另一个问题，这里不知道是不是特有的share_media_text 以后看看吧
        moshi1=html_content.find_all('div' ,class_="share_media_text")
        moshi2=html_content.find_all('p')#

        #print(html_content) 


        if(len(moshi1)==1):
            #print('1111111111')
            tagtxt = str(moshi1[0])
            # 使用正则表达式提取 content 的值
            match = re.search(r'var\s+content\s*=\s*"(.*?)";', tagtxt , re.DOTALL)
            if match:
                content_value = match.group(1)
                print(content_value)
            else:
                print("未找到 content 的值")

            html_content='<p>{}<br  /></p>'.format(content_value)

        elif(len(moshi2)>0):
            #print('222222222222')
            #处理到这里，默认基本上都是<p></p>格式(简单的公众号都是这样，都是文字加图片居多，这里不考虑很多，简化代码，有问题再说)
            for p_tag in moshi2:
                img_tag = p_tag.find('img')
                # 判断是否找到了 <img> 标签
                if img_tag:#保存图片到本地
                    # 发送HTTP请求获取图片内容
                    img_url = img_tag.get('src')
                    if img_url is not None:
                        img_response = requests.get(img_url)
                        # 获取图片文件名
                        img_filename = os.path.join(savepath, os.path.basename(img_url))
                        if img_response.status_code == 200:
                            # 保存图片到本地
                            with open(img_filename, 'wb') as img_file:
                                img_file.write(img_response.content)
                                print(f"Image '{img_filename}' downloaded successfully.")
                        else:
                            print(f"Failed to download image from URL: {img_url}")
                        #修改图片网页源码展示本地图片
                        
                        # 创建新的img标签并设置属性
                        # new_img_tag = soup.new_tag('img')
                        new_src = os.path.basename(img_url)
                        # new_img_tag['src'] = new_src
                        # new_img_tag['alt'] = 'New Image Alt Text'
                        # data_s = img_tag['data-s']
                        # # 将data-s字符串拆分为宽度和高度
                        # width, height = map(int, data_s.split(','))
                        # new_img_tag['width'] = str(1029)  # 你想设置的新宽度
                        # new_img_tag['height'] = str(height)  # 或者设置你想要的新高度 
                        # # 替换原来的img_tag
                        # img_tag.replace_with(new_img_tag)
                        img_tag['src'] = new_src


                    img_data_url = img_tag.get('data-src')
                    if img_data_url is not None:
                        img_response = requests.get(img_data_url)

                        # 使用正则表达式提取路径中的一部分
                        match = re.search(r'/([^/]+)/640', img_data_url)
                        if match:
                            extracted_part = match.group(1)
                            #print(f"Extracted part: {extracted_part}")
                        else:
                            print("error Pattern not found in data-src")
                            return 
                        # 获取图片文件名
                        img_filename = os.path.join(savepath, extracted_part+'.PNG')
                        if img_response.status_code == 200:
                            # 保存图片到本地
                            with open(img_filename, 'wb') as img_file:
                                img_file.write(img_response.content)
                                print(f"Image '{img_filename}' downloaded successfully.")
                        else:
                            print(f"Failed to download image from URL: {img_data_url}")
                        #修改图片网页源码展示本地图片
                        
                        # 创建新的img标签并设置属性
                        # new_img_tag = soup.new_tag('img')
                        new_src = extracted_part+'.PNG'
                        # new_img_tag['src'] = new_src
                        # new_img_tag['alt'] = 'New Image Alt Text'
                        # data_s = img_tag['data-s']
                        #  # 将data-s字符串拆分为宽度和高度
                        # width, height = map(int, data_s.split(','))
                        # new_img_tag['width'] = str(width)  # 你想设置的新宽度
                        # new_img_tag['height'] = str(height)  # 或者设置你想要的新高度 
                        # # 替换原来的img_tag
                        # img_tag.replace_with(new_img_tag)
                        img_tag['src'] = new_src

                    if(img_url is None  and img_data_url is None):
                        print('新图片类型，添加判断代码')
                        print(img_tag.get('class'),img_tag.get('id'),img_tag.get('src'))

                
                # a_tag = p_tag.find('a')
                # if a_tag:#
                #     #a_href = a_tag.get('href')#文字有链接，链接跳转另一个文章或网页，这里先不处理
                #     pass

            #print(html_content)
            #print(type(html_content))
            html_content=str(html_content)
            # 获取去掉最外层标签后的内容
            # 使用正则表达式匹配最外层的<div>元素
            pattern = re.compile(r'<div[^>]*>(.*?)</div>', re.DOTALL)
            match = pattern.search(html_content)
            if match:
                # 获取匹配的内容（最外层的<div>元素）
                html_content = match.group(1)
                # 打印结果
                #print(html_content)       



        html_content = re.sub(r'\n+', '', str(html_content))#去掉所有连续的换行符
        #print('####',html_content)

        html_content=self.html_tmpt.format(html_content)
        file= savepath + '/'+str(article_date).replace(' ','_').replace(':','_')+'.html'
        with open(file, 'w', encoding="utf-8") as f:
            f.write(html_content)
        print("Save to " + file)


        #webbrowser.open(os.path.join(os.getcwd(), file))#手动初步编辑一下 #不太好检测是否关闭网页，这里是直接执行退出没有阻塞

 


    def reorder_list(self, url_list):
        '''
        这段代码的主要目的是对给定的 url_list 列表进行重新排序，
        根据列表中元素的第一个元素（假设是日期或时间戳）进行分组，
        并按照日期或时间戳的降序重新组合列表。下面是对代码的含义注释
        '''
        split_list = []
        update_time = ''
        begin = 0
        for i, line in enumerate(url_list):
            if line[0] != update_time:
                if i > 0:
                    split_list.append(url_list[begin:i])
                begin = i
                update_time = line[0]
        if begin == 0:
            split_list.append(url_list[:])
        else:
            split_list.append(url_list[begin:])

        ans_list = []
        for one_day in split_list[::-1]:
            ans_list.extend(one_day)
        return ans_list

    # 运行入口函数
    def run(self,path):
        # 获取url列表和时间列表
        url_list = self.get_url_list()
        if(len(url_list)==0):
            return 
        url_list = self.reorder_list(url_list)
 
        # 遍历url列表，发送请求，获取响应
        for line in url_list:

            #print(line)
            num = line[0]
            article_date = line[1]
            title = line[2]
            # if '为你读诗' in title or '汇总' in title or '听歌学英文' in title:
            #     continue
            url = line[3]
            #print(str(num) + " Title:" + title)

            # 解析url，获得html
            html_str = self.parse_url(url)
            print("开始保存{} 内容".format(article_date))
            # 获取内容
            self.parse_content(article_date, title, html_str,path=path)
 

    # 运行入口函数
    def daily_run(self,path):
        # 获取url列表和时间列表
        url_list = self.get_url_list()
        if(len(url_list)<=0 or url_list is None ):
            print('最新文章下载更新完毕')
            return 

        url_list = self.reorder_list([url_list[0]])
 
        # 遍历url列表，发送请求，获取响应
        for line in url_list:
            print(line)
            # num = line[0]
            # article_date = line[1]
            # title = line[2]
            # # if '为你读诗' in title or '汇总' in title or '听歌学英文' in title:
            # #     continue
            # url = line[3]
            #print(str(num) + " Title:" + title)
            article_date = line[0]
            title = line[1]
            url = line[2]

            savepath=path+'/'+str(article_date)[:8]#公众号名字的文件夹+时间
            file_path= savepath + '/'+str(article_date).replace(' ','_').replace(':','_')+'.html'
            if(  os.path.exists(file_path) ):
                continue
            # 解析url，获得html
            html_str = self.parse_url(url)
            print("开始保存{} 内容".format(article_date))
            # 获取内容
            self.parse_content(article_date, title, html_str,path=path)