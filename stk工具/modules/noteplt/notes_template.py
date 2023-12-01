
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




def deal_html(data,type,tmpl):

	if(type=="blocks"):
		tempdata=data['blocks']
		temppath="help-center/"+"tmpl_"+'blocks.html'#默认了，tmpl接口为了以后其他网址用，或修改用
		#temppath="help-center/"+"tmpl_"+tmpl
	elif(type=="index"):
		tempdata=data['index']
		temppath="help-center/"+"tmpl_"+'index.html'#默认了，tmpl接口为了以后其他网址用，或修改用
	elif(type=="stocks"):
		tempdata=data['stocks']
		temppath="help-center/"+"tmpl_"+'stocks.html'#默认了，tmpl接口为了以后其他网址用，或修改用

	path=pathlib.Path(__file__).absolute().parent/temppath#这个是模版
	#print(path)
	with open(path,'rb') as file:
		html = file.read()
		soup  = BeautifulSoup(html,'html.parser')
		#print(dir(soup))
	#网页模版中默认给了一个div 和唯一id，方便查找，
	#然后再dev-id中添加新元素作为div的子元素

	#查找 是个结果列表，<div> <p>等都可能在里面，通过设置不同参数，来得到想要结果列表  https://blog.csdn.net/weixin_44015669/article/details/109603117
	#div_复盘异动=soup.find_all(id='复盘异动')
	div_异动=soup.find_all('div',attrs={'id':'复盘异动'})#复盘异动'需要手动添加，方便快速定位添加元素简化操作
	#div_复盘异动=soup.find(id='复盘异动')#首个id==的元素
	#print(type(div_复盘异动))
	#print(div_复盘异动)
	#print(type(div_复盘异动[0]))
	#print(div_异动[0])
	#print(div_异动)
	
	#删除原有元素
	#print(dir(div_复盘异动[0]))
	div_异动[0].clear()#清除元素或清除内容text清除，不是tag
	#print(div_异动[0])
	#print(div_异动)

	for i in range(len(tempdata)):
		#添加异动信号文字信息
		newtag = soup.new_tag('p')
		newtag.string=tempdata[i][0]
		#div_板块异动[0].append(newtag)
		div_异动[0].append(newtag)
		#print(div_复盘异动[0])
		#添加链接
				# 使用new_tag创建一个'a'标签
		link_tag = soup.new_tag('a')
				# 设置链接地址
		link_tag['href'] = tempdata[i][1]
				# 添加文本内容
		link_tag.string = 'notelink'
				# 将链接标签添加到body标签中
		div_异动[0].append(link_tag)
	#div自我删除
	#div_复盘异动[0].decompose()  #删除div
	#另存为网页
	temppath="help-center/"+tmpl
	path=pathlib.Path(__file__).absolute().parent/temppath #调试原来网址和保存分来，以后不用了
	with open(path,"w",encoding="utf-8" ) as f:
		f.write(str(soup.prettify()))




def notes_stocks(data,page_type):#data默认是字典格式，特定notes格式
	
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
	 
	if(page_type==20):#异动信号
		deal_html(data=data,type="stocks",tmpl='stocks.html')
		deal_html(data=data,type="index",tmpl='index.html')
		deal_html(data=data,type="blocks",tmpl='blocks.html')
	# 用默认浏览器打开index
	webbrowser.open(pathlib.Path(__file__).absolute().parent/'main.html')


if __name__ == '__main__':
	notes_stocks()