
#处理html虽然python自带html库，但是似乎不好用，主流是BeautifulSoup、urllib.requests
#似乎BeautifulSoup更好用

#读取指定html
#运行各种监控代码得到结论
#在html默认位置，根据结论添加文本
#输出保存html
import string
from bs4 import BeautifulSoup
import  pathlib
def notes_stocks():
	
	path=pathlib.Path(__file__).absolute().parent/'help-center/basic_normal.html'

	with open(path,'rb') as file:
		html = file.read()
	soup  = BeautifulSoup(html,'html.parser')

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
	 

	#另存为网页
	#print(str(soup.prettify()))
	path=pathlib.Path(__file__).absolute().parent/'help-center/1basic_normal.html' #调试原来网址和保存分来，以后不用了
	with open(path,"w",encoding="utf-8" ) as f:
	   f.write(str(soup.prettify()))
	


if __name__ == '__main__':
	notes_stocks()