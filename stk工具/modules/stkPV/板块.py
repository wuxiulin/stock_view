#很重要
#同花顺和财联社新增概念
#不太清楚新增的标准是什么但是新增后，容易形成股票池和指数，就是容易形成关注度，那么这个关注度就是流量，
#容易引导共识，拉升，反复操作可能
#流量入口（关注度）--------（吸引眼球方式---新闻、广告、宣传等）
#-----------获取流量（获取关注度，得到很多人关注查看，根据信息，要么传播输入信息，
#要么传播的是思维模式，无论如何目的就是让关注到这个信息的人得到特定的结论，就是所谓共识，所以操纵人的共识、思想、行为）
#----（历史案例、理论研究宣传、逻辑自洽，洗脑、重复宣传懂方式--来洗脑影响思维或者影响信息输入，得到特定结论，
#进而让流量达成特定共识）获取支持共识


#不同地方的新增板块

#获取旧板块保存本地

#定期爬取所有板块，比较，得到新增

#输出到笔记中
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) 
#print(current_dir)
parent_dir = os.path.dirname(current_dir)
#print(parent_dir)
#sys.path.append(parent_dir)  

import pywencai 
import json
import pandas as pd
 
import time
 

import datetime
from datetime import timedelta
from selenium import webdriver  
#https://blog.csdn.net/jsy6666/article/details/129802261?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-129802261-blog-129605194.235^v39^pc_relevant_anti_vip_base&spm=1001.2101.3001.4242.1&utm_relevant_index=3
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
 
from bs4 import BeautifulSoup

 

class 概念板块( ):
	"""docstring for ClassName"""
	def __init__( self ):
		pass
	def get_新增概念板块_财联社(self,dayset=120,url='https://www.cls.cn/searchPage?keyword=%E6%A6%82%E5%BF%B5%E5%8A%A8%E6%80%81&type=depth'):
 		#安装google就可以了   
 		#https://blog.csdn.net/jsy6666/article/details/129802261?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-129802261-blog-129605194.235^v39^pc_relevant_anti_vip_base&spm=1001.2101.3001.4242.1&utm_relevant_index=3
		service = ChromeService(executable_path=ChromeDriverManager().install())
		# chrome_options = Options()
		# chrome_options.add_argument("--headless")  # 使浏览器在后台运行 有问题
		driver = webdriver.Chrome(service=service)
		driver.set_window_size(100, 100)#打开网页大小
		driver.set_window_position(100, 500)#网页位置
		driver.get(url)
		time.sleep(5)#必须简单的等待加载
		#print(driver.page_source)
		dynamic_content = driver.page_source
		driver.quit()
		#print(dynamic_content) 
		soup  = BeautifulSoup(dynamic_content,'html.parser')
		link_element=soup.find_all('div',class_='subject-interest-image-content-box')
		# print(type(link_element[0]))
		# print(link_element[0].div.a.get_text())
 
		# 处理数组
		array = []

		for element in link_element:
			#print(type(element))
			tag_eles=element.find_all('div')#孩子div
			notion=tag_eles[0].a.get_text()
			#print(tag_eles[0].a.get_text())
			if("财联社主题库新增" not in notion):
				continue
			tag_eles=element.find_all('div')#孩子div
			time_tag=tag_eles[2].div.span.get_text()
			#print(time_tag)
			#这里可以添加时间戳判断，	
			time_tags=time_tag.split(" 星期")
			#print(time_tags)
			
			time_obj = datetime.datetime.strptime(time_tags[0], "%Y-%m-%d %H:%M")
			current_time =datetime.datetime.now()
			if(current_time - time_obj  > timedelta(days=dayset)):
				continue
			#print(notion,time_tag)
			notion=(notion.split('|'))[1]
			notiontime=notion+" "+time_tag
			array.append(notiontime)
		return array

	def get_新增概念板块_同花顺(self,dayset=120):
		current_dir = os.path.dirname(os.path.abspath(__file__)) 
		#print(current_dir)
		filename = "同花顺新增概念板块.json"
		file_path=os.path.join(current_dir,filename)

		if os.path.exists(file_path):#新文件存在
		    # 文件存在，读取内容
			with open(file_path, 'r') as json_file:
				pre_data = json.load(json_file)
		else:
			pre_data={}

		#print(pre_data)
		df_blocks=self.get_新增概念板块_同花顺_辅助()
		#print(df_blocks)
		if(df_blocks.empty):#这里不用返回还要处理
			res=[]
			#处理结果，然后再次保存，
			for key in pre_data.keys():
				current_time=datetime.datetime.now()
				timetag=datetime.datetime.strptime(key, "%Y-%m-%d")
				#print(current_time - timetag)
				if(current_time - timetag < timedelta(days=dayset)):
					#print("9999999999999999999999")
					#print(pre_data[key]+" "+key)
					res.append(pre_data[key]+" "+key)
				else:
					pre_data.pop(key)#时间太久了不要了
			#保存
			with open(file_path, 'w') as json_file:
				json.dump(pre_data, json_file)
			return  res[::-1]

		df_blocks=list(df_blocks["指数简称"])
		out=""
		for blk in df_blocks:
			out=out+blk+" "
		#获取当下时间标签
		current_time =datetime.datetime.now()
		timetag=datetime.datetime.strftime(current_time, "%Y-%m-%d")
		if(timetag in pre_data.keys()):
			if(out not in pre_data[timetag]):
				pre_data[timetag]=pre_data[timetag] + " " +out#这里处理有重复算了有问题再说
		else:
			pre_data[timetag]=out


		res=[]
		#处理结果，然后再次保存，
		for key in pre_data.keys():
			current_time=datetime.datetime.now()
			timetag=datetime.datetime.strptime(key, "%Y-%m-%d")
			if(current_time - timetag < timedelta(days=120)):
				#print("BBBBBB")
				#print(type(key))
				res.append(pre_data[key]+" "+key)
			else:
				pre_data.pop(key)#时间太久了不要了
		#保存
		with open(file_path, 'w') as json_file:
			json.dump(pre_data, json_file)
		
		return res[::-1]
		





	def get_新增概念板块_同花顺_辅助(self,searchtxt='概念板块'):
		current_dir = os.path.dirname(os.path.abspath(__file__)) 
		#print(current_dir)
		filename="同花顺概念板块" + ".json"
		old_filename='old_'+filename
		file_path = os.path.join(current_dir,filename)
		old_file_path = os.path.join(current_dir,old_filename)
		if os.path.exists(file_path) and os.path.getsize(file_path) > 0:#空json load会报错
		    # 文件存在，读取内容
			pre_data=pd.read_json(file_path, orient='records')
			#print(pre_data.head(6))
		else:
			pre_data=None
		
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='zhishu',sort_key="指数代码")#测试'
		except Exception as e:
			print(e,"get_新增概念板块_同花顺  pywencai.get    is error ") 
			return None
		res=res[["指数代码","指数简称"]]
		# print(res)
		# print(pre_data.head(3))
		# print(res.head(3))

		if(res is None):
			return  None
		else:
			#print(res)
			if(pre_data is  not None):
				missing_rows = res[~res.isin(pre_data.to_dict(orient='list')).all(axis=1)]
			else:
				missing_rows=None
 
		#print(missing_rows)
		if os.path.exists(file_path):#新文件存在
			if os.path.exists(old_file_path):
				os.remove( old_file_path)
				os.rename(file_path, old_file_path)#备份
			else:
				os.rename(file_path, old_file_path)#备份
				# 使用 json.dump 将字典保存为 JSON 文件
		else:#新文件不存在
			res.to_json(old_file_path, orient='records')
		res.to_json(file_path, orient='records')
		#print(missing_rows)


		return missing_rows

 




if __name__ == '__main__':
	a=概念板块().get_新增概念板块_同花顺()
	print(a)
	#概念板块().get_新增概念板块_财联社()
	pass






