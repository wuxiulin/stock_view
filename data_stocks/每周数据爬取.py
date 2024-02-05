#有些数据需要每日保存】
import sys
import os
import configparser
from datetime import datetime ,timedelta
import time
import akshare as ak
sys.path.append(os.path.dirname(os.path.abspath(__file__)) )
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) )))

from  数据保存.数据保存 import 数据保存类
from  数据爬取 import 股票代码映射
 
from  数据爬取.每周成交量 import 每周成交量类

from  common.TradingCalendar import  TradingCalendar类

class 每周数据爬取类( ):
	def __init__(self, GlobalCfg =None):

		self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
		self.conf = GlobalCfg

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
 

	def 每周更新(self,start=None,end=None):#start,end 这里不需要，因为接口只能爬取最近5天
 		#历史更新_指数_min()#五日接口，目前看是1min数据需要保存，以后再扩展看看需要保存哪些，


if __name__ == '__main__':

	todaynow = datetime.now().strftime('%Y%m%d')
	tradeday=TradingCalendar类().get_tradeday_from_day_pre(todaynow) 
 
	temp类=每周数据爬取类()
 
	temp类.每周更新() 
