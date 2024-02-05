#【历史数据爬取】 
#1、是为了集中爬取历史一级数据，保存数据到本地，，如果没有及时日更周期更新，通过这里模块补全。
#2、是为了爬取历史数据后，绘图，研究规律，然后计算阈值，这是最主要的
#3、不是所有数据都需要保存在本地，有时候是为了研究而爬取，保存本地，方便下一次研究，因为爬取时间有的太久了
#4、历史数据爬取，应该调用每日数据爬接口，接口做成一样的，如果不是，那么就是放在其他周期更新，不是日更新数据


import sys
import os
import configparser
from datetime import datetime ,timedelta
import time
import akshare as ak
import json
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
 

sys.path.append(os.path.dirname(os.path.abspath(__file__)) )
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) )))

from  common.TradingCalendar import  TradingCalendar类
from  数据保存.数据保存       import 数据保存类  
from  数据爬取.股票代码映射   import 股票代码映射类
from  数据爬取.爬取方式       import 爬取方式类 
from  数据爬取.每日同花顺板块 import 每日同花顺板块类

class 历史一级数据爬取类( ):
	def __init__(self, GlobalCfg =None):
		self.conf = GlobalCfg
		self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
		self.cfgpath_local= os.path.join( self.current_dir , '配置文件.cfg')
		if not os.path.exists(self.cfgpath_local):
			# 如果配置文件不存在，创建一个空的配置文件
			with open(self.cfgpath_local, 'w'):
				pass
			print('配置文件没有配置')
			return	

    	# 读取配置文件，最新更新日期，不要重复爬取
		self.conf_local = configparser.ConfigParser()
		self.conf_local.read(self.cfgpath_local, encoding='utf-8')

		self.root_path=self.conf_local.get('path','root_path')
		self.cfgpath_global=self.conf_local.get('path','cfg_path')
		self.conf_global=configparser.ConfigParser()
		self.conf_global.read(self.cfgpath_global,encoding='utf-8')



 
	def 历史更新_每日同花顺二级行业_资金流向(self,start='20210801',end=None):	
		#默认从20210101更新到当下，
		#看已经保存的日期，不用使用默认，而是看需要补漏的时间段
		#已经日更，但是可能没有执行，所以有遗漏，可通过start，end来设置补数据
		if end is None or end == '':
			end=TradingCalendar类().get_tradeday_from_today() #
			if end is None:
				print('end 设置错误')
				return None
		days=TradingCalendar类().get_tradeday_from_start_end(start=start,end=end) 
		if days is  None or len(days)==0 :
			print('爬取时间为空')
			return None
		print('更新时间为： ',days[0],days[-1])
		
		file_dir=self.conf_global.get('每日同花顺二级行业板块', '数据保存路径')
		for day in days:
			print(day)
			file_path=os.path.join(self.root_path,file_dir,'资金流向/day/{}.json'.format(day))
			#判断是否存在
			if(os.path.exists(file_path)):
				print(f'%s 今日已经爬取'%file_path)
				continue
			#爬取数据
			data=每日同花顺板块类().crawl_每日同花顺二级行业_资金流向_day(tradeday=day)
			if(data is None or len(data)==0):
				print('爬取数据为空')
				continue
			#print(data)
			#保存数据 按照行把df保存为json
			数据保存类().save_to_json(data=data.to_json(orient='records'),file_path=file_path)
			#读取为df方式   df = pd.read_json(json_filename, orient='records')
			print(f'%s 爬取完成'%file_path)

	def 历史更新_指数_min(self,start,end,period="1",symbols=["000001",'399001']):
		#目前接口只提供五日历史数据，所以如果长时间不执行日更新或周更新，目前接口无法补全历史数据，所以注意更新数据周期
		#这里是废弃不用的接口，因为历史数据太少了，且找到通过同花顺量化平台获取的方法了
		days=TradingCalendar类().get_tradeday_from_start_end(start=start,end=end) 
		if days is  None or len(days)==0 :
			print('爬取时间为空')
			return None
		print('更新时间为： ',days[0],days[-1])
		file_dir=self.conf_global.get('每日指数', '数据保存路径')
		for day in days:
			print(day)
			for symbol in symbols:
				file_path=os.path.join(self.root_path,file_dir,symbol,period+'min','{}.json'.format(day))
				#判断是否存在
				if(os.path.exists(file_path)):
					print(f'%s 今日已经爬取'%file_path)
					continue
				#爬取数据
				start_ft=day[:4]+'-'+day[4:6]+'-'+day[6:]
				#目前接口提供只是最近5天的的数据,start太早没有意义
				data = ak.index_zh_a_hist_min_em(symbol=symbol, period=period, start_date=start_ft+" 09:15:00", end_date=start_ft+" 19:00:00")
				#print(data)
				if(data is None or len(data)==0):
					print('爬取数据为空')
					continue
				#print(data)
				#保存数据 按照行把df保存为json
				数据保存类().save_to_json(data=data.to_json(orient='records'),file_path=file_path)
				#读取为df方式   df = pd.read_json(json_filename, orient='records')
				print(f'%s 爬取完成'%file_path)


	def THS_SuperMind(self,src_filepath):
		#格式化处理函数
		#这里通过同花顺量化平台得到了txt数据，这里格式化处理一下，因为格式可能不一样所以需要微调
		#定制化，也就那么几种格式  
		#*********************************************
		'''
		2024-02-03 04:01:47INFOINFO :回测开始运行
		,2024-02-03 04:01:47INFO回测开始
		,2019-01-02 09:31:00INFO170842501
		,2019-01-03 09:31:00INFO147449400
		,2019-01-04 09:31:00INFO724953643
		,2024-02-02 09:31:00INFO1191042290
		,2024-02-03 04:01:55INFO回测结束
		'''

		with open(src_filepath,'r',encoding='utf-8') as file:
			content=file.read()
		content=content.replace('\n','')
		content=content.split(',')
		#print(content[0],content[1])
		content=content[2:-1]#去掉最前后结束文字
		#print(content[0])
		#content=[[item.split('INFO')[0][:10].replace('-',''),int(item.split('INFO')[1])]    for item in content ]
		#方便后面处理时间插入排序
		content = {item.split('INFO')[0][:10].replace('-',''):item.split('INFO')[1]    for item in content}
		return content



	def 历史更新_股价历史新低数_days(self,start,end):
		days=TradingCalendar类().get_tradeday_from_start_end(start=start,end=end) 
		if days is  None or len(days)==0 :
			print('爬取时间为空')
			return None
		print('更新时间为： ',days[0],days[-1])

		file_dir=self.conf_local.get('股价历史新低数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('股价历史新低数_字典'))
		#判断是否存在
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		#爬取数据
		pre_days=data.keys()
		for day in days:
			if day in pre_days:
				continue
			print(day)
			#没有用每日接口，因为很简单，
			df=爬取方式类().crawl_by_wencai(searchtxt=day+'历史新低',column_str=None,loop=True,query_type='stock')
			if df is None or len(df)==0:
				 data[day]=0
			else:
				data[day]=len(df)
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		keys=list(data.keys())#
		keys=sorted(keys)#重新排序时间，生成有序列表，方便图形化表格时候，读取数据直接按照时间展示
		data=[[day,data[day]] for day in keys]

		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('股价历史新低数_有序列表'))
 
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))
		return data




	def 历史更新_THS_SuperMind_days(self,keywds,src_filepath,names):
 		#一个文件多个数据,keywds和names对应，重复的通过[]*N

		#爬取数据
		temp_crawl_data=self.THS_SuperMind(src_filepath=src_filepath)	
		#print(temp_crawl_data)
		crawl_data= [{} for _ in range(len(keywds))]
		keys=temp_crawl_data.keys()
		for ikey  in keys :
			ivalue=temp_crawl_data[ikey].split(' ')
			#print(ivalue)
			for i in range(len(keywds)):
				crawl_data[i][ikey]=int(ivalue[i])
		#print(crawl_data)
		result=[]
		for i in range(len(keywds)):
			keywd=keywds[i]
			name=names[i]
			#通过同花顺的量化平台,执行策略，然后导出策略日志，得到想要的数据文件txt,然后对他格式化处理，获取历史数据
			file_dir=self.conf_local.get(keywd, '数据保存路径')
			file_path=os.path.join(self.root_path,file_dir,'{}_字典.json'.format(name))
			data=数据保存类().read_from_json(file_path=file_path)
			if(data is None):
				data={}
			data.update(crawl_data[i])#
			#print(data)
			#保存数据
			数据保存类().save_to_json(data=data,file_path=file_path)
			print(f'%s 爬取完成'%os.path.basename(file_path))

			keys=list(data.keys())
			keys=sorted(keys)#重新排序时间，生成有序列表，方便图形化表格时候，读取数据直接按照时间展示
			data=[[key,data[key]] for key in keys]
			file_path=os.path.join(self.root_path,file_dir,'{}_有序列表.json'.format(name))
			#保存数据
			数据保存类().save_to_json(data=data,file_path=file_path)
			print(f'%s 爬取完成'%os.path.basename(file_path))
			result=result+data
		
		return result



	def 折线(self,x,y):#临时看一下折线图，不同可视化了，
		plt.figure(figsize=(8, 6))
		plt.plot(x, y, marker='o', linestyle='-', color='b', label='Line 1',markersize=2,)
		plt.gcf().autofmt_xdate()# 格式化日期显示
		# 添加标题和标签
		plt.title('Time Series Line Chart')
		plt.xlabel('Date')
		plt.ylabel('Values')

		# 显示图例
		plt.legend()
		# 在每个点上显示数值
		for i, txt in enumerate(y):
			plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(0, 5), ha='center',fontsize=5)

		# 显示折线图
		plt.show()


	def 核密度(self,data):

		#data = np.random.randn(1000)
		# 使用 seaborn 画核密度图
		sns.histplot(data, kde=True, color="blue")
		#print(data)
		#temp=sorted(temp)
		#print(temp)
		#print('样本数:',len(data),' 阈值是 3,置信：',len(temp)/len(data))
		# 添加标签和标题
		plt.xlabel("X-axis Label")
		plt.ylabel("Density")
		plt.title("Kernel Density Plot")
		plt.show()

if __name__ == '__main__':
	tradeday=TradingCalendar类().get_tradeday_from_today() 
	print(tradeday)
#历史数据爬取，想要集中补全历史数据，理论上是所有历史数据，但是不一定能找到合适的接口，所以只能是尽可能补全，所以发现新接口替换就好了
#保存大量历史数据到本地是无奈选择，因为很多接口提供数据有限，所以只能日更新和周更新保存到本地。
#还有一个理由是，保存到本地，方便二次处理和统计计算阈值，更容易快速实现代码和快速方便查看统计数据,这里只要将大量数据放在硬盘，修改data_path
#可以是一次数据爬取，可以是二次，但是二次要先更新一次，所以做两个类，区分，目的是方便管理
#返回数据格式固定，方便后面画图表代码，但是有些需要处理，所以尽可能标准化就好
#图表展示，形象化，方便发现规律，然后针对性的计算阈值。所以图表在这里展示不要在阈值那里
	
	temp类=历史一级数据爬取类()

#request.get
	#temp类.历史更新_每日同花顺二级行业_资金流向(start='20210801',end=None)

#akshare
	#temp类.历史更新_指数_min(start='20240120',end=None)
	 

#同花顺量化
	#data=temp类.历史更新_THS_SuperMind_days(keywds=['沪深两市_成交量_min_xxxx'],names=['1301'],src_filepath='./thsSuperMind/13_00两市成交量.txt',)
	#data=temp类.历史更新_THS_SuperMind_days(keywds=['沪深两市_统计数_min_xxxx_涨跌幅_设定值'],names=['0935_负3_low减open'],src_filepath='./thsSuperMind/outlog1.txt')
	data=temp类.历史更新_THS_SuperMind_days(keywds=['沪深两市_统计数_min_xxxx_涨跌幅_设定值']*2,names=['0935_负3_low减open','0935_正3_high减open'],src_filepath='./thsSuperMind/5outlog.txt')
	#data=data[0]
#问财
	#data=temp类.历史更新_股价历史新低数_days(start='20240201',end='20240202')
	#data=[-100:]
	#print(data)
	if 1:#
		print('样本时间',data[0][0],data[-1][0])
		x=[]
		y=[]
		for value in data:
			y.append( value[1])
			#y.append( 跌停数)
			#y.append( 上涨数)
			#y.append( 下跌数)
			x.append(value[0])
		x = [datetime.strptime(date, '%Y%m%d') for date in x]
	 
		#temp类.折线(x=x,y=y)
		temp类.核密度(data=y)#是80%区间，