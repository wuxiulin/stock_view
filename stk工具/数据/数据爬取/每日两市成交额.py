#akshare可以直接获取，但是需要计算，为了加快执行代码速度，和方便，这里保存在本地
#更新数据方式：这里每天都用，所以日更新，
#因为能一次获取全部，所以不用特殊处理，直接全部爬取后都写入，不用专门爬取某一天的


import numpy as np
import   pywencai
import os,sys
import  json
from  datetime import datetime
import akshare as ak
import webbrowser
from jinja2 import Template

class 每日两市成交额类( ):
 
	def __init__(self):
		pass

	def crawl_day_每日两市成交额_ak(self,tradeday):
		trade_df=list(ak.stock_zh_index_daily_em(symbol="sh000001")['date'])
		trade_df=[d[:4]+d[5:7]+d[8:] for d in trade_df]#时间类型不对，转换
		lastindex= trade_df.index(tradeday)
		try:
			df=ak.stock_zh_index_daily_em(symbol="sh000001")
			trade_df=[d[:4]+d[5:7]+d[8:] for d in list(df['date'])]#时间类型不对，转换
			lastindex= trade_df.index(tradeday)
			amount1 = df['amount'][lastindex]/100000000
			
			df=ak.stock_zh_index_daily_em(symbol="sz399001")
			trade_df=[d[:4]+d[5:7]+d[8:] for d in list(df['date'])]#时间类型不对，转换
			lastindex= trade_df.index(tradeday)			
			amount2 = df['amount'][lastindex]/100000000
		except Exception as e:
			raise e
		return int(amount1)+int(amount2)

	def crawl_每日两市成交额_ak(self):
		trade_df=list(ak.stock_zh_index_daily_em(symbol="sh000001")['date'])
		trade_df=[d[:4]+d[5:7]+d[8:] for d in trade_df]#时间类型不对，转换
		try:
			df=ak.stock_zh_index_daily_em(symbol="sh000001")
			amount1=df['amount']/100000000
			amount2=ak.stock_zh_index_daily_em(symbol="sz399001")['amount']/100000000			
			
			minlen=min(len(amount1),len(amount2))
			amount1=list(amount1[-minlen:])
			amount2=list(amount2[-minlen:])
			
			amount =[int(i+j) for i,j in zip(amount1,amount2)]
			
			tradedays=list(df['date'][-minlen:])
			tradedays=[d[:4]+d[5:7]+d[8:] for d in tradedays]

			result = {day:at for day,at in zip(tradedays,amount)}
		except Exception as e:
			raise e

		return result

if __name__ == '__main__':
	a=每日两市成交额类().crawl_每日两市成交额_ak()
	print(a)


