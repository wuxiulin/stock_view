#因为note的只有一个地方用，这里不做类似在其他某班复制文件夹static的处理了


# import sys
# import os
# current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# parent_dir = os.path.dirname(current_dir)
# print(parent_dir)
# sys.path.append(parent_dir)

#处理html虽然python自带html库，但是似乎不好用，主流是BeautifulSoup、urllib.requests
#似乎BeautifulSoup更好用

#读取指定html
#运行各种监控代码得到结论
#在html默认位置，根据结论添加文本
#输出保存html
import webbrowser
import string
from bs4 import BeautifulSoup
import  pathlib

#from  stk工具.common import DataStruct


import sys
import os

class 复盘笔记类( ):
	def __init__(self):
		pass
		

	def deal_html(self,data,ttype,tmpl):

		if(ttype=="blocks"):
			tempdata=data['blocks']
			temppath="help-center/"+'blocks.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'blocks.html'#默认了，tmpl接口为了以后其他网址用，或修改用
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
		elif(ttype=="index"):
			tempdata=data['index']
			temppath="help-center/"+'index.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'index.html'#默认了，tmpl接口为了以后其他网址用，或修改用
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
		elif(ttype=="stocks"):
			tempdata=data['stocks']
			temppath="help-center/"+'stocks.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'stocks.html'#默认了，tmpl接口为了以后其他网址用，或修改用
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
		elif(ttype=="time"):

			tempdata=data['time']
			temppath="help-center/"+'timepoint.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'timepoint.html'#默认了，tmpl接口为了以后其他网址用，或修改用
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
		elif(ttype=='emotional_cycle'):
			tempdata=data['emotional_cycle']
			temppath="help-center/"+'emotional_cycle.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'emotional_cycle.html'#默认了，tmpl接口为了以后其他网址用，或修改用
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版

		elif(ttype=='daily_notes'):
			tempdata=data['daily_notes']
			temppath="help-center/"+'daily_notes.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			path_txt=pathlib.Path(__file__).absolute().parent/"help-center/templates/tmpl_daily_notes.txt"
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'daily_notes.html'#默认了，tmpl接口为了以后其他网址用，或修改用
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			#处理格式字符串	
			with open(path_txt,'rb') as file:
				daily_notes_txt = file.read()
				# 解码为字符串
				daily_notes_str = daily_notes_txt.decode('utf-8')
			#print(data['daily_notes'])
			#print(daily_notes_str)
			daily_notes_str=daily_notes_str.format(**(tempdata[0]))
			#print(daily_notes_str)
			tempdata[0]=daily_notes_str#把输入数据转为格式化字符串，
			#
		elif(ttype=='daily_dapan_notes'):
			tempdata=data['daily_dapan_notes']
			temppath="help-center/"+'daily_notes.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'daily_notes.html'#默认了，tmp
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
		elif(ttype=='dynamic_monitor'):
			tempdata=data['dynamic_monitor']
			temppath="help-center/"+'dynamic_monitor.html'#默认了，tmpl接口为了以后其他网址用，或修改用
			path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
			if os.path.exists(path):#目标文件存在
				pass
			else:
				temppath="help-center/templates/"+"tmpl_"+'dynamic_monitor.html'#默认了，tmp	
				path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版

		else:
			print("type is error")
			return

		if(ttype=="blocks" or ttype=="index" or ttype=="stocks" or ttype=="time"):
			#print(path)
			with open(path,'rb') as file:
				html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
			#print(dir(soup))
			div_异动=soup.find_all('div',attrs={'id':'复盘异动'})#复盘异动'需要手动添加，方便快速定位添加元素简化操作
			for i in range(len(tempdata)):
				#添加异动信号文字信息
				newtag = soup.new_tag('p')
				newtag.string=str(tempdata[i][0]).replace("[", "").replace("]", "").replace("'", "") 
				newtag['style'] = f'display: block; background-color: cyan; padding: 10px; text-decoration: none; color: black;'
				div_异动[0].append(newtag)
				#添加链接
				# 使用new_tag创建一个'a'标签
				link_tag = soup.new_tag('a')
				# 设置链接地址
				link_tag['href'] = tempdata[i][1]
				#print(tempdata[i][1])
				# 添加文本内容
				link_tag.string = 'notelink'
				link_tag['target'] = "_blank" # 添加这一行来设置在新标签页中打开链接
				#设置这个<a>是高亮块

				div_异动[0].append(link_tag)
			temppath="help-center/"+tmpl
			path=pathlib.Path(__file__).absolute().parent/temppath #调试原来网址和保存分来，以后不用了
			with open(path,"w",encoding="utf-8" ) as f:
				f.write(str(soup.prettify()))
		elif(ttype=='emotional_cycle'):
			with open(path,'rb') as file:
				html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
			div_异动=soup.find_all('div',attrs={'id':'复盘异动'})#复盘异动'需要手动添加，方便快速定位添加元素简化操作
			for i in range(len(tempdata)):
				#添加异动信号文字信息
				newtag = soup.new_tag('p')
				newtag.string=str(tempdata[i] ).replace("[", "").replace("]", "").replace("'", "") 
				newtag['style'] = f'display: block; background-color: cyan; padding: 10px; text-decoration: none; color: black;'
				div_异动[0].append(newtag)
			temppath="help-center/"+tmpl
			path=pathlib.Path(__file__).absolute().parent/temppath #调试原来网址和保存分来，以后不用了
			with open(path,"w",encoding="utf-8" ) as f:
				f.write(str(soup.prettify()))
		
		elif(ttype=='daily_notes'):


			with open(path,'rb') as file:
				html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
			div_异动=soup.find_all('div',attrs={'id':'复盘异动'})#复盘异动'需要手动添加，方便快速定位添加元素简化操作

			for i in range(len(tempdata)):
				#读取本地txt模版，
				#数据写入txt
				#写入html
				#添加异动信号文字信息
				newtag = soup.new_tag('p')
				newtag.string=str(tempdata[i]).replace("[", "").replace("]", "").replace("'", "") 
				newtag['style'] = f'display: block; background-color: cyan; padding: 10px; text-decoration: none; color: black;'
				div_异动[0].append(newtag)


			temppath="help-center/"+tmpl
			path=pathlib.Path(__file__).absolute().parent/temppath #调试原来网址和保存分来，以后不用了
			with open(path,"w",encoding="utf-8" ) as f:
				f.write(str(soup.prettify()))			

			pass
		
		elif(ttype=='daily_dapan_notes'):


			with open(path,'rb') as file:
				html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
			div_异动=soup.find_all('div',attrs={'id':'复盘异动'})#复盘异动'需要手动添加，方便快速定位添加元素简化操作

			for i in range(len(tempdata)):
				#读取本地txt模版，
				#数据写入txt
				#写入html
				#添加异动信号文字信息
				newtag = soup.new_tag('p')
				newtag.string=str(tempdata[i]).replace("[", "").replace("]", "").replace("'", "") 	
				newtag['style'] = f'display: block; background-color: cyan; padding: 10px; text-decoration: none; color: black;'
				div_异动[0].append(newtag)


			temppath="help-center/"+tmpl
			path=pathlib.Path(__file__).absolute().parent/temppath #调试原来网址和保存分来，以后不用了
			with open(path,"w",encoding="utf-8" ) as f:
				f.write(str(soup.prettify()))			

			pass
		elif(ttype=='dynamic_monitor'):
			with open(path,'rb') as file:
				html = file.read()
			soup  = BeautifulSoup(html,'html.parser')
			div_异动=soup.find_all('div',attrs={'id':'复盘异动'})#复盘异动'需要手动添加，方便快速定位添加元素简化操作

			for i in range(len(tempdata)):
				#读取本地txt模版，
				#数据写入txt
				#写入html
				#添加异动信号文字信息
				newtag = soup.new_tag('p')
				newtag.string=str(tempdata[i][0]).replace("[", "").replace("]", "").replace("'", "") 
				newtag['style'] = f'display: block; background-color: cyan; padding: 10px; text-decoration: none; color: black;'
				div_异动[0].append(newtag)

				#添加链接
				# 使用new_tag创建一个'a'标签
				link_tag = soup.new_tag('a')
				# 设置链接地址
				link_tag['href'] = tempdata[i][1]
				#print(tempdata[i][1])
				# 添加文本内容
				link_tag.string = 'notelink'
				link_tag['target'] = "_blank" # 添加这一行来设置在新标签页中打开链接
				#设置这个<a>是高亮块

				div_异动[0].append(link_tag)

			temppath="help-center/"+tmpl
			#print(temppath)
			path=pathlib.Path(__file__).absolute().parent/temppath #调试原来网址和保存分来，以后不用了

			with open(path,"w",encoding="utf-8" ) as f:
				f.write(str(soup.prettify()))	

 
 

		else:
			print('error 123456')
			pass

		

	def deal_daily_notes(self):
		#
		#
		pass


	def notes_stocks(self,data,page_type,ttype='',isopenweb=0):
	#data默认是字典格式，特定notes格式
	#在需要写入笔记地方写调用笔记，网页内容自动添加保存，生成今日的笔记
	#而是异步来处理，这里不用考虑啥异步写文件，没有那么夸张啊，都是顺序执行的
	 
		# path=pathlib.Path(__file__).absolute().parent/'help-center/blocks.html'
		# with open(path,'rb') as file:
		# 	html = file.read()
		# soup  = BeautifulSoup(html,'html.parser')
		# #print(dir(soup))
		# #网页模版中默认给了一个div 和唯一id，方便查找，
		# 然后再dev-id中添加新元素作为div的子元素
		# #查找 是个结果列表，<div> <p>等都可能在里面，通过设置不同参数，来得到想要结果列表  https://blog.csdn.net/weixin_44015669/article/details/109603117
		# #div_复盘异动=soup.find_all(id='复盘异动')
		# div_复盘异动=soup.find_all('div',attrs={'id':'复盘异动'})#
		# #div_复盘异动=soup.find(id='复盘异动')#首个id==的元素
		# print(type(div_复盘异动))
		# print(div_复盘异动)
		# print(type(div_复盘异动[0]))
		# #删除原有元素
		# print(div_复盘异动[0])
		# print(dir(div_复盘异动[0]))
		# div_复盘异动[0].clear()#清除元素或清除内容text清除，不是tag
		# print(div_复盘异动[0])
		# #创建新元素
		# newtag = soup.new_tag('p')
		# newtag.string='TTTTTT'
		# #添加
		# div_复盘异动[0].append(newtag)
		# print(div_复盘异动[0])	 
		#div自我删除
		#div_复盘异动[0].decompose()  #删除div
		if(page_type==12):
				self.deal_html(data=data,ttype=ttype,tmpl='daily_notes.html')
		if(page_type==13):
			#print(ttype)
			self.deal_html(data=data,ttype=ttype,tmpl='dynamic_monitor.html')



		if(page_type==21):#异动信号
			self.deal_html(data=data,ttype="index",tmpl='index.html')
		if(page_type==22):#异动信号
			self.deal_html(data=data,ttype="blocks",tmpl='blocks.html')
		if(page_type==23):#异动信号
			self.deal_html(data=data,ttype="stocks",tmpl='stocks.html')
		if(page_type==24):
			self.deal_html(data=data,ttype="time",tmpl='timepoint.html')

		if(page_type==25):
			self.deal_html(data=data,ttype="emotional_cycle",tmpl='emotional_cycle.html')			


		if(isopenweb==1):
			# 用默认浏览器打开index
			webbrowser.open(pathlib.Path(__file__).absolute().parent/'main.html')


if __name__ == '__main__':
	webbrowser.open('main.html')

	#emotional cycle