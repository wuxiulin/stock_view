import configparser
import akshare as ak
import sys,os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))#后面可以删除调试

from  modules.noteplt.notes_template import 复盘笔记类 
from  common import CommonStruct
 
class 动态监控类( ):
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







if __name__ == '__main__':

	动态监控类().复盘股价监控(tradeday='20240104')
	pass
