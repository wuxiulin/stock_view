#有些数据需要每日保存】
import sys
import os
import configparser
from datetime import time as dttime
from datetime import datetime ,timedelta
import time
import akshare as ak
sys.path.append(os.path.dirname(os.path.abspath(__file__)) )
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ))
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) )))

from  数据保存                        import 数据保存类
from  数据爬取.股票代码映射            import 股票代码映射类
from  数据爬取.每日指数                import 每日指数类 
from  数据爬取.每日股指期货            import 每日股指期货类   
from  数据爬取.每日两市成交额    		 import 每日两市成交额类
from  数据爬取.每日涨跌停数            import 每日涨跌停数类
from  数据爬取.每日北向资金            import 每日北向资金类
from  数据爬取.每日涨停封单额          import 每日涨停封单额类
from  数据爬取.每日最高连板数          import 每日最高连板数类
from  数据爬取.每日上涨下跌数          import 每日上涨下跌数类
from  数据爬取.每日同花顺板块          import 每日同花顺板块类
from  数据爬取.每日财联社涨停分析      import  每日财联社涨停分析类
from  数据爬取.每日龙虎榜              import 每日龙虎榜类
from  数据爬取.每日资金流向            import 每日资金流向类
from  数据爬取.每日竞价               import  每日竞价类
from  数据爬取.个股                   import 个股类

from  common.TradingCalendar         import  TradingCalendar类


class 每日数据爬取类( ):
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

	def 每日更新_股票代码映射(self,tradeday):
		股票代码映射类().update_股票代码映射()

	def 每日更新_同花顺板块代码(self,tradeday):

		#这里目前是为了比较，得到新增概念
		每日同花顺板块类().crawl_每日同花顺概念板块代码()


	def 每日更新_领先指数_min(self,tradeday):

		file_dir=self.conf_global.get('领先指数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'1c0002/min/{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据
		data=每日指数类().crawl_同花顺领先指数1c0002_min()
		if data is None or len(data)<240:
			print(data)
			print('error，查看数据，有问题补全')
			return
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%file_path)

	def 每日更新_指数_min(self,tradeday):
		file_dir=self.conf_global.get('每日指数', '数据保存路径')
		symbols=["000001",'399001']
		for symbol in symbols:
			period="1"
			file_path=os.path.join(self.root_path,file_dir,symbol,period+'min','{}.json'.format(tradeday))
			#判断是否存在
			if(os.path.exists(file_path)):
				print(f'%s 今日已经爬取'%file_path)
				continue
			#爬取数据
			start_ft=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:]
			data = ak.index_zh_a_hist_min_em(symbol=symbol, period=period, start_date=start_ft+" 09:15:00", end_date=start_ft+" 19:00:00")
			#print(data)
			if(data is None or len(data)==0):
				print('error,数据为空')
				continue
			#print(data)
			#保存数据 按照行把df保存为json
			数据保存类().save_to_json(data=data.to_json(orient='records'),file_path=file_path)
			#读取为df方式   df = pd.read_json(json_filename, orient='records')
			print(f'%s 爬取完成'%file_path)


	def 每日更新_股指期货_min(self,tradeday):
		file_dir=self.conf_global.get('股指期货', '数据保存路径')
		更新时间_股指期货=self.conf_global.get('股指期货', '更新时间_股指期货')
		 
		#判断是否存在
		if 更新时间_股指期货 == tradeday:
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据
		 
		data=每日股指期货类().crawl_同花顺股指期货_min()
		if(data is None):
			print('爬取数据为空')
			return
		#保存数据,一次爬取多个结果
		for key,value in data.items():
			file_path=os.path.join(self.root_path,file_dir,'min/{}_{}.json'.format(tradeday,key))
			数据保存类().save_to_json(data=value,file_path=file_path)
		print('股指期货 爬取完成')


	def 每日更新_涨跌停数_min(self,tradeday):
		file_dir=self.conf_global.get('每日涨跌停数', '数据保存路径')
		file_path_z=os.path.join(self.root_path,file_dir,'min/涨停/{}.json'.format(tradeday))
		file_path_d=os.path.join(self.root_path,file_dir,'min/跌停/{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path_z) and os.path.exists(file_path_d)):
			print(f'%s 今日已经爬取'%file_path_z)
			print(f'%s 今日已经爬取'%file_path_d)
			return
  		#爬取数据
		data=每日涨跌停数类().crawl_涨跌停数_min(tradeday=tradeday)
		if(data is None):
			print('爬取数据为空')
			return
		数据保存类().save_to_json(data={tradeday:data[0]},file_path=file_path_z)
		数据保存类().save_to_json(data={tradeday:data[1]},file_path=file_path_d)
		print(f'%s 爬取完成'% file_path_z)
		print(f'%s 爬取完成'% file_path_d)
	def 每日更新_昨日涨停今日收益涨跌幅_min(self,tradeday):
		file_dir=self.conf_global.get('昨日涨停今日收益涨跌幅', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'min/{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
  		#爬取数据
		data=每日涨跌停数类().crawl_昨日涨停今日收益涨跌幅_min(tradeday=tradeday)
		if(data is None):
			print('爬取数据为空')
			return
		数据保存类().save_to_json(data={tradeday:data[0]},file_path=file_path)
 
		print(f'%s 爬取完成'% file_path)


	def 每日更新_北向资金_min(self,tradeday):
		file_dir=self.conf_global.get('每日北向资金', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'min/{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return

		#爬取数据
		data=每日北向资金类().crawl_每日北向资金_min(tradeday=tradeday)
		if(data is None):
			print('爬取数据为空')
			return
		
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%file_path)

	def 每日更新_每日竞价(self,tradeday):
		file_dir=self.conf_global.get('每日竞价', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'min/{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据
		data=每日竞价类().crawl_竞价_min(tradeday=tradeday)
		if(data is None):
			print('爬取数据为空')
			return
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%file_path)
		#立刻更新其他数据，不用单独写了
		self.每日更新_每日竞价涨跌及分布(tradeday=tradeday,indata=data)

	def 每日更新_每日竞价涨跌及分布(self,tradeday,indata):
		file_dir=self.conf_global.get('每日竞价', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day/{}.json'.format('每日竞价涨跌及分布_字典'))
		#判断是否存在
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return
		#爬取数据  
		# temp类=每日两市成交额.每日两市成交额类()
		# data=temp类.crawl_每日两市成交额_ak(outtype=0)
		# if(data is None):
		# 	print('爬取数据为空')
		# 	return
		#处理分类数据
		date_string= tradeday+' 09:25:00'
		dt_object = datetime.strptime(date_string, "%Y%m%d %H:%M:%S")
		timestamp =str( int(dt_object.timestamp()))
		res={}
		for key in indata.keys():
			try:
				res[key]=indata[key][timestamp]
			except Exception as e:
				print(timestamp)
				raise e
		data[tradeday]=res
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
 
		#读取
		file_path=os.path.join(file_dir,'day/{}.json'.format('每日竞价涨跌及分布_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,res])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))





	def 每日更新_两市成交额(self,tradeday):
		file_dir=self.conf_global.get('每日两市成交额', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('每日两市成交额_字典'))
		#判断是否存在
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return
		#爬取数据
		data=每日两市成交额类().crawl_每日两市成交额_ak(outtype=0)
		if(data is None):
			print('爬取数据为空')
			return
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		#爬取数据
		data=temp类.crawl_每日两市成交额_ak(outtype=1)		
		file_path=os.path.join(file_dir,'{}.json'.format('每日两市成交额_有序列表'))
		
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

	def 每日更新_涨停封单额(self,tradeday):
		file_dir=self.conf_global.get('每日涨停封单额', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('每日涨停封单额_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日涨停封单额类().crawl_每日涨停封单额_day_by_wencai(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return
		#添加数据
		data[tradeday]=out
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'{}.json'.format('每日涨停封单额_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,out])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))


	def 每日更新_最大涨停封单额(self,tradeday):
		file_dir=self.conf_global.get('每日涨停封单额', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('每日最大涨停封单额_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日涨停封单额类().crawl_每日最大涨停封单额_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return

		#添加数据
		data[tradeday]=out
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'{}.json'.format('每日最大涨停封单额_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,out])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))


	def 每日更新_每日最高连板数(self,tradeday):
		file_dir=self.conf_global.get('每日最高连板数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('每日最高连板数_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日最高连板数类().crawl_每日最高连板数_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return

		#添加数据
		data[tradeday]=str(out)
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'{}.json'.format('每日最高连板数_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,str(out)])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))

	def 每日更新_每日最高连板数_龙头股(self,tradeday):
		file_dir=self.conf_global.get('每日最高连板数_龙头股', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format('每日最高连板数_龙头股_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日最高连板数类().crawl_每日最高连板数_龙头股_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return
		#添加数据
		data[tradeday]=out
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'{}.json'.format('每日最高连板数_龙头股_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,out])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))

	def 每日更新_每日涨停数(self,tradeday):		
		file_dir=self.conf_global.get('每日涨跌停数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day/{}.json'.format('每日涨停数_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日涨跌停数类().crawl_每日涨停数_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return

		#添加数据
		data[tradeday]=str(out)
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'day/{}.json'.format('每日涨停数_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,str(out)])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))
	
	def 每日更新_每日跌停数(self,tradeday):
		file_dir=self.conf_global.get('每日涨跌停数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day/{}.json'.format('每日跌停数_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日涨跌停数类().crawl_每日跌停数_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return

		#添加数据
		data[tradeday]=str(out)
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'day/{}.json'.format('每日跌停数_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,str(out)])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))



 




	def 每日更新_每日上涨数(self,tradeday):
		file_dir=self.conf_global.get('每日上涨下跌数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day/{}.json'.format('每日上涨数_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日上涨下跌数类().crawl_每日上涨下跌数_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return
		#添加数据
		data[tradeday]=str(out[0])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'day/{}.json'.format('每日上涨数_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,str(out[0])])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))

	def 每日更新_每日下跌数(self,tradeday):
		file_dir=self.conf_global.get('每日上涨下跌数', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day/{}.json'.format('每日下跌数_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日上涨下跌数类().crawl_每日上涨下跌数_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return
		#添加数据
		data[tradeday]=str(out[1])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'day/{}.json'.format('每日下跌数_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,str(out[1])])
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))

	def 每日更新_每日同花顺二级行业板块_min(self,tradeday):
		#每日同花顺二级行业板块   更新
		file_dir=self.conf_global.get('每日同花顺二级行业板块', '数据保存路径')
		temp类=每日同花顺板块.每日同花顺板块类()
		blks=temp类.crawl_每日同花顺二级行业代码()  

		for blk in blks:
			print(blk)
			file_path=os.path.join(self.root_path,file_dir,'min/{}/{}.json'.format(blk,tradeday))
			#判断是否存在
			if(os.path.exists(file_path)):
				print(f'%s 今日已经爬取'%file_path)
				continue
			#爬取数据
			data=temp类.crawl_每日同花顺板块_min(tradeday=tradeday,blk=blk)
			if(data is None):
				print('爬取数据为空')
				time.sleep(5)
				#return None
				continue
			
			#保存数据
			数据保存类().save_to_json(data=data,file_path=file_path)
			print(f'%s 爬取完成'%file_path)
			time.sleep(3)

		file_dir=self.conf_global.get('每日同花顺概念板块', '数据保存路径')
		blks=每日同花顺板块类().crawl_每日同花顺概念板块代码()
		#print(len(blks))
		for blk in blks:
			print(blk)
			file_path=os.path.join(file_dir,'min/{}/{}.json'.format(blk,tradeday))
			#判断是否存在
			if(os.path.exists(file_path)):
				print(f'%s 今日已经爬取'%file_path)
				continue
			#爬取数据
			data=temp类.crawl_每日同花顺板块_min(tradeday=tradeday,blk=blk)
			if(data is None):
				print('爬取数据为空')
				#return None
				time.sleep(5)
				continue
			
			#保存数据
			数据保存类().save_to_json(data=data,file_path=file_path)
			print(f'%s 爬取完成'%file_path)
			time.sleep(3)

	def 每日更新_每日同花顺二级行业板块_资金流向_day(self,tradeday):
		file_dir=self.conf_global.get('每日同花顺二级行业板块', '数据保存路径')		
		file_path=os.path.join(self.root_path,file_dir,'day板块资金流向/{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据
		data=每日同花顺板块类().crawl_每日同花顺二级行业_资金流向_day(tradeday=tradeday)
		if(data is None):
			print('爬取数据为空')
			return None
		#print(data)
		#保存数据 按照行把df保存为json
		数据保存类().save_to_json(data=data.to_json(orient='records'),file_path=file_path)
		#读取为df方式   df = pd.read_json(json_filename, orient='records')
		print(f'%s 爬取完成'%file_path)

	def 每日更新_每日财联社涨停分析(self,tradeday):
		
		file_dir=self.conf_global.get('每日财联社涨停分析', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return	

		data=每日财联社涨停分析类().crawl_财联社_每日涨停数据_pic_to_file(tradeday=tradeday,file_dir=file_dir)
		if(data is None):
			print('爬取数据为空')
			return None

		#数据再次格式化一下
		data=data['data']
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%file_path)

		#为了方便再次回顾，这里多保存了txt
		数据保存类().save_to_text(data=data,file_path=os.path.join(file_dir,tradeday+'.txt'))
		

	def 每日更新_每日龙虎榜(self,tradeday):
		file_dir=self.conf_global.get('每日龙虎榜', '数据保存路径')
		
		file_path=os.path.join(self.root_path,file_dir,'{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据
		data=每日龙虎榜类().crawl_龙虎榜_day(tradeday=tradeday)
		if(data is None):
			print('爬取数据为空')
			return None
		#print(data)
		#保存数据
		数据保存类().save_to_json(data=str(data),file_path=file_path)
		print(f'%s 爬取完成'%file_path)

	def 每日更新_股指期货_day(self,tradeday):#返回数据多个文件，所以有点不同的判断方式
		# temp类=每日股指期货.每日股指期货类()
		# out=temp类.crawl_同花顺股指期货_day(flag_20days=2)
		# print(out)#方便补齐，所以打印就好了然后复制粘贴就好了
		# return 
		#有个20日数据函数没有调用以后再说吧
		file_dir=self.conf_global.get('股指期货', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day','{}.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据
		out=每日股指期货类().crawl_同花顺股指期货_day()
		if(out is None):
			print('爬取数据为空',file_path)
			return
		for key,value in out.items():#沪深300等指数顺便保存一下吧，
			#读取数据
			file_path=os.path.join(file_dir,'day','{}_字典.json'.format(key))
			data=数据保存类().read_from_json(file_path=file_path)			
			if(data is None):
				data={}
			if 'cha' in key:
				data[tradeday]= value
			else:
				data[tradeday]=value
			数据保存类().save_to_json(data= data ,file_path=file_path)
			print(f'%s 爬取完成'%os.path.basename(file_path))

			file_path=os.path.join(file_dir,'day','{}_有序列表.json'.format(key))
			data=数据保存类().read_from_json(file_path=file_path)		
			if(data is None):
				data=[]
			if 'cha' in key:
				data.append([tradeday,value])
			else:
				data.append([tradeday,value])
			数据保存类().save_to_json(data= data ,file_path=file_path)

			print(f'%s 爬取完成'%os.path.basename(file_path))

		file_path=os.path.join(file_dir,'day','{}.json'.format(tradeday))
		数据保存类().save_to_json(data='一次获取多个数据情况下，作为保存结束标志用的文件名字',file_path=file_path)
		print(f'%s 爬取完成'%file_path)

	def 每日更新_股指期货_day_mul(self,tradeday):
		file_dir=self.conf_global.get('股指期货', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day','{}_mul.json'.format(tradeday))
		#判断是否存在
		if(os.path.exists(file_path)):
			print(f'%s 今日已经爬取'%file_path)
			return
		#爬取数据		
		out=每日股指期货类().crawl_同花顺股指期货_day_mul()
		#print(out)
		for key,value in out.items():#沪深300等指数顺便保存一下吧，
			#读取数据
			filename=value['name']
			file_path=os.path.join(file_dir,'day','{}_字典.json'.format(filename))
			data=数据保存类().read_from_json(file_path=file_path)			
			if(data is None):
				data={}
			value.pop('name')
			data[tradeday]=value
			#print(data[tradeday])
			数据保存类().save_to_json(data= data ,file_path=file_path)
			print(f'%s 爬取完成'%os.path.basename(file_path))

			file_path=os.path.join(file_dir,'day','{}_有序列表.json'.format(filename))
			data=数据保存类().read_from_json(file_path=file_path)		
			if(data is None):
				data=[]
			data.append([tradeday,value])
			数据保存类().save_to_json(data= data ,file_path=file_path)

			print(f'%s 爬取完成'%os.path.basename(file_path))

		file_path=os.path.join(file_dir,'day','{}_mul.json'.format(tradeday))
		数据保存类().save_to_json(data='一次获取多个数据情况下，作为保存结束标志用的文件名字',file_path=file_path)
		print(f'%s 爬取完成'%file_path)



	def 每日更新_每日资金流向(self,tradeday):
		file_dir=self.conf_global.get('每日资金流向', '数据保存路径')
		file_path=os.path.join(self.root_path,file_dir,'day/{}.json'.format('每日资金流向_字典'))

		#判断是否存在
		#读取
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data={}
		if(tradeday in data.keys()):
			print(f'%s 今日已经爬取'%os.path.basename(file_path))
			return

		#爬取数据
		out=每日资金流向类().crawl_每日沪深资金流向_day(tradeday=tradeday)
		if(out is None):
			print('爬取数据为空')
			return
		#添加数据
		data[tradeday]=out  #单位亿
 
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)
		print(f'%s 爬取完成'%os.path.basename(file_path))

		#读取
		file_path=os.path.join(file_dir,'day/{}.json'.format('每日资金流向_有序列表'))
		data=数据保存类().read_from_json(file_path=file_path)
		if(data is None):
			data=[]
		#添加数据
		data.append([tradeday,out])
 
		#保存数据
		数据保存类().save_to_json(data=data,file_path=file_path)

		print(f'%s 爬取完成'%os.path.basename(file_path))

	def 每日更新_创N日新低_codes(self,end,start='19800101'):
 
		file_dir=self.conf_global.get('个股', '数据保存路径')
		统计时间_创N日新低=self.conf_global.get('个股', '统计时间_创N日新低')
		file_path  =  os.path.join(self.root_path,file_dir,'股价/创N日新低/创N日新低.json')
		if 统计时间_创N日新低 ==  '{} {}'.format(start,end):
			print(f'%s 已经统计过'%file_path)
			return None
		data=个股类().crawl_创N日新低_codes(start=start,end=end)
		if data is None or len(data)==0:
			return None

		数据保存类().save_to_json(data=data,file_path=file_path)
 
		print(f'%s 爬取完成'%os.path.basename(file_path))










if __name__ == '__main__':
 
	current_time = datetime.now().time()
	todaynow = datetime.now().strftime('%Y%m%d')
	temp类=每日数据爬取类()
	tradeday=TradingCalendar类().get_tradeday_from_today()#凌晨5点前返回上一个交易日而非今日这个交易日

	print('更新时间为：',tradeday)

	if tradeday is not None :#返回的可能是None #非交易日直接执行，交易日判断时间hour后，更新数据后再爬取
		if (dttime(15, 0) < current_time < dttime(23, 59,)  and todaynow == tradeday)  \
			or (todaynow != tradeday ): #非交易日直接执行，或者凌晨直接更新

			temp类.每日更新_股票代码映射(tradeday=tradeday)
			temp类.每日更新_同花顺板块代码(tradeday=tradeday)
			temp类.每日更新_指数_min(tradeday=tradeday)
			temp类.每日更新_领先指数_min(tradeday=tradeday)
			temp类.每日更新_两市成交额(tradeday=tradeday)
			temp类.每日更新_涨停封单额(tradeday=tradeday)
			temp类.每日更新_最大涨停封单额(tradeday=tradeday)
			temp类.每日更新_每日最高连板数(tradeday=tradeday)
			temp类.每日更新_每日最高连板数_龙头股(tradeday=tradeday)
			temp类.每日更新_北向资金_min(tradeday=tradeday)
			temp类.每日更新_涨跌停数_min(tradeday=tradeday)
			temp类.每日更新_每日涨停数(tradeday=tradeday)
			temp类.每日更新_昨日涨停今日收益涨跌幅_min(tradeday=tradeday)
			temp类.每日更新_每日跌停数(tradeday=tradeday)
			temp类.每日更新_每日上涨数(tradeday=tradeday)
			temp类.每日更新_每日下跌数(tradeday=tradeday)
			temp类.每日更新_股指期货_min(tradeday=tradeday)
			temp类.每日更新_股指期货_day(tradeday=tradeday)
			temp类.每日更新_股指期货_day_mul(tradeday=tradeday)
			temp类.每日更新_每日资金流向(tradeday=tradeday)
			temp类.每日更新_每日同花顺二级行业板块_资金流向_day(tradeday=tradeday)
			temp类.每日更新_每日竞价(tradeday=tradeday)
			temp类.每日更新_创N日新低_codes(end=tradeday)

		if (dttime(17, 0) < current_time < dttime(23, 59,)  and todaynow == tradeday)  \
			or (todaynow != tradeday ): #非交易日直接执行，或者凌晨直接更新
			
			temp类.每日更新_每日龙虎榜(tradeday=tradeday)

		if (dttime(19, 0) < current_time < dttime(23, 59,)  and todaynow == tradeday)  \
			or (todaynow != tradeday ): #非交易日直接执行，或者凌晨直接更新

			temp类.每日更新_每日同花顺二级行业板块_min(tradeday=tradeday)#太早容易被反爬去，所以晚点执行
			temp类.每日更新_每日财联社涨停分析(tradeday=tradeday)#多说在前30min但是少数到了50min才有数据

 






