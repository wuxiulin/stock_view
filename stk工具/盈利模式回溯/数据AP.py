from 买入 import 买入类
from 选股 import 选股类
from 卖出 import 卖出类
from 盈利 import 盈利类
import webbrowser
import re
import os,sys
import shutil
#数据分析和处理
#每个股的盈利已经计算了，这里就是怎么处理，
#处理盈利数据，处理个股那些取舍，等很多角度@@

# [{'600211': -1.6029}, {'600572': -3.5055}, {'603025': -2.1418}, {'603712': -1.3699}, {'600713': -2.0833}, 
# {'600080': -3.2746}, {'600168': -2.0802}, {'600192': 1.1628}, {'600321': 0.0}, {'600505': 2.518}, {'600714': -0.9278},
#  {'600725': 10.0559}, {'600834': -0.5931}, {'601177': -0.7187}, {'603011': 1.3532}, {'603045': 0.0651}, {'603088': -0.9569},
#   {'603268': -0.4077}, {'603963': -2.1904}, {'605162': -0.9474}, {'600860': -2.7737}, {'688071': -4.8727}, {'688215': 0.0563}, 
#   {'688676': -1.6228}, {'688331': -3.223}, {'002112': -1.0711}, {'002462': -2.1828}, {'002788': -1.5317}, {'002923': -1.3699},
#    {'003033': -3.763}, {'002046': -2.0134}, {'002424': -2.515}, {'002542': -1.0345}, {'002739': 1.8045}, {'000099': 0.0},
#     {'000544': -0.1401}, {'000566': -2.4845}, {'000813': -2.0468}, {'000989': -3.4884}, {'300099': -0.8013}, 
#     {'300147': -1.7699}, {'300193': -0.3886}, {'300237': -0.4739}, {'300421': -0.6006}, {'300439': -1.1765}, 
#     {'300483': -0.9709}, {'300222': -1.457}, {'301075': -1.953}, {'301130': -0.579}, {'301138': -0.9431}, 
#     {'301031': -1.5802}, {'603030': 0.7143}]

#考虑用不同新模版展示数据，所以需要确定用那种模版
##

class 数据AP类(object):
	"""docstring for 数据分理"""
	def __init__(self):
		pass
		self.收益day=''
		#self.tplt1_path = './tplt1/'#当下目录的./tplt1/ 是模板位置  通过输入决定
		#self.html_tplt1_path='./html_tplt1/'#通过tplt1生成的目标文件
		#./tplt1/mac.html
		# 每个图表最多是三条曲线，这里可以增加，每个图表的都是类似样式，就是各个图表第一条都是散点，第二条都是折线等，都是相同
		# 通过每个图表数据，为空，来对齐想要的样式，就是说此处大量增加每个图表的能容纳的条数。然后每个条是不同的类型，多样话曲线类似
		# 然后每个图表使用哪个通过调整数据先后和或用空来代替，跳过某个类型来使用后面的某个类型。
	def 数据重构(self,src_type=1,des_type=1,data=[]):#data 种类或者来源是src_type，然后生成格式是des_type
	#获取特定数据后要使用特定格式来展示，需要根据展示模板，重构数据结构
		#这里需要不断维护的地方，来实现其他代码的通用性
		if(src_type==1):#data 来自 src_type=盈利类().get_盈利涨幅()
		#[{'600211': -1.6}, {'600572': -3.51}, {'603025': -2.14}]
			if(des_type==1):#目标是  散点图_tplt1
			#   cp = 
			# 	[
			# 	   {
			# 	        "name": "指数",
			# 	        "data": 
			# 	           [
			# 	                    ["2023-01", 3255.67],
			# 	                    ["2023-02", 3279.61],
			#			   ]
			#      },
			#   //......同一个图里多条曲线数据
			#   ]
			#
				linedata_meta=[]# ["2023-01", 3255.67]
				linedata=[]#[ ["2023-01", 3255.67],["2023-02", 3279.61], ]
				linename=''#  "指数"
				line={}#一条曲线数据{"name":xx,'data':xxxx}
				chart=[]#一个图表，多个line 
				
				#一个图表数据
				linedata1=[]
				for i in range(len(data)):
					zf=list(data[i].values())[0]#取出值-3.51 {'600572': -3.51}
					linedata_meta1=[i,zf]#曲线一个点的横坐标和纵坐标
					linedata1.append(linedata_meta1)
				linename1='涨跌幅'
				line1={'name':linename1,'data':linedata1}#一条曲线数据

				chart1=[]
				chart1.append(line1)##一个图表
			if(des_type==2):
				linedata=[]
				for i in range(len(data)):
					zf=list(data[i].values())[0]
					linedata.append(zf)
				return linedata


		return  chart1



		
		#	
	################数据展示
	################数据展示
	def 有问题以后再写_散点图_tplt1(self,data,datatile=[],data_series=[],templt_name='./tplt1/mac.html',desname='./html_tplt1/mac.html',isopenweb=1):
		#问题是不该这样复制拼凑，有问题，而是其他方式
		#数据组织不应该在这里，提高代码通用性，所以data就是想要的数据
		#图表数据data，
		#每个需要的数据格式
		# var cp = 
		# 	[
		# 	   {
		# 	      "name": "指数",
		# 	      "data": 
		# 	      [
		# 	        ["2023-01", 3255.67],["2023-02", 3279.61],["2023-03", 3272.86],         
		# 	      ]
		# 	  },
		#	  {},#同表格其他曲线数据
		#     {},#同表格其他曲线数据
		# 	]


		#复制模板的static文件到目标文件夹
		if(not os.path.exists(templt_name )):#模板文件不存在
			print(templt_name,"   不存在" )
			return None

		if(len(data)<=0):
			print('散点图_tplt1 data为空')
			return
		elif(len(data)>3):
			print("目前js文件是三条，有空在修改js文件代码要添加")

		#获取模板文件路径
		templt_abspath=os.path.abspath(templt_name)#绝对路径
		templt_absdir=os.path.dirname(templt_abspath)
		des_abspath=os.path.abspath(desname)#绝对路径
		des_absdir=os.path.dirname(des_abspath)#目标文件存放的文件夹  #./html_tplt1/

		temp_src=os.path.join(templt_absdir,'static')##默认模板配置都在模板文件的static文件夹中，以后规范都是这样
		temp_des=os.path.join(des_absdir,'static') 
		if(os.path.exists( temp_src )):
			#static文件夹复制到des文件夹中
			try:
				shutil.copytree(temp_src, temp_des)#递归创建des_absdir所有缺失的文件夹
			except Exception as e:
				print('[WinError 183] 当文件已存在时,这里做删除之前文件，重新复制')
				shutil.rmtree(temp_des)#z注意这里的处理方式
				shutil.copytree(temp_src, temp_des)

				#raise e

			#复制模板文件
			des_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(templt_abspath))
			#print(des_tplt_abspath)
			shutil.copy(templt_abspath,des_tplt_abspath)#存在就覆盖
		else:
			if(os.path.exists(des_absdir)):
				shutil.rmtree(des_absdir)
			os.makedirs(os.path.dirname(desname), exist_ok=True)
			des_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(templt_abspath))
			#print(des_tplt_abspath)
			shutil.copy(templt_abspath,des_tplt_abspath)#存在就覆盖

		#这样，模板基本内容都复制到目的地了
		#那么针对目标文件夹中文件操作就好了

		#mac.html中的 ['cp', 'mm', 'zbj', 'interest']变量  决定图表个数 ，cp的元素个数决定曲线数，元素内容是坐标数据构成
		#cp的每条曲线的样式，在mac.v1.js中的series 是对应位置决定选择
		#这里注意的是由于模板原因，不同图表的第i条曲线，都是相同格式，这个关联性取消，以后再说！
		#所以需要根据data个数确认图表个数，然后data_series是对样式，缺失的用默认来填补

		num_charts=len(data)#图表数
		#确认图表数据name
		names_charts=[]
		for i in range(num_charts):
			names_charts.append('chat'+str(i))#类似['cp', 'mm', 'zbj', 'interest']
		#图表标题检查
		if( num_charts < len(datatile)):
			print('数据标题不对等')
			datatile=datatile[:num_charts]
		elif( num_charts > len(datatile)):
			print('数据标题不对等')
			datatile=datatile+['无标题']*(num_charts - len(datatile))

		for idt in data:
			#idt  字典
			for iidt in idt['data']:
				#iidt  [0, -1.6]
				pass

			prnit(idt)
			tempstr=''' 
			{
				"name": "{}",
				"data":

			}
			 '''

		return

		#得到格式化变量和对应数据
		charts_names_data=['var {} =[ {} ] '.format(iname, str(idata)) for i in range(num_charts) for iname, idata in zip(names_charts, data)]

		str_charts_names_data='\n'.join(charts_names_data)

		#data_series类似如下格式
		#  [
		# 			{
		# 	            name: data1.name,
		# 	            type: 'scatter',
		# 	            data: data1.data,
		# 	            stack: 'data1',
		# 	            showAllSymbol: false,
		# 	            color: color.lineColor[0]
		#        		 },
		#	     //.........下一条曲线格式设置
  		#      	 ]
		if(0):#这里曲线格式 先不搞，js文件，有待怪，以后再说吧
			num_input_style=len(data_series)#一个图表曲线数
	  		#所有图表中，一个图表含有的曲线最大条数
			max_num_chartlines=max([len(idata) for idata in data ])
			if(num_input_style > max_num_chartlines):#输入格式数量 大于数据
				print('输入格式有多余，是格式和曲线对其有问题，要么曲线数少，要么格式重复多余，检查一下')
	  			#这里可以做处理，可以返回
	  			#return
	  			#处理方式就是截断，用前面样式
				data_series=data_series[:max_num_chartlines]
			else:#输入格式数量小于数据，有些用默认就好，就是后面曲线用默认，
			#默认格式
				#data1这里肯定要改的，default_style_line是字符串，不是字典，
				default_style_line='''{
						name: data1.name,
						type: 'scatter',
						data: data1.data,
						stack: 'data1',
						showAllSymbol: false,
						color: color.lineColor[0]
				 	}'''
				data_series=data_series+[default_style_line]*(max_num_chartlines-num_input_style)
			str_data_series=str(data_series)
		#到这里图表数据和格式，都完成组建，构成字符串，之后写入html模板就行

		#js处理文件变量名字
		# $(function() {  // jQuery 的文档就绪事件，当页面完全加载完毕时执行其中的代码。在这里，它用于设置点击事件监听器。
		#     $('.v a').click(function() {  //当某个类为 'v' 下的 a 元素被点击时，会触发下列代码块：
		#         color.bgColor = color.bgColor == '#181d24' ? '#fff' : '#181d24'
		#         initChart('cpi_ppi', color, cp)
		#         initChart('m1_m2', color, mm)
		#         initChart('zbj', color, zbj)
		#         initChart('interest', color, interest)
		#     })
		#     color = {//在点击事件中，切换背景颜色（黑/白）后，分别调用 initChart 函数初始化四个图表
		#         'axisFontColor': '#666',
		#         'lineColor': ['#f06f6f', '#7eb2f3', '#fea31e']
		#     }
		#     initChart('cpi_ppi', color, cp)
		#     initChart('m1_m2', color, mm)
		#     initChart('zbj', color, zbj)
		#     initChart('interest', color, interest)
		# })
		js_vebs=''
		for i in range(num_charts):
			js_vebs=js_vebs+'''initChart('{}', color, {}) \n'''.format(datatile[i],names_charts[i])

		str_js_vebs='''
				$(function() {  // jQuery 的文档就绪事件，当页面完全加载完毕时执行其中的代码。在这里，它用于设置点击事件监听器。
		    $('.v a').click(function() {  //当某个类为 'v' 下的 a 元素被点击时，会触发下列代码块：
		        color.bgColor = color.bgColor == '#181d24' ? '#fff' : '#181d24'
		       %s
		    })
		    color = {//在点击事件中，切换背景颜色（黑/白）后，分别调用 initChart 函数初始化四个图表
		        'axisFontColor': '#666',
		        'lineColor': ['#f06f6f', '#7eb2f3', '#fea31e']
		    }
		   %s
		})'''%(js_vebs,js_vebs)





		#打开复制过来的本地的模板文件
		with open(des_tplt_abspath, "r",encoding="utf-8") as file:#des_tplt_abspath 复制过来的本地的模板文件
			html_content = file.read()
			#获取模板图表
			str_replace="//<!-- 数据替换地方、数据格式如下-->"
			if(str_replace in html_content ):
				html_content = html_content.replace(str_replace ,str_charts_names_data )

		#保存生成目标文件
		with open(desname, "w",encoding="utf-8") as file:
			file.write(html_content)	
		

		#修改js文件， 打开
		js_despath=os.path.join( des_absdir,'static\\js\\mac_v1.js')#复制过来的目标文件夹中的js
		print(js_despath)
		print(str_js_vebs)
		with open(js_despath, "r",encoding="utf-8") as file:#des_tplt_abspath 复制过来的本地的模板文件
			js_content = file.read()
			#获取模板图表
			str_replace='//<!-- 替换地方1数据格式如下-->'
			if(str_replace in js_content ):
				js_content = js_content.replace(str_replace ,str_js_vebs )

		print(js_content)
		#保存生成目标文件
		with open(js_despath, "w",encoding="utf-8") as file:
			file.write(js_content)


		#打开测试
		if(isopenweb==1):
			webbrowser.open(desname)#手动初步编辑一下 #不太好检测是否关闭网页，这里是直接执行退出没有阻塞	
	



	def html_格式化(self,src='./测试tplt/tplt_散点折线图.html',des='./测试tplt/tplt_tplt_散点折线图.html'):
		with open(src, "r",encoding="utf-8") as file:#des_tplt_abspath 复制过来的本地的模板文件
			html_content = file.read()
			#替换所有{}为{{}}
			html_content=html_content.replace('{', '{{')
			html_content=html_content.replace('}', '}}')
		with open(des, "w",encoding="utf-8") as file:
			file.write(html_content)



	def 散点图(self,data,datatile=[],data_series=[],templt_name='./tplt/散点折线图.html',desname='./测试tplt/散点折线图.html',openweb=1,init=1):

		#init=1 删除目标文件夹，重新开始
		#数据组织不应该在这里，提高代码通用性，所以data就是想要的数据
		#图表数据data，
		#每个需要的数据格式
                    #  data: [
                    #     { x: 1, y: 10 },
                    #     { x: 2, y: 20 },
                    #     { x: 3, y: 15 },
                    #     { x: 4, y: 25 },
                    #     { x: 5, y: 30 }
                    # ]

		#复制模板的static文件到目标文件夹
		if(not os.path.exists(templt_name )):#模板文件不存在
			print(templt_name,"   不存在" )
			return None

		# if(len(data)<=0):
		# 	print('散点图_tplt1 data为空')
		# 	return


		#获取模板文件路径
		templt_abspath=os.path.abspath(templt_name)#绝对路径
		templt_absdir=os.path.dirname(templt_abspath)

		des_abspath=os.path.abspath(desname)#绝对路径
		des_absdir=os.path.dirname(des_abspath)#目标文件存放的文件夹   

		while True:	#循环目的是init==0，但是缺少文件，所以重置init==1
			if(init==1):#目标文件夹删除后重建
				if(os.path.exists(des_absdir)):
					shutil.rmtree(des_absdir)
				
				static_file_src=os.path.join(templt_absdir,'static')##默认模板配置都在模板文件的static文件夹中，以后规范都是这样
				static_file_des=os.path.join(des_absdir,'static') 
				if(os.path.exists( static_file_src )):#模板文件夹中有static文件夹复制到des文件夹中
					try:
						shutil.copytree(static_file_src, static_file_des)#递归创建des_absdir所有缺失的文件夹
					except Exception as e:
						print('[WinError 183] 当文件已存在时,这里做删除之前文件，重新复制')
						shutil.rmtree(static_file_des)#z注意这里的处理方式
						shutil.copytree(static_file_src, static_file_des)
						#复制模板文件
						des_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(templt_abspath))
						#print(des_tplt_abspath)
						shutil.copy(templt_abspath,des_tplt_abspath)#存在就覆盖
				else:
					#前面删除目标文件了，这里直接创建
					os.makedirs(des_absdir, exist_ok=True)
					des_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(templt_abspath))
					#print(des_tplt_abspath)
					shutil.copy(templt_abspath,des_tplt_abspath)#存在就覆盖

				des_tplt_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(des_tplt_abspath))
				#print(des_tplt_tplt_abspath)
				self.html_格式化(src=des_tplt_abspath,des= des_tplt_tplt_abspath)
				break
			else:#
				#用之前的tplt_html就可以
				des_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(templt_abspath))
				des_tplt_tplt_abspath=os.path.join(des_absdir,"tplt_"+os.path.basename(des_tplt_abspath))
				if(os.path.exists( des_tplt_tplt_abspath )):
					break
				elif(init==0):#不存在就是删除了文件，init又是0
					init=1
					continue
				else:
					print('error 检查')
					break
 

        #有完整数据可以显示的作为模板，不要做修改，就是从网站爬取的初始版本，可能有static的文件
        #复制html和static文件夹到到目标文件夹，改名字为tplt_html,
        #读取tplt_html，python处理中每个{}换成 {{  }}
        #保存为tplt_tplt_html  #这里不能展示数据了
        #打开tplt_tplt_html，手动修改其中要替换部分为{}，保存，不用另取名字了
 		#写python，准备格式化data 替换内容{}代替
 		#然后读取tplt_tplt_html   然后file.format(data1，data2) 
 		#保存file到xxxdes.html完成，这里看结果html源码对不对！
		#print(data)
		# 将数据格式化成 JavaScript 数组字符串
		data_string = ', '.join([f'{{ x: {item[0]}, y: {item[1]} }}' for item in zip(range(len(data)),data)])
		#print(data_string)
 

		# # 替换 HTML 模板中的数据
		with open(des_tplt_tplt_abspath, "r",encoding="utf-8") as file:#des_tplt_abspath 复制过来的本地的模板文件
			html_content = file.read()
			if('{}' in html_content):
				formatted_html = html_content.format(data_string)
			else:
				print(" 手动修改替换内容为{} 并设置init=0")
				return 


		#保存生成目标文件
		with open(des_abspath, "w",encoding="utf-8") as file:
			file.write(formatted_html)

		#打开测试
		if(openweb==1):
			webbrowser.open(des_abspath)#手动初步编辑一下 #不太好检测是否关闭网页，这里是直接执行退出没有阻塞		


if __name__ == '__main__':
	#如下是某一天，通过均线突破，选股，买入，卖出，计算盈利，得到个股盈利 散点图
	a=选股类()
	a.均线突破_wencai(period='D',choseday='20231213',ma='250',srhtxt='去掉北交所')

	b=买入类()
	b.买入成本(T=1,Buytype=1,chose类=a)

	#print(b.get_买入价格())
	#print(b.get_买入时间())

	c=卖出类()
	c.卖出价格(T=1,Selltype=1,buy类=b)	#这里是为了传递买入的成本和时间等信息

	#print(c.get_卖出价格())
	#print(c.get_卖出时间())
	
	d=盈利类()
	d.盈利计算(buy类= b ,sell类= c,profittype=1)

	dd=d.get_盈利涨幅()
	#print(d.get_盈利涨幅())
	#print(dd)

	#组织数据，然后展示图表，这里是需要手动选择
	e=数据AP类()
	ee=e.数据重构(src_type=1,des_type=2,data=dd)
	print(ee)
	# ee=[]
	e.散点图(data=ee,init=0,templt_name='./tplt/散点折线图.html',desname='./测试tplt/'+c.get_卖出时间()+'散点折线图.html')