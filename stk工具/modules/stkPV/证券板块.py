
# import sys
# import os
# current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# parent_dir = os.path.dirname(current_dir)
# #print(parent_dir)
# sys.path.append(parent_dir)




from  stk工具.common import DataStruct
import pywencai
import akshare as ak
from datetime import date
import datetime

 


class 证券():
	"""docstring for ClassName"""
	def __init__(self):
		self.result=DataStruct()
		
	def 证券个股连板(self,searchtxt="2020年07月03日涨停，证券板块"):
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"证券个股连板  pywencai.get    is error ") 
			return None
		#res = pywencai.get(query="涨停，证券板块",loop=True,query_type='stock')#sort_key='所属同花顺行业'
		#print(res)
		if(res is None):
			return  None
		columns=res.columns
		#证券有个股三连板
		zt_res_col=([ i  for i in columns  if('连续涨停天数' in i)  ])#连续涨停列名字
		#print(zt_res_col)
		if(len(zt_res_col)!=1):#结果df列名字有问题
			res = pywencai.get(query="涨停，证券板块",loop=True,query_type='stock')#sort_key='所属同花顺行业'
			columns=res.columns
			zt_res_col=([ i  for i in columns  if('连续涨停天数' in i)  ])#连续涨停列名字
			if(len(zt_res_col)!=1):
				print(" 连续涨停天数 搜索结果没有这列名字")
		if(len(zt_res_col)==1):#处理完所有事项,形成”证券有个股三连板“代码功能块，代码不要写出去
			zt_res_col=zt_res_col[0]#列名字
			temp=list(res[zt_res_col])
			#print(temp)
			temp=[i for i in temp if(i >= 3 ) ]#三连板统计结果
			#print(temp)
			if(len(temp)>=1):#存在大于三连板的个股，保存信号
				#不用看是哪个股了，直接输出信号就好复盘证券所有个股和指数走势
				#输出格式是什么样子的
				#print(result.data)
				#result.append("证券个股出现三连板，指数牛市预期",keys=['stocks'])
				self.result.append(["证券个股出现三连板，牛市预期，关注此层面机会",'https://note.youdao.com/s/c8CQowSB'])#默认keys=空，表示全部添加
				#print(result.data)
			#二连板
			temp=[i for i in temp if(i >= 2 ) ]#二连板统计结果
			#print(temp)
			if(len(temp)>=1):#存在大于二连板的个股，保存信号
				#不用看是哪个股了，直接输出信号就好复盘证券所有个股和指数走势
				#输出格式是什么样子的
				#print(result.data)
				#result.append("证券个股出现三连板，指数牛市预期",keys=['stocks'])
				tip="证券个股出现二连板，证券板块机会。是否有演化三连板可能性，激活牛市预期？"
				self.result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])#默认keys=空，表示全部添加
				#print(result.data)
			#涨停板
			temp=[i for i in temp if(i >= 1) ]#
			if(len(temp)>=3):#证券板块有三个个股涨停首板 #证券当日涨停数量多，需要统计一下得到一个阈值
				tip="证券个股出现三个以上首板，证券板块机会。是否有演化二连板可能性，激活牛市预期？"
				self.result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])#默认keys=空，表示全部添加
		else:
			pass#搜索结果有问题，报错了，跳过这个检测

		return self.result
		
	def 证券个股异动(self):
		#个股信号
		#stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600030", period="daily", start_date="20231001", end_date='', adjust="qfq")
		#print(stock_zh_a_hist_df)
	 
		#中信证券3%大阳
		tempday = date.today()
		tempday = datetime.datetime.strftime(tempday,"%Y%m%d")
		stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600030", period="daily", start_date=tempday[:4]+"0101", end_date=tempday, adjust="qfq")
		#print(stock_zh_a_hist_df)
		if(list(stock_zh_a_hist_df['涨跌幅'])[-1] > 0):
			tip="中信证券大涨，证券机会"
			self.result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])
		return self.result

if __name__ == '__main__':
	a=证券()
	b=a.证券个股异动()
	print(b.data)
