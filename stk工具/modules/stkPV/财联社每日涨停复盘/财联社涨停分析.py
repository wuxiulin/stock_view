
from selenium import webdriver  
#https://blog.csdn.net/jsy6666/article/details/129802261?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-129802261-blog-129605194.235^v39^pc_relevant_anti_vip_base&spm=1001.2101.3001.4242.1&utm_relevant_index=3
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import re
import requests
from io import BytesIO
from PIL import Image

import sys
import os
import akshare as ak
import cv2
import easyocr
import webbrowser

from jinja2 import Template
import numpy as np
import pywencai


current_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(current_dir)
sys.path.append(current_dir)
from 获取各类数据函数 import 股票代码映射







#https://www.cls.cn/searchPage?keyword=%E6%B6%A8%E5%81%9C%E5%88%86%E6%9E%90&type=telegram

#在首页中搜索，内容不是最想要的
#在电报中搜索，得到所有条目都是想要的，太多太杂翻页问题，需要点击，加载更多，才能看到更多条目，爬取难度大，
#这里通过加日期方式，缩减结果，简化爬取
#https://www.cls.cn/searchPage?keyword=5%E6%9C%8817%E6%97%A5%E6%B6%A8%E5%81%9C%E5%88%86%E6%9E%90&type=telegram
#只有三条，就是21-22 -23年的特定日期的结果！！可以爬取了，不用翻页了！

# （1）做链接，就是搜索结果网页构建
# （2）爬取，然后得到link，在爬取link网页，
# （3）爬取link网页，得到图片，处理图片信息，具体组织再说！
# （4）按照月来保存文件	

class 财联社类( ):
	"""docstring for 财联社"""
	def __init__(self):
		pass
	def 爬取_涨停分析_网页图片(self,strday='20230517'):
		pic_path=os.path.dirname(os.path.abspath(__file__))+'/clspic/'
		print( pic_path)

		if os.path.exists(pic_path+strday+'.png'):
			return 

		if(strday[4]=='0'):
			searchtxt="{}月{}日涨停分析".format(strday[-3:-2],strday[-2:])
		elif(strday[4]=='1'):
			searchtxt="{}月{}日涨停分析".format(strday[-4:-2],strday[-2:])
		url="https://www.cls.cn/searchPage?keyword={}&type=telegram".format(searchtxt)
		#print(url)
		service = ChromeService(executable_path=ChromeDriverManager().install())
		# chrome_options = Options()
		# chrome_options.add_argument("--headless")  # 使浏览器在后台运行 有问题
		driver = webdriver.Chrome(service=service)
		driver.set_window_size(100, 100)#打开网页大小
		driver.set_window_position(100, 500)#网页位置
		driver.get(url)
		time.sleep(3)#必须简单的等待加载
		#print(driver.page_source)
		dynamic_content = driver.page_source#页面不存在可能返回不确定页面
		
		#print(dynamic_content) 
		soup  = BeautifulSoup(dynamic_content,'html.parser')
		# 使用正则表达式进行模糊匹配
		# pattern = re.compile(r'^/detail/\d+$')
		# link_elements = soup.find_all('a', href=pattern)

		# # 打印找到的元素
		# for link in link_elements:
		# 	print(link)

		#     #print(type(link))
		# 	# 输出href属性
		# 	href_value = link.get('href')
		# 	print(href_value)
 	# 		#这里默认是第一个需要的，如果出问题，在上面href=pattern增加，或者link中特殊语句判断是否，在增加判断，里面的内容等，再说

		#print(link_elements[0].get('href'))

		elements=soup.find_all('div',class_="clearfix b-c-e6e7ea search-telegraph-list")
		#print(elements)
		# 打印找到的元素
		weblink=''
		for link in elements:#多年条目
			#print(link)#每年条目
			tags=link.find_all("div")#具体时间和内容
			#print(tags[0].string)#时间标签
			if(strday[:4] in tags[0].string):#年 是对的
				#print(tags[1].find_all("div")[0])#文字内容
				templink=tags[1].find_all("a")[0].get('href')
				#print(templink)#/detail/1352506
				weblink="https://www.cls.cn{}".format(templink)
		if(len(weblink)==0):
			print("web link is none")
			return None
		else:
			#print(weblink)#爬取的页面
			pass

		#再次爬取	
		driver.get(weblink)
		time.sleep(3)#必须简单的等待加载
		#print(driver.page_source)
		dynamic_content = driver.page_source#页面不存在可能返回不确定页面
		
		#print(dynamic_content) 
		soup  = BeautifulSoup(dynamic_content,'html.parser')
		#print(soup)
		elements=soup.find_all('span',class_="telegraph-image-thumbnail")
		#<span class="telegraph-image-thumbnail" style="background-image:url(https://img.cls.cn/images/20230517/Ew637c1616.png?x-oss-process=image/resize,w_300)"></span>
		#print(elements)
		#print(elements[0].get('style'))
		#print(type(elements[0].get('style')))
		t_pic_url=elements[0].get('style')
		# 使用正则表达式提取括号内的内容
		pic_url = re.search(r'\((.*?)\)', t_pic_url)
		if pic_url:
			image_url = pic_url.group(1)
			#https://img.cls.cn/images/20230517/Ew637c1616.png?x-oss-process=image/resize,w_300
			#print(image_url)# 图片的URL
			image_url=(image_url.split('?'))[0] #高清网址
			#print(image_url)# 图片的URL
		else:
			print("No match found.")
			return None
		driver.quit()

		# 发送HTTP请求获取图片
		response = requests.get(image_url)

		# 检查响应状态
		if response.status_code == 200:
		    # 从响应中读取图像数据
			image_data = BytesIO(response.content)
		    # 使用PIL库打开图像
			img = Image.open(image_data)
			print(os.path.abspath('.'))
		    # 保存图像到本地
			img.save(pic_path+strday+".png")
			print(strday+" 图片已下载到本地。")
		else:
			print(f"下载图片时发生错误，HTTP状态码：{response.status_code}")
			return None

			#https://www.cls.cn/searchPage?keyword=%E6%B6%A8%E5%81%9C%E5%88%86%E6%9E%90&type=telegram
	def 财联社大涨股解读图像(self,strday='20230517'):#图片不同，定制特殊处理
	#由于受图片像素质量和提取库能力，效果不一样，很多信息文字提取有错误，还是要手动来修改一下。
	#不过尽可能代码就修改了，所以很多内容都是定制化的，根据实际效果特殊写的，不具有通用性

		path=os.path.dirname(os.path.abspath(__file__)) +'\\clspic\\'
		# # 读取图片
		path1=os.path.join(path,strday+".png")#路径中不能有中文
		print(path1)#似乎是不支持中文路径			
		# img = cv2.imread(str(path1))
		# if img is  None:
		# 	print(strday+".png" +" 读取有问题")
		# 将图片转换为灰度图
		img = cv2.imdecode(np.fromfile(path1, dtype=np.uint8), cv2.IMREAD_COLOR)
		if img is  None:
			print(strday+".png" +" 读取有问题")
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# 使用高斯滤波进行平滑处理
		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		# 输出二值化后的图像（可选）
		cv2.imshow('Blurred Image', blurred)
		#cv2.waitKey(0)
		cv2.destroyAllWindows()
		# 使用 EasyOCR 进行 OCR
		reader = easyocr.Reader(['ch_sim', 'en'])
		result = reader.readtext(blurred)


		if(("财联社大涨股解读" in result[0][1]) or 	 #开始用and，这里问题是汉字识别可能问题，例如上，被识别成卜
			(result[1][1] == '名称') or           #如果一个也不对，就是清晰度有问题，或者图片内容变化有问题
			(result[2][1] =="板数") or
			(result[3][1] =="涨跌幅") or
			(result[4][1] =="首次涨停") or 
			(result[5][1] =="上涨逻辑") or
			(result[6][1] =="市场焦点股") ):
			print(result[0][1] + "  图片解释正确")
		else:
			print(result[0][1] + "  图片解释错误，是图片来源问题，还是不清晰？")
		
		#以下是不具有通用性的处理文字，只能是一点点看，一点点叠加，可能有问题，注意调试
		#最简单就是一个类型一个类型的处理，就是每次添加一种处理方式，都是在前面结果上接力，
		#不要在一个循环上套用太多的处理类型。这样代码清晰，方便输出看处理的结果和原来内容，
		#增加代码而已，无所谓的！
		
		#提取图片需要的文字信息，
		txt1=[]
		for i in range(6,len(result)):
			txt1.append(result[i][1])

		#txt中此时很多错乱的文字，需要进一步处理
		#txt中此时很多错乱的文字，需要进一步处理
		#txt中此时很多错乱的文字，需要进一步处理
		
		#首先去掉带特殊符号，一般不出现，是在图片提示语句补充中，所以去掉这类字符
		txt2=[]
		for elem in txt1: 
			if(',' in elem or '。' in elem  or '(' in elem or ')' in elem ):
				continue
			else:
				txt2.append(elem)

		#
		txt3=[]
		ttype=0#各种情况
		ttdata=''
		#时间字符串在信息中，有 冒号，正常格式如下 
		#	字符串1
		#	A:B
		#正常格式如上，但是可能出现  如下 目前是这几种
		#  字符串1  A:                            字符串1
		#  B                                      A:
		#										  B
		#其次还有内容提示中带冒号，这里做了统一处理冒号
		for i in range(len(txt2)): 
			if(ttype==0):#正常情况
				#print(txt2[i])
				#print(len(txt2[i]))
				if(len(txt2[i])==0):
					continue
				if(txt2[i][-1]==':'): #字符串末尾是 冒号，
					tmep=txt2[i].split(' ')
					if(len(tmep)==2):#第一种情况
						ttype=1
						txt3.append(tmep[0])#前半部分保存
						ttdata=tmep[1]#后半是时间A部分，下次循环用
						continue
					if(len(tmep)==1):#第二种情况
						ttype=1
						ttdata=tmep[0]#后半是时间A部分，下次循环用
						continue
				if(':' in txt2[i]): #冒号，代码执行到这里没有在末尾的情况了  在中间，
				#正常时间也有，有些笔记语句含有，
					index=(txt2[i]).find(':')
					a=(txt2[i])[:index]#判断a是数字么？就是冒号后面内容是数字还是文字
					if(a.isdigit()):#纯数字构成的字符串，大概认为是时间
						txt3.append(txt2[i])
						continue
					else:#注释笔记中有冒号，跳过
						continue
				txt3.append(txt2[i])
				if(bool((re.compile(r'^\d{6}$')).match(txt2[i]))):#代码，六位数这里是做换行，方便后面文字查看
				#下面处理需要这里换行，所以这里也是为了处理方便，
				#此代码都是处理冒号，所以代码只会出现在这里，所以在这里判断，添加换行
					txt3.append('\n')

			elif(ttype==1):
				ttdata=ttdata+txt2[i]
				txt3.append(ttdata)#时间保存
				ttdata=''
				ttype=0#恢复
				continue

		temp=[]
		txt4=[]
		for itag in  txt3:#细化处理
			if(itag=='\n'):#某个股票信息块，应该是图片中一行，但是信息有问题，这里处理其中只有四条信息的情况
			#就是缺少涨停信息提示，和涨停时间，因为是大涨不是涨停
				if(len(temp)==4):#大概率是就是缺失板数和首次涨停
					if('%' in temp[1] and bool((re.compile(r'^\d{6}$')).match(temp[3]))):#进一步确认是此类
						#z涨幅数据和代码对的上，就是这种类型做处理
						txt4.append(temp[0])#
						txt4.append('-')#
						txt4.append(temp[1])#
						txt4.append('-')#
						txt4.append(temp[2])#
						txt4.append(temp[3])#
						txt4.append('\n')#
						temp=[]
					else:
						txt4=txt4+temp#
						temp=[]

				elif(len(temp)==0):#多个空行
					#txt4.append(itag)
					temp=[]
					continue
				else:#其他情况
					txt4=txt4+temp
					txt4.append('\n')#
					temp=[]

			else:#用换行做分界符
				temp.append(itag)

		# output_lines = "\n".join(txt4)	
		# file_path = "output.txt"
		# # 将结果保存到文件
		# with open(file_path, "w", encoding="utf-8") as file:
		#     file.write(output_lines)
		temp=[]
		txt5=[]
		for itag in  txt4:#细化处理
			#print(itag)
			if(itag=='\n' ):
				if(len(temp)>0):
					if(len(temp)==7):#带板块
						txt5.append(['\n'])#分行处理
						txt5.append([temp[0]])#分行处理
						formatted_list = [s.ljust(20)[:20] for s in temp]
						txt5.append(formatted_list[1:])
					else:

						formatted_list = [s.ljust(20)[:20] for s in temp]
						txt5.append(formatted_list)
					temp=[]#初始化
			else:#用换行做分界符
				temp.append(itag)

		#print(txt5)
		file_path = os.path.join(path,strday+".txt")
		# 打开一个文本文件用于写入
		with open(file_path, 'w',encoding="utf-8") as file:
		    # 遍历列表并写入文件
			for row in txt5:
				#print(row)
				formatted_row = ['{}'.format(item) for item in row]##{}是不让丢失元素的空格
				#print(formatted_row)
		        # 将每行的元素用空格连接起来，并写入文件
				file.write(''.join(formatted_row) + '\n')
		print(strday+".txt" + '  在 财联社大涨股解读图像 生成')
		print('通过网页打开  {}/{}.txt文件，手动修正数据'.format(os.path.dirname(__file__),strday))
		#这里作为观察标的
		#这里处理目的
		#观察周期股票池
		#板块和梯队，作为监控指标

	def deal_txt(self,filename=''):
		#通过网页，手动处理完了，图片文字纠错
		#这里在格式化一下，然后再次查看
		#默认保存文件名字是自定义，但是无法控制路径默认是桌面
		path=os.path.dirname(os.path.abspath(__file__)) +'/clspic/'
		file_path=os.path.join(path,filename)
		list2 = []
		try:
			with open(file_path, 'r', encoding='utf-8') as file:
				for line in file:
					#print(line)
					#处理时间字符串由于自己手动导致的中英文和空格问题
					line=line.replace('：', ':')#如果有中文冒号就替换  %是否也
					index_of_colon = line.find(":")
					if index_of_colon != -1:
					    # 去掉冒号前后的空格  xxx   10  :  90
					    line = line[:index_of_colon].rstrip() +':'+ line[index_of_colon+1:].lstrip()
					    #print(line)
					else:
					    #板块或者没有时间
					    #print(line)
					    pass
					#print(line)
					list1 = line.strip().split()  # Split the line into a list using spaces
					list2.append(list1)  # Append the list to the larger list

		except FileNotFoundError:
			print(f"The file '{file_path}' was not found.")
			return False
		except Exception as e:
			print(f"An error occurred: {e}")
			return False


		txt1=[]  #处理板块太多字符串不对导致
		for sublist in list2:
			#print(sublist)
			if(len(sublist)==0):
				continue
			elif(len(sublist)==1):
				txt1.append(sublist)
			elif(len(sublist)==6):
				txt1.append(sublist)
			elif(len(sublist)>6):
				#print("error ")
				#这里大概率是由于板块太多空格导致的导致的
				#print(sublist)
				temp=[sublist[0],sublist[1],sublist[2],sublist[3], ''.join(sublist[4:-1]) ,sublist[-1]  ]
				#print(a)
				txt1.append(temp)
			else:#缺项，丢失
				print(file_path+"  error  手动修改下面这行，主要文件名字保存，xxxx_bak.txt")

				print(sublist)
				return False

		#把最后代码放在第二个位置,方便看，和后面格式化空格添加数量
		txt2=[]
		for ele in txt1:
			if(len(ele)==1):
				txt2.append(ele)
			elif(len(ele)==6):
				ele=[ele[0],ele[5],ele[1],ele[2],ele[3],ele[4],]
				txt2.append(ele)
			else:
				print('error 9999')
				print(sublist)
				return False

		txt3=[]
		for ele in txt2:
			if(len(ele)==1):
				txt3.append(ele)
			elif(len(ele)==6):
				if len(ele[0])==4:#四个汉字
					ele[0]=ele[0].ljust(8)
				else:#三个汉字
					ele[0]=ele[0].ljust(10)

				if(ele[2]=='-' or ele[2]=='一'):
					ele[2]='-'
					ele[2]=ele[2].ljust(18)
				else:
					ele[2]=ele[2].ljust(14)

				if(ele[4]=='-' or ele[4]=='一'):
					ele[4]='-'
					ele[4]=ele[4].ljust(18)
				else:
					ele[4]=ele[4].ljust(14)

				ele=[ele[0],ele[1].ljust(15),ele[2],ele[3].ljust( 20),ele[4],ele[5].ljust(20) ]
				txt3.append(ele)
			else:
				print('error 8888')
				print(sublist)
				return False 

		file_name = filename.split('.')[0]+'_bak'+'.txt'
		file_path=os.path.join(path,file_name)
		# 打开一个文本文件用于写入
		with open(file_path, 'w',encoding="utf-8") as file:
		    # 遍历列表并写入文件
			for row in txt3:
				#print(row)
				formatted_row = ['{}'.format(item) for item in row]##{}是不让丢失元素的空格
				#print(formatted_row)
		        # 将每行的元素用空格连接起来，并写入文件
				file.write(''.join(formatted_row) + '\n')
		

		print(file_path+' 在deal中生成')
		return True



	def 财联社_每日涨停数据_pic_to_file(self,tradeday=''):
		#爬取某日财联社复盘大涨股的图片，然后提取信息，然后保存到日期中
		path=os.path.dirname(os.path.abspath(__file__))+'/clspic/'
		#print(path)

		self.爬取_涨停分析_网页图片(strday=tradeday)
		self.财联社大涨股解读图像(strday=tradeday)#获得(day).txt
		
		path1=os.path.dirname(os.path.abspath(__file__))+'/编辑图片文字信息保存到本地txt.html'
		with open(path1,'rb') as file:
			html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
		tag=soup.find_all('img',attrs={'id':'pic_src'})
		if tag:
			#src_value = tag.get('src')
			#<img id="pic_src" src="https://img.cls.cn/images/20230517/Ew637c1616.png" alt="左侧图片">
			#网络也行，本地也行，用本地吧
			tag[0]['src'] =path+tradeday+'.png'

		else:
			print("error 辑图片文字信息保存到本地txt.html ")
		path_web='依照图片手动修改内容格式.html'
		with open(path_web,"w",encoding="utf-8" ) as f:
			f.write(str(soup.prettify()))

		webbrowser.open(path_web)#手动初步编辑一下 #不太好检测是否关闭网页，这里是直接执行退出没有阻塞
		#_bak_txt形成
		while True:
			file=tradeday+'_bak.txt'
			file_path=os.path.join(path,file)
			if os.path.exists(file_path):
				print(file + '  首次手动生成')
				#print("11111")
				while  (self.deal_txt(filename=file))==False:
					print("等待处理 deal_txt 错误")
					time.sleep(30)
					pass
				  #形成bak_bak.txt
				break
			else:
				#print(' 通过网页选择文件，打开/clspic/xxx.txt文件，根据图片，手动修改解读的错误内容，保存为xxx_bak.txt')
				print(' 等待形成_bak.txt ')
				time.sleep(30)
				#手动处理图片信息后，这里再次处理一下，手动可能又问题

		webbrowser.open(path_web)#手动初步编辑一下 #不太好检测是否关闭网页，这里是直接执行退出没有阻塞
		#_bak_bak_bak.txt
		file=tradeday+'_bak_bak_bak.txt'
		while True:
			file_path=os.path.join(path,file)#形成_bak_bak.txt
			if os.path.exists(file_path):
				print(file+'  生成')
				list2=[]
				with open(file_path, 'r', encoding='utf-8') as file:
					for line in file:
						#print(line)
						list1 = line.strip().split()  # Split the line into a list using spaces
						list2.append(list1)

				data={}
				keys=[]
				key=''
				codes=[]
				for ele in list2 :
					if(len(ele)==1):
						if(len(key)==0):#新一轮
							key=ele[0]
							keys.append(key)
						else:#处理上一轮
							#print(key)
							#print(codes)
							#print('************************************************************')
							data[key]=codes
							codes=[]
							key=ele[0]
							keys.append(key)

					elif(len(ele)==6):
						codes.append(ele)
					else:
						#print("error 1112")
						print('cesih  ',ele)
						continue
				#print(key)
				#print(codes)
				data[key]=codes


				temppahttt=os.path.dirname(os.path.abspath(__file__))+'/clsdata/'
				with open(os.path.join(temppahttt,tradeday+'.txt'), 'w',encoding="utf-8") as file:
					file.write(str(data))

				out={'keys':keys,'data':data,'col':['名称','代码','板数','涨跌幅','首次涨停时间','上涨逻辑']}
				file_path=file_path=os.path.join(temppahttt,tradeday+'.json')

				with open(file_path, 'w') as json_file:
					json.dump(out, json_file)
				return out
			else:#d等待文件生成
				print('等待形成_bak_bak_bak.txt，再次确认错误修改 ')
				time.sleep(30)





	def get_财联社_每日复盘大涨数据(self,datapath='./clsdata/',tradeday=''):
		#原始数据是从财社图片爬取，然后手工处理，然后得到保存本地
		#
		#爬取某日财联社复盘大涨股的图片，然后提取信息，然后保存到日期中
		#判断当下时候有文件
		#有判断对不对
		#灭有就是
		file_path=datapath+tradeday+".json"#其他文件调用要看看路径对不对要改
		#print(file_path)

		if os.path.exists(file_path):

			with open(file_path, 'r') as json_file:
				data = json.load(json_file)
				return data
		else:
			print("开始爬取图片，手动修改错误内容后，保存数据到文件")
			a=self.财联社_每日涨停数据_pic_to_file(tradeday=tradeday)#保存在默认地方
			return a




	def 财社舍涨停表格(self,data_path1="",data_path2=""):#在上一级调用处判断展示形式，前天、昨天、今天
		#判断数据内容是否在存在

		#不存在爬取，分析图片

		path='财联社每日涨停表格.html'
		with open(path,'rb') as file:
			html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
			#print(dir(soup))
		#网页模版中默认给了一个div 和唯一id，方便查找，
		#然后再dev-id中添加新元素作为div的子元素

		#查找 是个结果列表，<div> <p>等都可能在里面，通过设置不同参数，来得到想要结果列表  https://blog.csdn.net/weixin_44015669/article/details/109603117
		#div_复盘异动=soup.find_all(id='复盘异动')
		div_标题1=soup.find_all('h2',attrs={'id':'标题1'})#pic_path1解读内容，默认是昨天的
		print(div_标题1)
		div_标题1[0].string="2023"
		print(div_标题1)
		#替换内容

		div_标题2=soup.find_all('h2',attrs={'id':'标题2'})##pic_path2解读内容，默认是今天的
		#替换内容

		path='测试.html'
		with open(path,"w",encoding="utf-8" ) as f:
			f.write(str(soup.prettify()))
		webbrowser.open(path)



	#板块，个股，等跟踪,不荣日期展现，涨停股规模，涨停资金，成交额，板块容量（去掉前10，后10后的容量）
	#是不同级别的，一个是大盘分时结合的板块轮动
	#这里是日k级别多日板块轮动角度视角看

#横轴是时间，纵轴是板块，然后鼠标悬停在板块上，出来提示信息
	#
	#
	def cls_市场焦点股(self):#也是从本地文件读取

		pass




	def 表格数据(self,today='20231215',sdata=[],templt_name="template_table.html",desname='cls_table.html'):
				#这个代码和html模版放在一个文件夹，然后再文件夹路径中cmd
		# cmd 中执行  python -m http.server
		# http://localhost:8000/index.html      就能打开index.html  刷新能看到调试状态，一种调试方式
		# http://localhost:8000/cls_table.html
		if(len(sdata)==0):
			sdata =[{"日期": [
			   				 {'symbol': 'AAPL', 'company': 'Apple Inc.', 'price': 150.25, 'change': '+2.5%'},
			  	 			 {'symbol': 'GOOGL', 'company': 'Alphabet Inc.', 'price': 2700.50, 'change': '-1.2%'},
			    			# 其他股票数据
						 	]
				    }]
		blocks_tmpts=''
		for idata in sdata:
			#print(idata)
			#print(idata.keys())
			淘汰日=list(idata.keys())[0]
			#print(淘汰日)
			stock_data=idata[淘汰日]

			column_names =stock_data[0].keys()#作为表头
			tmp_count = len(stock_data[0])  # 指定要生成的 <th> 数量
			tmp_col = """    <tr>\n{}\n    </tr> """
			tmp_tags = "\n".join(f"		<th>{{}}</th>" for i in range(tmp_count))
			tmp_col=tmp_col.format(tmp_tags)
			#print(tmp_col)
			head_content = tmp_col.format(*column_names)
			#print(head_content)


			td_count = len(stock_data[0])  # 指定要生成的 <td> 数量
			column_names =stock_data[0].keys()
			column_names = ['{' + name + '}' for name in column_names]
			html_template = """    <tr>\n{}\n    </tr> """
			# 使用循环生成 <td> 标签
			td_tags = "\n".join(f"		<td>{{}}</td>" for i in range(td_count))
			#print(td_tags)
			# 使用 format 方法将 <td> 标签插入到模板中
			template = html_template.format(td_tags)

			#print(column_names)
			# 使用 format 方法将列名插入到模板中
			formatted_template = template.format(*column_names)

			#print(formatted_template)

			# # 构建 tbody 部分
			tbody_content = ""
			for stock in stock_data:
				tbody_content += formatted_template.format(**stock)#这**呵呵很多不会用啊


			blocks_tmpt='''
			    <h1>{}</h1>
			    <table class="table">
			        <thead>
			        {}
			        </thead>
			        <tbody id="stock-table-body">  
			        {}
			        </tbody>
			    </table>


		    '''.format(淘汰日,head_content,tbody_content)
			blocks_tmpts=blocks_tmpts+blocks_tmpt

		#print(blocks_tmpt)

		# # 将生成的 tbody 替换到原始 HTML 文件中
		with open(templt_name, "r",encoding="utf-8") as file:
			html_content = file.read()
			html_content = html_content.replace("<!-- 替代部分 -->",blocks_tmpts)
 	
		with open(desname, "w",encoding="utf-8") as file:
			file.write(html_content)		

	def 每日淘汰市场焦点股(self,Newday='20231214',Oldday='20231213',Today="20231215"):
		
		New=self.get_财联社_每日复盘大涨数据(tradeday=Newday)
		New_stk= New['data']['市场焦点股']
		Ncodes=[ s[1]  for s in  New_stk]


		Old=self.get_财联社_每日复盘大涨数据(tradeday=Oldday)
		Old_stk =Old['data']['市场焦点股']
		Ocodes=[ s[1]  for s in  Old_stk]

		return [item for item in Ocodes if item not in Ncodes]

	def 统计表格_每日淘汰市场焦点股(self,	 Newday='20231214',Oldday='20231213',Today ='20231215'):
		#这里让上层输入时间，可以减少调用次数
		#需不需要全部执行，以后再说
		codes=self.每日淘汰市场焦点股(Newday=Newday,Oldday=Oldday,Today=Today)
		#Newday这天淘汰，当天表现？
		result=[]
		tempout=[]
		out=[]
		for code in codes:  
			df=ak.stock_individual_info_em(symbol=code) 
			#print(df['value'][5])
			#df['item'][5]#股票简称
			#df['item'][1]#流通市值

			#统计是old到当下振幅，涨幅，等数据
			Oldday_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=Oldday, end_date=Oldday, adjust="qfq")
			#print(Oldday_df)
			#Newday 这天个股的数据信息,看Newday这天淘汰，当天表现？
			Newday_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=Newday, end_date=Newday, adjust="qfq")
			Today_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=Today, end_date=Today, adjust="qfq")
			Oldday_Today_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=Oldday, end_date=Today, adjust="qfq")
			#print(Newday_df)
			if(len(Oldday_df['日期'])>0 and len(Newday_df['日期'])>0 and len(Today_df['日期'])>0 ):
				Newday_开盘涨幅=Newday_df['开盘'][0]/Oldday_df['收盘'][0]-1#开盘涨幅
				Newday_收盘涨幅=Newday_df['涨跌幅'][0]#开盘涨幅
				Newday_最高涨幅=Newday_df['最高'][0]/Oldday_df['收盘'][0]-1#开盘涨幅
				Newday_最低涨幅=Newday_df['最低'][0]/Oldday_df['收盘'][0]-1#开盘涨幅
				Newday_振幅=Newday_df['振幅'][0]
				Newday_换手率=Newday_df['换手率'][0]
				Newday_成交额=Newday_df['成交额'][0]
				Oldday_Today_收盘涨幅=Today_df['收盘'][0]/Oldday_df['收盘'][0]-1#
				Oldday_Today_最高涨幅=max(Oldday_Today_df['最高'])/Oldday_df['收盘'][0]-1#
				Oldday_Today_最低涨幅=min(Oldday_Today_df['最低'])/Oldday_df['收盘'][0]-1#
				Oldday_Today_振幅=(max(Oldday_Today_df['最高'])-min(Oldday_Today_df['最低']))/Oldday_df['收盘'][0]#

				#result.append([code,df['item'][5],Oldday_Today_收盘涨幅,Oldday_Today_最高涨幅,Oldday_Today_最低涨幅,Oldday_Today_振幅,
				#Newday_开盘涨幅,Newday_收盘涨幅,Newday_最高涨幅,Newday_最低涨幅,Newday_振幅,Newday_换手率,Newday_成交额,df['item'][1]])
				tempout={	
					'代码':code,
					'股票简称':df['value'][5],
					'至今涨幅':round(Oldday_Today_收盘涨幅*100,2),
					'期间最高':round(Oldday_Today_最高涨幅*100,2) ,
					'期间最低':round(Oldday_Today_最低涨幅*100,2) ,
					'期间振幅':round(Oldday_Today_振幅*100,2),
					'淘汰开盘':round(Newday_开盘涨幅*100,2) ,
					'淘汰最高':round(Newday_最高涨幅*100,2) , 
					'淘汰最低':round(Newday_最低涨幅*100,2) ,
					'淘汰收盘':Newday_收盘涨幅,
					'淘汰振幅':Newday_振幅,
					'淘汰换手': Newday_换手率,
					'淘汰成交':round(Newday_成交额/100000000,2),
					'当下流通市值':round(df['value'][1]/100000000,2)
					}
				out.append(tempout)
 									

			else:
				print("stock_zh_a_hist 获取失败")
				return None
		# result=pd.DataFrame(result, columns= ['代码','股票简称','至今涨幅','期间最高','期间最低','期间振幅','淘汰当天开盘','淘汰当天收盘',
		# 									'淘汰最高','淘汰最低','淘汰振幅','淘汰换手','淘汰成交','当下流通市值'])
		return out

	def 绘制图表网页_每日淘汰市场焦点股(self,isopenweb=0):
		stocks_data=[]

		today='20231215'
		newday='20231214'
		data=self.统计表格_每日淘汰市场焦点股(Oldday='20231213',Newday=newday,Today =today)
		stocks_data.append( {newday:data} )
		#测试,x需要一个循环调用函数这里灭有完成，后面再说
		stocks_data.append( {newday:data} )
		#print(stocks_data)
		desname=today+'_cls_table.html'
		self.表格数据(today=today,sdata=stocks_data,templt_name="template_table.html",desname=desname)
		if(isopenweb==1):
			# 用默认浏览器打开index
			print(os.path.dirname(__file__)+desname)
			webbrowser.open(os.path.dirname(__file__)+'/'+desname)


	#把数据写入到html模板中展示
	def get_chart_html_template1(self,dynamic_data,name,iswebopen=0,src_html_path='',des_html_path=''):
		src_html_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
		src_html_path= os.path.dirname(src_html_path)+'/html_template1/templates/template1.html'


		#运行这个 Python 脚本，它将生成一个 HTML 文件（比如 output.html）
		#其中包含动态数据的 JavaScript 代码。打开这个 HTML 文件，
		#你应该能够看到 Highcharts 图表，其中的曲线数据是你在 Python 中指定的动态数据。
		#读取模板文件
		with open(src_html_path, 'r', encoding='utf-8') as template_file:
		    template_content = template_file.read()

		# 创建 Jinja2 模板对象
		template = Template(template_content)

		# 使用模板渲染 HTML，传递动态数据
		#在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
		#模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
		#html_output = template.render(data=dynamic_data)
		#网页输入文本变量名称，相互区别
		voltname=(des_html_path.split('/')[-1])[:-5]
		
		html_output = template.render(data=dynamic_data,voltname=[ voltname+'_myTextarea',voltname+'_savedText'])
		# 将生成的 HTML 写入文件
		output_file_path=des_html_path
		# 创建目录结构
		os.makedirs(os.path.dirname(output_file_path), exist_ok=True)#没有路径就创建
		with open(output_file_path, 'w', encoding='utf-8') as output_file:
		    output_file.write(html_output)
		if(iswebopen==1):
			# 用默认浏览器打开生成的 HTML 文件
			webbrowser.open(os.path.abspath( output_file_path))#用output_file_path  有问题

	def get_blocks_stocks_分时(self,tradeday='20231229'):

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		#todaynow = datetime.now()
		#last_date=todaynow
		#last_date_string =todaynow.strftime("%Y%m%d")
		#last_yetd_date_string =''
		#print(last_date_string,trade_df[1])
		last_date=datetime.strptime(tradeday,'%Y%m%d')
		last_date_string=tradeday
		while True:
			if(last_date_string not in trade_df):
				last_date=last_date-timedelta(days=1)#最近上一个交易日
				last_date_string = last_date.strftime("%Y%m%d")

			else:
				lastindex= trade_df.index(last_date_string)
				last_yetd_date_string=trade_df[lastindex-1]
				break

		print(last_yetd_date_string,last_date_string)#最近交易日


		#按照板块来
		#获取财联社数据，图片数据
		cls_data=self.get_财联社_每日复盘大涨数据(tradeday=last_date_string)
		#print(cls_data.keys())
		#print(cls_data)
		cls_blks_data=cls_data['data']#字典
		day_ft=last_date_string[:4]+'-'+last_date_string[4:6]+'-'+last_date_string[6:]
		result={}
		for ikey,ivalue in cls_blks_data.items():
			#print(ikey)
			temp1={}
			for ii in ivalue:
				#print(ii[1])
				#print(ii)
				#股票代码
				#不复权数据
				上个交易日收盘价格= ak.stock_zh_a_hist(symbol=ii[1], period="daily", start_date=last_yetd_date_string, end_date=last_yetd_date_string, adjust="")['收盘'][0]
				#print(上个交易日收盘价格)
 				# 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0。1min不复权
				stock_min_df = ak.stock_zh_a_hist_min_em(symbol=ii[1], start_date=day_ft+" 09:30:00", end_date=day_ft+" 19:00:00", period='1', adjust='hfq')
				#print(stock_min_df)
				#股价数据画图
				#selected_data=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(stock_min_df['时间'],stock_min_df['收盘'])  ]
				#涨幅画图
				selected_data=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,round(100*idata/上个交易日收盘价格-100,2)]   for idate,idata in zip(stock_min_df['时间'],stock_min_df['收盘'])  ]
				#print(selected_data)
				temp1[ii[0]]=selected_data
			result[ikey]=temp1

		#按照板块依次保存数据分时
		return result

	def get_blocks_stocks_分笔(self,tradeday='20231221'):
		#接口似乎有问题，以后在测试，这里先不要弄
		#按照板块来
		#获取财联社数据，图片数据
		cls_data=self.get_财联社_每日复盘大涨数据(tradeday=tradeday)
		#print(cls_data.keys())
		#print(cls_data)
		cls_blks_data=cls_data['data']#字典
		day_ft=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]
		result={}
		for ikey,ivalue in cls_blks_data.items():
			#print(ikey)
			temp1={}
			for ii in ivalue:
				#print(ii[1])
				#print(ii)
				#股票代码转化
				codeflag=股票代码映射.股票代码映射类().get_股票代码映射_flag(flag=ii[1])
				print(codeflag)

				try:
					stock_min_df = ak.stock_zh_a_tick_tx_js(symbol=codeflag)
				except Exception as e:
					raise e
				if(stock_min_df is None or len(stock_min_df)==0 ):
					print('数据有问题 ')
					return

				selected_data=[ [ (datetime.strptime(idate, "%H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(stock_min_df['成交时间'],stock_min_df['成交价格'])  ]
				#print(selected_data)
				temp1[ii[0]]=selected_data
			result[ikey]=temp1

		#按照板块依次保存数据分时
		return result




		#返回
	def get_chart_blks_核心龙头_分时叠加(self,tradeday='20231222',iswebopen=0):
		# 左侧是上证指数，右侧是所有板块的第一个核心股的分时图，
		pass


	def get_chart_blk_stocks_分时叠加(self,tradeday='20231222',iswebopen=0):
		#https://note.youdao.com/s/Ip6sVHtc
 		#测试模板案例1  ：   左侧是上证指数，右侧是某个板块核心股的分时图，
		tempday=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]
 		#上涨指数数据
		index_df = ak.index_zh_a_hist_min_em(symbol="000001", period="1", start_date=tempday+" 09:30:00", end_date=tempday+" 19:00:00")
		#print(index_df['收盘'])
	
		selected_index_data=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(index_df['时间'],index_df['收盘'])  ]
		#print(selected_index_data)
 
		#统计数据
		#个股分时图数据

		data=self.get_blocks_stocks_分时(tradeday=tradeday)
		#print(data)

		#格式化
		左纵=0
		右纵=1
		

		for ikey ,ivalue in data.items():
			print(ikey)#板块
			dydata={'上证指数':[selected_index_data,左纵]}
			for iikey,iivalue in ivalue.items():
				dydata[iikey]=[iivalue,右纵]#每个股票的分时数据

			tempath= os.path.dirname(os.path.abspath(__file__))+ '/static/{}/{}_{}.html'.format(tradeday,tradeday,ikey)
			self.get_chart_html_template1(dydata,"无",iswebopen=iswebopen,des_html_path=tempath)
			time.sleep(5)
		#生成html  

if __name__ == '__main__':



	a=财联社类( )
	#b=a.get_财联社_每日复盘大涨数据(tradeday='20231229')
	#print(b)
	#a.get_blocks_stocks_分时()
	#a.get_blocks_stocks_分笔()

	a.get_chart_blk_stocks_分时叠加(tradeday='20231229',iswebopen=1)





    #调出是因为没有涨停，应该是这个规律
    #调出时间，调出后当下涨跌幅，调出最大跌幅，等关心的
	#a.表格数据()
	#dd=a.每日淘汰市场焦点股()
	#print(dd)
	#a.统计表格_每日淘汰市场焦点股()
	#a.绘制图表网页_每日淘汰市场焦点股(isopenweb=1)
