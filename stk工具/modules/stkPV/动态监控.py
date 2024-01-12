import configparser
import akshare as ak
import sys,os
import copy

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))#后面可以删除调试

from  modules.noteplt.notes_template import 复盘笔记类 
from  common import CommonStruct
 
class 股价监控类( ):
	"""docstring for 动态监控类"""
	def __init__(self,  ):
		self.conf = configparser.ConfigParser()
		self.path = os.path.join(  os.path.dirname(os.path.abspath(__file__)), 'conf/股价监控.cfg')
		self.conf.read( self.path ,encoding='utf-8')

		self.notes_txt=CommonStruct()#笔记格式公共类

	#作为复盘或者盘中动态指标个股等很多角度，临时添加重要提示，后面实现兑现后可能删除的，监控理由和解释笔记都要加上否则渴忘记了含义
	#
	## 修改配置数据
	#config.set('Settings', 'password', 'new_secret_password')

	# 添加一个新的配置项
	#config.set('Settings', 'new_option', 'new_value')

	# 重新写入到文件
	# with open('modified_example.ini', 'w') as configfile:
	#     config.write(configfile)
 


	def 复盘股价监控(self,tradeday):
		'''
		设置 ./stk/stkPV/conf/股价监控.cfg ,文件实现对个股股价的的监控
		设置方式: 类似如下格式，
			[600519]
			price_low_down = [1537, 1448]
			price_low_down_set = 1
		变量是关键字,price_low_down   含义：监控股价（price）的最低价（low），下跌（down）到设定值【可以多个依次比较】，开始告警
		price_low_down_set = 1  含义是set对应1，[1537, 1448]是满足其中条件后，重置 [1537],否则 不重置，还是[1537, 1448]

		'''
		codes=self.conf.sections()
		for code in codes:
			df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=tradeday , end_date=tradeday , adjust="qfq")
			#print(df)
			if(df is None or len(df)==0):
				print(code ,'数据为空')
				return None
			all_items = self.conf.items(code)
			for key, value in all_items:
				#print(key)
				if(key=='price_close_up'):
					pass
				elif(key=='price_low_down'):
					#字符转list
					try:
					    # 使用eval将字符串转换为列表
					    value = eval(value)
					    # 确保转换后是一个列表类型
					except Exception as e:
					    print("发生错误:", e)
					    raise e
					#print(value,value[0],type(value[1]))
					#print(df['最低'][0] , max(value))
					if(df['最低'][0] < max(value)):#最低价触碰设置位置
						#print('笔记')
						value1 = [x for x in value if x >= df['最低'][0]]#回写#去掉告警，以后不再提示，
						self.notes_txt.append([code+' 跌破设定预警监控值：'+ str(value1),'https://note.youdao.com/s/alhT1D4E'],keys=["dynamic_monitor"])
						set_value=self.conf.get(code, 'price_low_down_set') 
						#print(set_value,type(set_value))
						if(set_value=='1'):#删除已经实现的配置
							value2 = [x for x in value if x < df['最低'][0]]#回写#去掉告警，以后不再提示，
							self.conf.set(code, key, str(value2))


		#上面可能修改了配置，需要重写
		with open(self.path, 'w',encoding='utf-8') as configfile:
			self.conf.write(configfile)

		复盘笔记类().notes_stocks(data=self.notes_txt.data,page_type=13,ttype='dynamic_monitor') #page_type，设置需要改那个页面内容



class 指数点位监控格式1类( ):
	"""docstring for 动态监控类"""
	def __init__(self  ):
		self.conf = configparser.ConfigParser()
		self.path = os.path.join(  os.path.dirname(os.path.abspath(__file__)), 'conf/指数点数监控_格式1.cfg')
		self.conf.read( self.path ,encoding='utf-8')

		self.notes_txt=CommonStruct()#笔记格式公共类

	#作为复盘或者盘中动态指标个股等很多角度，临时添加重要提示，后面实现兑现后可能删除的，监控理由和解释笔记都要加上否则渴忘记了含义
	#
	## 修改配置数据
	#config.set('Settings', 'password', 'new_secret_password')

	# 添加一个新的配置项
	#config.set('Settings', 'new_option', 'new_value')

	# 重新写入到文件
	# with open('modified_example.ini', 'w') as configfile:
	#     config.write(configfile)
 


	def 复盘指数监控(self,tradeday):
		'''
		设置 ./stk/stkPV/conf/股价监控.cfg ,文件实现对个股股价的的监控
		设置方式: 类似如下格式，
			[600519]
			price_low_down = [1537, 1448]
			price_low_down_set = 1
		变量是关键字,price_low_down   含义：监控股价（price）的最低价（low），下跌（down）到设定值【可以多个依次比较】，开始告警
		price_low_down_set = 1  含义是set对应1，[1537, 1448]是满足其中条件后，重置 [1537],否则 不重置，还是[1537, 1448]

		'''
		codes=self.conf.sections()
		for code in codes:
			df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=tradeday , end_date=tradeday , adjust="qfq")
			#print(df)
			if(df is None or len(df)==0):
				print(code ,'数据为空')
				return None
			all_items = self.conf.items(code)
			for key, value in all_items:
				#print(key)
				if(key=='price_close_up'):
					pass
				elif(key=='price_low_down'):
					#字符转list
					try:
					    # 使用eval将字符串转换为列表
					    value = eval(value)
					    # 确保转换后是一个列表类型
					except Exception as e:
					    print("发生错误:", e)
					    raise e
					#print(value,value[0],type(value[1]))
					#print(df['最低'][0] , max(value))
					if(df['最低'][0] < max(value)):#最低价触碰设置位置
						#print('笔记')
						value1 = [x for x in value if x >= df['最低'][0]]#回写#去掉告警，以后不再提示，
						self.notes_txt.append([code+' 跌破设定预警监控值：'+ str(value1),'https://note.youdao.com/s/alhT1D4E'],keys=["dynamic_monitor"])
						set_value=self.conf.get(code, 'price_low_down_set') 
						#print(set_value,type(set_value))
						if(set_value=='1'):#删除已经实现的配置
							value2 = [x for x in value if x < df['最低'][0]]#回写#去掉告警，以后不再提示，
							self.conf.set(code, key, str(value2))


		#上面可能修改了配置，需要重写
		with open(self.path, 'w',encoding='utf-8') as configfile:
			self.conf.write(configfile)

		复盘笔记类().notes_stocks(data=self.notes_txt.data,page_type=13,ttype='dynamic_monitor') #page_type，设置需要改那个页面内容


class 指数点位监控格式2类( ):#给两个点坐标，就是日期和点位，自动计算预警值
	"""docstring for 动态监控类"""
	def __init__(self  ):
		self.conf = configparser.ConfigParser()
		self.path = os.path.join(  os.path.dirname(os.path.abspath(__file__)), 'conf/指数点数监控_格式2.cfg')
		self.conf.read( self.path ,encoding='utf-8')

		self.notes_txt=CommonStruct()#笔记格式公共类

	#作为复盘或者盘中动态指标个股等很多角度，临时添加重要提示，后面实现兑现后可能删除的，监控理由和解释笔记都要加上否则渴忘记了含义
	#
	## 修改配置数据
	#config.set('Settings', 'password', 'new_secret_password')

	# 添加一个新的配置项
	#config.set('Settings', 'new_option', 'new_value')

	# 重新写入到文件
	# with open('modified_example.ini', 'w') as configfile:
	#     config.write(configfile)
 

	def calculate_line_and_y(self,val):
		if(val[0]=='年'):
			x1=int(val[1][:4])
			x2=int(val[3][:4])
			x3=int(val[5][:4])

		if(val[0]=='季'):
			x1year=int(val[1][:4])
			x2year=int(val[3][:4])
			x3year=int(val[5][:4])
			
			x1ji=int(val[1][4:6])/3+1
			x2ji=int(val[3][4:6])/3+1
			x3ji=int(val[5][4:6])/3+1

			x1=0
			x2=(x2year-x1year)*4 + (x2ji-x1ji)
			x3=(x3year-x1year)*4 + (x3ji-x1ji)
			
		if(val[0]=='月'):
			x1year=int(val[1][:4])
			x2year=int(val[3][:4])
			x3year=int(val[5][:4])
			

			x1month=int(val[1][4:6])
			x2month=int(val[3][4:6])
			x3month=int(val[5][4:6])
			x1=0
			x2=(x2year-x1year)*12 + (x2month-x1month)
			x3=(x3year-x1year)*12 + (x3month-x1month)




		y1=val[2]
		y2=val[4]
		# 计算斜率 m
		m = (y2 - y1) / (x2 - x1)

		# 计算截距 b
		b = y1 - m * x1

		# 计算给定 x3 值时的 y3
		y3 = m * x3 + b

		# 返回斜截式方程的斜率、截距和对应 x3 值时的 y3
		#print(y3)
		return y3

	def 复盘指数监控(self,tradeday):
		'''
		设置 ./stk/stkPV/conf/股价监控.cfg ,文件实现对个股股价的的监控
		设置方式: 类似如下格式，
			[600519]
			price_low_down = [1537, 1448]
			price_low_down_set = 1
		变量是关键字,price_low_down   含义：监控股价（price）的最低价（low），下跌（down）到设定值【可以多个依次比较】，开始告警
		price_low_down_set = 1  含义是set对应1，[1537, 1448]是满足其中条件后，重置 [1537],否则 不重置，还是[1537, 1448]

		'''
		codes=self.conf.sections()
		#print(codes)
		for code in codes:   #symbol="sz399552"; 支持 sz: 深交所, sh: 上交所, csi: 中信指数 + id(000905)
			#print(code)
			df = ak.index_zh_a_hist(symbol=code, period="daily", start_date=tradeday , end_date=tradeday )
			#print(df)
			if(df is None or len(df)==0):
				print(code ,'数据为空，无法执行  复盘指数监控')
				return None
			all_items = self.conf.items(code)
			
			for key, value in all_items:
				#字符转list
				try:
				    # 使用eval将字符串转换为列表
				    value = eval(value)
				    # 确保转换后是一个列表类型
				except Exception as e:
				    print("发生错误:", e)
				    raise e
				tempvalue=copy.deepcopy(value)

				if(key=='price_close_up'):
					pass
				elif(key=='price_low_down'):
					for i in range(len(value)):
						#print(value,value[0],type(value[1]))
						#print(df['最低'][0] , max(value))
						#两点确认一条直线
						y3=self.calculate_line_and_y(value[i]+[tradeday])
						
						if(df['最低'][0] < y3*1.05):#最低价触碰设置位置5%开始告警一致告警，因为是指数，所以提前预警，且一直预警，所以set=0
							#print('笔记')
							self.notes_txt.append([code+' 到达105%设定预警监控值，设定值是'+ str(value[i]),''],keys=["dynamic_monitor"])
							set_value=self.conf.get(code, 'price_low_down_set') 
							#print(set_value,type(set_value))
							if(set_value=='1'):#删除已经实现的配置
								tempvalue.pop(i)#回写#去掉告警，以后不再提示，
								self.conf.set(code, key, str(tempvalue))


		#上面可能修改了配置，需要重写
		with open(self.path, 'w',encoding='utf-8') as configfile:
			self.conf.write(configfile)

		复盘笔记类().notes_stocks(data=self.notes_txt.data,page_type=13,ttype='dynamic_monitor') #page_type，设置需要改那个页面内容




if __name__ == '__main__':

	#动态监控类().复盘股价监控(tradeday='20240104')

	指数点位监控格式2类().复盘指数监控(tradeday='20240105')