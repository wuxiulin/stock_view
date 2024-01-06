import akshare as ak
import sys,os
current_dir =os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(current_dir)
sys.path.append(current_dir)
from 获取各类数据函数 import  每日上证指数黄白线分钟数据
from 获取各类数据函数 import  每日同花顺二级行业板块分钟数据

import pywencai
from datetime import datetime
from jinja2 import Template
import webbrowser
import json
import time
import pandas as pd

class 复盘大盘分时_程序笔记类():
	def __init__(self):
		pass

	def get笔记_复盘大盘分时_day(self,tradeday):#data可以是黄白线数据，或者白线数据

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		data=每日上证指数黄白线分钟数据.上证指数黄白线分钟数据类().get_day_上证指数黄白线分钟数据(tradeday=tradeday)
		ydata=每日上证指数黄白线分钟数据.上证指数黄白线分钟数据类().get_day_上证指数黄白线分钟数据(tradeday=last_yetd_date_string)

		昨日收盘白=float(ydata[-1][1])
		昨日收盘黄=float(ydata[-1][3])
		#print(昨日收盘白)
		今日分时白=[ float(item[1])  for item in data]
		今日分时黄=[ float(item[3])  for item in data]


		#波动点数，波动振幅，这是是一个东西么？看点数波动，还是振幅波动，以后再说吧
		#data是黄白线数据，所以这里做一个处理
		#第一种是昨日收盘比较，比较
		#第二种是早盘(9:30比较开盘价比较（高开或低开后，可能一天波动很小）

		#第一种 白（波动点数，涨幅，振幅）  黄（波动点数，涨幅，振幅）
		result1白=[round(max(今日分时白)-min(今日分时白),2),round(100*今日分时白[-1]/昨日收盘白-100,2),round((max(今日分时白)-min(今日分时白))*100/昨日收盘白,2)]
		result1黄=[round(max(今日分时黄)-min(今日分时黄),2),round(100*今日分时黄[-1]/昨日收盘黄-100,2),round((max(今日分时黄)-min(今日分时黄))*100/昨日收盘黄,2)]

		#第二种 白（波动点数，涨幅，振幅）  黄（波动点数，涨幅，振幅）

		result2白=[round(max(今日分时白)-min(今日分时白),2),round(100*今日分时白[-1]/今日分时白[0]-100,2),round((max(今日分时白)-min(今日分时白))*100/今日分时白[0],2)]
		result2黄=[round(max(今日分时黄)-min(今日分时黄),2),round(100*今日分时黄[-1]/今日分时黄[0]-100,2),round((max(今日分时黄)-min(今日分时黄))*100/今日分时黄[0],2)]

		
		#print(result1白,result1黄,result2白,result2黄,(max(今日分时白)-min(今日分时白))/今日分时白[0])
		txt='今日上证指数波动{}点，涨幅{}%，振幅{}%;'.format(result1白[0],result1白[1],result1白[2])
		txt=txt+'情绪黄线波动{}点，涨幅{}%，振幅{}%；'.format(result1黄[0],result1黄[1],result1黄[2])
		txt=txt+'如果以今日9:30为基准，白线涨幅{}%，振幅{}%；黄线涨幅{}%，振幅{}%'.format(result2白[1],result2白[2],result2黄[1],result2黄[2])

		return txt
	def get_web(self):
		#不好量化，通过网页方式选择题，来得到

		#分时是否一路下滑，从开盘跌到收盘？如果是，情绪极端悲观，无护盘，影响很大一个关键点！风险思考点
		#
		pass


class 复盘大盘分时_手动复盘类():
	def __init__(self):
		pass
	def get_codes_上证非科创_对大盘分时影响大_精确(self,tradeday,cha=100):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = last_yetd_date_string+'流通值排序，流通股数，收盘价前复权，上证非科创，流通值大于40亿'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None
		#print(res.columns)
		col_昨日流通股数=[ col for col in res.columns  if '流通a股[' in col  and last_yetd_date_string in col][0]
		col_昨日收盘价 =[col for col in res.columns if  '收盘价:前复权[' in col and last_yetd_date_string in col][0]

		昨日数据=res.apply(lambda row: {row['code']: [row[col_昨日流通股数], row[col_昨日收盘价] ]}, axis=1).tolist()
		#print(昨日数据)
		dict昨日数据={}
		for item in 昨日数据:
			for key,value in item.items():
				dict昨日数据[key]=[float(value[0]),float(value[1])   ]

		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = tradeday+'最高价，最低价，涨跌幅，上证非科创，流通值大于50亿'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)	

		col_今日最高价=[ col for col in res.columns  if '最高价:前复权[' in col  and tradeday in col][0]
		col_今日最低价=[ col for col in res.columns  if '最低价:前复权[' in col  and tradeday in col][0]
		#col_今日涨跌幅=[ col for col in res.columns  if '涨跌幅:前复权[' in col  and tradeday in col][0]

		res今日= res.apply(lambda row: {row['code']: [row[col_今日最高价], row[col_今日最低价],row['股票简称'],row['股票代码']]}, axis=1).tolist()

		result增流通={}
		result减流通={}
		out=[]
		for item in  res今日:
			for key,value in item.items():

				#dict昨日数据[key][0]#昨日流通值
				#dict昨日数据[key][1]#昨日收盘价
				#value[0]##最高价
				#value[1]##最低价
				#增加流通值
				if float(value[0]) > dict昨日数据[key][1] :#最高价大于昨日收盘价
					tt=round((float(value[0]) - dict昨日数据[key][1])*dict昨日数据[key][0]/100000000,2)#最高价新增流通值
					if(tt>=cha):
						#result增流通[key]=tt
						out.append([value[3],value[2],key, tt])
				#减少流通值
				if float(value[1]) < dict昨日数据[key][1] :#最低价小于昨日收盘价
					tt=round((float(value[1]) - dict昨日数据[key][1])*dict昨日数据[key][0]/100000000,2)#最高价新增流通值
					if(tt<=-cha):
						#result减流通[key]=tt
						out.append([value[3],value[2],key, tt])
		#print(result增流通)
		#print(result减流通)


		# 按值排序字典
		# result增流通 = dict(sorted(result增流通.items(), key=lambda item: item[1],reverse=True))#降序
		# result减流通 = dict(sorted(result减流通.items(), key=lambda item: item[1],reverse=False))#升序
		# print(result增流通,result减流通)
		df=pd.DataFrame(out, columns=['股票代码','股票简称','code','流通值差'])
		df=df.drop_duplicates(subset='股票代码')
		return  df

	def get_codes_深圳非创业_对大盘分时影响大_精确(self,tradeday,cha=50):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = last_yetd_date_string+'流通值排序，流通股数，收盘价前复权，深圳非创业，流通值大于40亿'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None
		#print(res.columns)
		col_昨日流通股数=[ col for col in res.columns  if '流通a股[' in col  and last_yetd_date_string in col][0]
		col_昨日收盘价 =[col for col in res.columns if  '收盘价:前复权[' in col and last_yetd_date_string in col][0]

		昨日数据=res.apply(lambda row: {row['code']: [row[col_昨日流通股数], row[col_昨日收盘价] ]}, axis=1).tolist()
		#print(昨日数据)
		dict昨日数据={}
		for item in 昨日数据:
			for key,value in item.items():
				dict昨日数据[key]=[float(value[0]),float(value[1])   ]

		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = tradeday+'最高价，最低价，涨跌幅，深圳非创业，流通值大于50亿'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)	

		col_今日最高价=[ col for col in res.columns  if '最高价:前复权[' in col  and tradeday in col][0]
		col_今日最低价=[ col for col in res.columns  if '最低价:前复权[' in col  and tradeday in col][0]
		#col_今日涨跌幅=[ col for col in res.columns  if '涨跌幅:前复权[' in col  and tradeday in col][0]

		res今日= res.apply(lambda row: {row['code']: [row[col_今日最高价], row[col_今日最低价],row['股票简称'],row['股票代码']]}, axis=1).tolist()

		result增流通={}
		result减流通={}
		out=[]
		for item in  res今日:
			for key,value in item.items():

				#dict昨日数据[key][0]#昨日流通值
				#dict昨日数据[key][1]#昨日收盘价
				#value[0]##最高价
				#value[1]##最低价
				#增加流通值
				if float(value[0]) > dict昨日数据[key][1] :#最高价大于昨日收盘价
					tt=round((float(value[0]) - dict昨日数据[key][1])*dict昨日数据[key][0]/100000000,2)#最高价新增流通值
					if(tt>=cha):
						#result增流通[key]=tt
						out.append([value[3],value[2],key, tt])
				#减少流通值
				if float(value[1]) < dict昨日数据[key][1] :#最低价小于昨日收盘价
					tt=round((float(value[1]) - dict昨日数据[key][1])*dict昨日数据[key][0]/100000000,2)#最高价新增流通值
					if(tt<=-cha):
						#result减流通[key]=tt
						out.append([value[3],value[2],key, tt])
		#print(result增流通)
		#print(result减流通)


		# 按值排序字典
		# result增流通 = dict(sorted(result增流通.items(), key=lambda item: item[1],reverse=True))#降序
		# result减流通 = dict(sorted(result减流通.items(), key=lambda item: item[1],reverse=False))#升序
		# print(result增流通,result减流通)
		df=pd.DataFrame(out, columns=['股票代码','股票简称','code','流通值差'])
		df=df.drop_duplicates(subset='股票代码')
		return  df

	def get_codes_创业板_对大盘分时影响大_精确(self,tradeday,cha=30):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = last_yetd_date_string+'流通值排序，流通股数，收盘价前复权，创业板，流通值大于40亿'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None
		#print(res.columns)
		col_昨日流通股数=[ col for col in res.columns  if '流通a股[' in col  and last_yetd_date_string in col][0]
		col_昨日收盘价 =[col for col in res.columns if  '收盘价:前复权[' in col and last_yetd_date_string in col][0]

		昨日数据=res.apply(lambda row: {row['code']: [row[col_昨日流通股数], row[col_昨日收盘价] ]}, axis=1).tolist()
		#print(昨日数据)
		dict昨日数据={}
		for item in 昨日数据:
			for key,value in item.items():
				dict昨日数据[key]=[float(value[0]),float(value[1])   ]

		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = tradeday+'最高价，最低价，涨跌幅，创业板，流通值大于50亿'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)	

		col_今日最高价=[ col for col in res.columns  if '最高价:前复权[' in col  and tradeday in col][0]
		col_今日最低价=[ col for col in res.columns  if '最低价:前复权[' in col  and tradeday in col][0]
		#col_今日涨跌幅=[ col for col in res.columns  if '涨跌幅:前复权[' in col  and tradeday in col][0]

		res今日= res.apply(lambda row: {row['code']: [row[col_今日最高价], row[col_今日最低价],row['股票简称'],row['股票代码']]}, axis=1).tolist()

		result增流通={}
		result减流通={}
		out=[]
		for item in  res今日:
			for key,value in item.items():

				#dict昨日数据[key][0]#昨日流通值
				#dict昨日数据[key][1]#昨日收盘价
				#value[0]##最高价
				#value[1]##最低价
				#增加流通值
				if float(value[0]) > dict昨日数据[key][1] :#最高价大于昨日收盘价
					tt=round((float(value[0]) - dict昨日数据[key][1])*dict昨日数据[key][0]/100000000,2)#最高价新增流通值
					if(tt>=cha):
						#result增流通[key]=tt
						out.append([value[3],value[2],key, tt])
				#减少流通值
				if float(value[1]) < dict昨日数据[key][1] :#最低价小于昨日收盘价
					tt=round((float(value[1]) - dict昨日数据[key][1])*dict昨日数据[key][0]/100000000,2)#最高价新增流通值
					if(tt<=-cha):
						#result减流通[key]=tt
						out.append([value[3],value[2],key, tt])
		#print(result增流通)
		#print(result减流通)


		# 按值排序字典
		# result增流通 = dict(sorted(result增流通.items(), key=lambda item: item[1],reverse=True))#降序
		# result减流通 = dict(sorted(result减流通.items(), key=lambda item: item[1],reverse=False))#升序
		# print(result增流通,result减流通)
		df=pd.DataFrame(out, columns=['股票代码','股票简称','code','流通值差'])
		df=df.drop_duplicates(subset='股票代码')
		return  df





	def get_codes_对上证指数分时影响大(self,tradeday,cha=100):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = '{}流通市值,{}流通市值,上证非科创，去掉流通值小于100亿'.format(last_yetd_date_string,tradeday)
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None

		#print(res)
		#print(res.columns)
		col_昨日流通值=[ col for col in res.columns  if 'a股市值(不含限售股)[' in col  and last_yetd_date_string in col][0]
		col_今日流通值=[ col for col in res.columns  if 'a股市值(不含限售股)[' in col  and tradeday in col][0]
		res['流通值差']=(res[col_今日流通值]-res[col_昨日流通值])/100000000
		res=res[(res['流通值差'] > cha) | (res['流通值差'] < -cha)]#选择-100亿和100亿之外的数据
		df_sorted = res.sort_values(by='流通值差').reset_index(drop=True)
		df_sorted=df_sorted[['股票代码','股票简称','code','流通值差']]
		#print(df_sorted)
		#选择阈值，去掉，然后只看核心权重，得到值最大影响度，收盘不一定有这么大影响！只是选出来观察！
		return df_sorted

	def get_codes_对深圳成指分时影响大(self,tradeday,cha=50):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = '{}流通市值,{}流通市值,深圳非创业板，去掉流通值小于100亿'.format(last_yetd_date_string,tradeday)
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None

		#print(res)
		#print(res.columns)
		col_昨日流通值=[ col for col in res.columns  if 'a股市值(不含限售股)[' in col  and last_yetd_date_string in col][0]
		col_今日流通值=[ col for col in res.columns  if 'a股市值(不含限售股)[' in col  and tradeday in col][0]
		res['流通值差']=(res[col_今日流通值]-res[col_昨日流通值])/100000000
		#print(res)
		res=res[(res['流通值差'] > cha) | (res['流通值差'] < -cha)]#选择-100亿和100亿之外的数据
		df_sorted = res.sort_values(by='流通值差').reset_index(drop=True)
		df_sorted=df_sorted[['股票代码','股票简称','code','流通值差']]
		#print(df_sorted)
		#选择阈值，去掉，然后只看核心权重，得到值最大影响度，收盘不一定有这么大影响！只是选出来观察！
		return df_sorted
	def get_codes_对创业板分时影响大(self,tradeday,cha=30):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = '{}流通市值,{}流通市值,创业板，去掉流通值小于100亿'.format(last_yetd_date_string,tradeday)
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None

		#print(res)
		#print(res.columns)
		col_昨日流通值=[ col for col in res.columns  if 'a股市值(不含限售股)[' in col  and last_yetd_date_string in col][0]
		col_今日流通值=[ col for col in res.columns  if 'a股市值(不含限售股)[' in col  and tradeday in col][0]
		res['流通值差']=(res[col_今日流通值]-res[col_昨日流通值])/100000000
		#print(res)
		res=res[(res['流通值差'] > cha) | (res['流通值差'] < -cha)]#选择-100亿和100亿之外的数据
		df_sorted = res.sort_values(by='流通值差').reset_index(drop=True)
		df_sorted=df_sorted[['股票代码','股票简称','code','流通值差']]
		#print(df_sorted)
		return df_sorted
		#选择阈值，去掉，然后只看核心权重，得到值最大影响度，收盘不一定有这么大影响！只是选出来观察！

	def get_blocks_stocks_分时(self,tradeday='20231229'):

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换

		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
 
		#print(last_yetd_date_string)#最近交易日


		#按照板块来
		result={}
 
		
		# df=self.get_codes_对上证指数分时影响大(tradeday=tradeday)
		# result['上证']=df[['code', '股票简称']].to_numpy().tolist()

		# df=self.get_codes_对深圳成指分时影响大(tradeday=tradeday)
		# result['深圳']=df[['code', '股票简称']].to_numpy().tolist()
		
		# df=self.get_codes_对创业板分时影响大(tradeday=tradeday)
		# result['创业']=df[['code', '股票简称']].to_numpy().tolist()
		df=self.get_codes_上证非科创_对大盘分时影响大_精确(tradeday='20240103')
		result['上证']=df[['code', '股票简称']].to_numpy().tolist()
		#print(a)
		df=self.get_codes_深圳非创业_对大盘分时影响大_精确(tradeday='20240103')
		#print(a)
		result['深圳']=df[['code', '股票简称']].to_numpy().tolist()
		df=self.get_codes_创业板_对大盘分时影响大_精确(tradeday='20240103')
		#print(a)
		result['创业']=df[['code', '股票简称']].to_numpy().tolist()
		


		#print(result)
		day_ft=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]
		
		for blk ,codes in result.items():
			temp1={}
			for code in codes:
				#股票代码
				#不复权数据
				上个交易日收盘价格= ak.stock_zh_a_hist(symbol=code[0], period="daily", start_date=last_yetd_date_string, end_date=last_yetd_date_string, adjust="")['收盘'][0]
				#print(上个交易日收盘价格)
					# 注意：该接口返回的数据只有最近一个交易日的有开盘价，其他日期开盘价为 0。1min不复权
				stock_min_df = ak.stock_zh_a_hist_min_em(symbol=code[0], start_date=day_ft+" 09:30:00", end_date=day_ft+" 19:00:00", period='1', adjust='')
				#print(stock_min_df)
				#股价数据画图
				#selected_data=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(stock_min_df['时间'],stock_min_df['收盘'])  ]
				#涨幅画图
				selected_data=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,round(100*idata/上个交易日收盘价格-100,2)]   for idate,idata in zip(stock_min_df['时间'],stock_min_df['收盘'])  ]
				#print(selected_data)
				temp1[code[1]]=selected_data

			result[blk]=temp1

		#按照板块依次保存数据分时
		return result

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

	def get_chart_今日影响大权重分时叠加图(self,tradeday,iswebopen=0):
		#https://note.youdao.com/s/Ip6sVHtc
 		#测试模板案例1  ：   左侧是上证指数，右侧是某个板块核心股的分时图，
		tempday=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]

		index_codes={'上证':"000001",'深圳':'399001',"创业":'399006'}
		selected_index_data={}
		for key,code in index_codes.items():

	 		#上涨指数数据
			index_df = ak.index_zh_a_hist_min_em(symbol=code, period="1", start_date=tempday+" 09:30:00", end_date=tempday+" 19:00:00")
			#print(index_df['收盘'])
			selected_index_data[key]=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(index_df['时间'],index_df['收盘'])  ]
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
			dydata={ikey:[selected_index_data[ikey],左纵]}
			for iikey,iivalue in ivalue.items():
				print(iikey)
				dydata[iikey]=[iivalue,右纵]#每个股票的分时数据

			tempath= os.path.dirname(os.path.abspath(__file__))+ '/static/{}/{}_{}.html'.format(tradeday,tradeday,ikey)
			self.get_chart_html_template1(dydata,"无",iswebopen=iswebopen,des_html_path=tempath)
			time.sleep(5)
			dydata={}
		#生成html  



	def get_blks_对指数分时影响大(self,tradeday,cha=100):
		#思路是，大盘分时影响是通过流通值的增减影响，所以个股流通值变化反应对大盘潜在影响程度
		#所以如果最高价涨幅>0，那么最高价就是最大流通值增加情况，反映对大盘上涨影响最大
		#所以如果最低价涨幅<0, 那么最低价就是最大流通值减少情况，反映对大盘下跌影响最大
		#所以选出来流通值增加最大排序，减少排序，选出这些codes，就是今天对大盘分时影响巨大的票，看看这些票，然后不同的板块分类一下！就可以做笔记输出了！
		#不用盯着分析了，可以分时看，这里就是具体到每个min或者5min都是可以量化的角度了！比较复杂了！可以简化就是选出来stocks统计就好了看那些min或者5min影响大的票！
		
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日

		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = '同花顺二级行业指数,{}流通市值,{}流通市值'.format(last_yetd_date_string,tradeday)
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=True,query_type='zhishu')#测试'
		except Exception as e:
			print(e,"get_day_每日最高连板数   is error ") 
			return None
		#print(res)
		#print(res.columns)
		if(res is None or len(res)==0):
			print("get_day_每日最高连板数   is  none ") 
			return  None

		#print(res)
		#print(res.columns)
		col_昨日流通值='指数@流通市值[{}]'.format(last_yetd_date_string)
		col_今日流通值='指数@流通市值[{}]'.format(tradeday)
		res['流通值差']=(res[col_今日流通值]-res[col_昨日流通值])/100000000
		res=res[(res['流通值差'] > cha) | (res['流通值差'] < -cha)]#选择-100亿和100亿之外的数据
		df_sorted = res.sort_values(by='流通值差').reset_index(drop=True)
		df_sorted=df_sorted[['指数代码','指数简称','code','流通值差']]
		#print(df_sorted)
		# #选择阈值，去掉，然后只看核心权重，得到值最大影响度，收盘不一定有这么大影响！只是选出来观察！
		return df_sorted

	def get_blocks_分时(self,tradeday='20231229'):

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		last_yetd_date_string=trade_df[lastindex-1]
		#print(tradeday,last_yetd_date_string)#最近交易日


		result={}
		df=self.get_blks_对指数分时影响大(tradeday=tradeday,cha=100)
		result['ths二级行业']=df[['code', '指数简称']].to_numpy().tolist()
		
		day_ft=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]
		
		for typeblk ,codes in result.items():
			temp1={}
			for code in codes:
				#股票代码
				#不复权数据
				上个交易日收盘价格= ak.stock_board_industry_index_ths(symbol= code[1], start_date=last_yetd_date_string, end_date=last_yetd_date_string)['收盘价']
				上个交易日收盘价格=float(上个交易日收盘价格.iloc[0])
				#print(上个交易日收盘价格)
				
				stock_min_df = 每日同花顺二级行业板块分钟数据.每日同花顺二级行业板块分钟数据类().get_day_blk_同花顺二级行业板块分钟数据(tradeday=tradeday,blk=code[0])
				#print(stock_min_df)
				#print(type(stock_min_df))
				if(stock_min_df is None or len(stock_min_df)==0):
					print('有数据没有爬取下来')
					continue
				#stock_min_df=json.loads(stock_min_df)
				#股价数据画图
				#selected_data=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(stock_min_df['时间'],stock_min_df['收盘'])  ]
				#涨幅画图
				selected_data=[ [ (datetime.strptime(tradeday+' '+item[0], "%Y%m%d %H%M")).timestamp()*1000   ,round(100*float(item[1])/上个交易日收盘价格-100,2)]   for item in stock_min_df]
				#print(selected_data)
				temp1[code[1]]=selected_data

			result[typeblk]=temp1

		#按照板块依次保存数据分时
		return result


	def get_chart_今日影响大行业板块分时叠加图(self,tradeday,iswebopen=0):
		#https://note.youdao.com/s/Ip6sVHtc
 		#测试模板案例1  ：   左侧是上证指数，右侧是某个板块核心股的分时图，
		tempday=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]

		index_codes={'上证':"000001",'深圳':'399001',"创业":'399006'}
		selected_index_data={}
		for key,code in index_codes.items():

	 		#上涨指数数据
			index_df = ak.index_zh_a_hist_min_em(symbol=code, period="1", start_date=tempday+" 09:30:00", end_date=tempday+" 19:00:00")
			#print(index_df['收盘'])
			selected_index_data[key]=[ [ (datetime.strptime(idate, "%Y-%m-%d %H:%M:%S")).timestamp()*1000   ,idata]   for idate,idata in zip(index_df['时间'],index_df['收盘'])  ]
			#print(selected_index_data)
 
		#统计数据
		#个股分时图数据

		data=self.get_blocks_分时(tradeday=tradeday)
		#print(data)

		#格式化
		左纵=0
		右纵=1
		for ikey ,ivalue in data.items():
			print(ikey)#板块
			dydata={'上证':[selected_index_data['上证'],左纵]}
			for iikey,iivalue in ivalue.items():
				print(iikey)
				dydata[iikey]=[iivalue,右纵]#每个股票的分时数据

			tempath= os.path.dirname(os.path.abspath(__file__))+ '/static/{}/{}_{}.html'.format(tradeday,tradeday,ikey)
			self.get_chart_html_template1(dydata,"无",iswebopen=iswebopen,des_html_path=tempath)
			time.sleep(5)
			dydata={}


if __name__ == '__main__':
	#txt=复盘大盘分时类_程序笔记类().get笔记_复盘大盘分时_day(tradeday='20240103')
	#print(txt)
	复盘大盘分时_手动复盘类().get_chart_今日影响大权重分时叠加图(tradeday='20240104',iswebopen=1)
	#复盘大盘分时_手动复盘类().get_blocks_分时(tradeday='20240103')
	复盘大盘分时_手动复盘类().get_chart_今日影响大行业板块分时叠加图(tradeday='20240104',iswebopen=1)
