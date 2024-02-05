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
 
from  数据爬取.个股 import 个股类  


from  common.TradingCalendar import  TradingCalendar类

class 每月数据爬取类( ):
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


	def 每月更新_地量_codes(self,start,end,set百分比=0.2,):
		#每月更新一次，爬取个股历史数据，统计得到地量指标，作为阈值使用
		#只需要保存阈值，不需要保存个股成交量
		if (datetime.strptime(end,"%Y%m%d") - datetime.strptime(start,"%Y%m%d")).days >1000:
			print('start时间太久，个股配股等导致数据不正确，最好是近两年统计')
			return None
		if (datetime.strptime(end,"%Y%m%d") - datetime.strptime(start,"%Y%m%d")).days <100:
			print('start时间太短，结果意义不大')
			return None
		roo_dir=self.conf_local.get('path', 'root_path')
		file_dir=self.conf_local.get('个股', '数据保存路径')
		#方便记录比较和查看统计周期
		file_path_bak=os.path.join(roo_dir,file_dir,'成交量/地量/地量_百分{}成交量_均值_{}_{}.json'.format(str(int(set百分比*100)),start,end))#y用于bak时间戳，方便看统计时间
		file_path  =  os.path.join(roo_dir,file_dir,'成交量/地量/地量_百分{}成交量_均值.json'.format(str(int(set百分比*100))))

		#判断是否存在
		if(os.path.exists(file_path_bak)):
			print(f'%s 已经统计过'%file_path_bak)
			return None
		result=个股类().crawl_地量_codes_ak(start =start,end=end,set百分比=set百分比)

		if result is None or len(result)==0:
			print('error result is None')
			return None
		#print(result)	

		数据保存类().save_to_json(data=result,file_path=file_path)
		数据保存类().save_to_json(data=result ,file_path=file_path_bak)
		print(f'%s 爬取完成'%file_path_bak)








if __name__ == '__main__':

	todaynow = datetime.now().strftime('%Y%m%d')
	tradeday=TradingCalendar类().get_tradeday_from_day_pre(todaynow) 
 
	temp类=每月数据爬取类()

	temp类.每月更新_地量_codes(start='20220102',end='20240126',set百分比=0.2)
	 