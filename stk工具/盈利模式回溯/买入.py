#买入条件的确认和选择，决定的是成本价

#这里汇聚是选股的买点确认后的成本计算

import akshare as ak
from 选股 import 选股类
class 买入类( ):

	def __init__(self  ):

		self.__买入时间=''#私有数据，不能外部访问，不让修改，而是通过函数来调用
		self.__买入价格=0
		self.__选股代码=''   #后面需要传递，都是可以通过选股类往后面传递的
		self.__选股code=''
		self.__选股日期=''


		pass
	def get_买入时间(self):
		return self.__买入时间

	def get_买入价格(self):
		return self.__买入价格
		
	def get_选股代码(self):
		return self.__选股代码

	def get_选股code(self):
		return self.__选股code

	def 买入成本(self,chose类:type[选股类],T=0,Buytype=1,):#choseday选股日，算出买入日
	#股票池获取，这通过选股了获取，如果其他方式，那么自建一个新函数就好，类似功能这实现是通过选股类方式
		#只是其中一类决定买点方式，其他的可以再另开函数
		#比较简单的分类汇聚这里，
		#距离tradeday选股日天数，0就是当天，1就是第二日，-1就是昨日(特殊操作吧，附带能实现)，这里是纯交易日！
		#假设保证tradeday是交易日不是假期，其次是，+1得到结果还是交易日，不会是假期，
		#type,是确认某日内的买点情况，早竞价0，收盘1，最高2，最低3，等不同选择，都在这里补充添加，
		#获取交易列表，然后定位tradeday后选择+t
		choseday=chose类.get_选股日期()
		codes=chose类.get_选股code()#带后缀的也有，换一个函数

		#print(codes)
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		if choseday in trade_df:
			index = trade_df.index(choseday)
		else:
			print(choseday ,"  choseday 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
		buyday=trade_df[index+T]#在这天买
		
		#print(buyday)
		
		#依次获取buyday的数据，进一步type确定买点
		if(len(codes)==0):
			print('codes 空')
			return None
		elif(len(codes[0])!=6):#或者A股池子获取判断，是股票代码也行，这里判断是代码格式有问题！
			print('codes 格式有问题，这里是需要类似  000001 ')
			return None
		buyprice_codes=[]
		for code in codes:
			#股价信息
			stock_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=buyday, end_date=buyday, adjust="qfq")
			#print(stock_df)
			#进一步确认买点成本，
			if(Buytype==0):#早竞价0 
				buyprice=stock_df['开盘'][0]
			elif(Buytype==1):# 收盘1，
				buyprice=stock_df['收盘'][0] 
			elif(Buytype==2):# 最高2， 
				buyprice=stock_df['最高'][0]
			elif(Buytype==3):#  最低3，
				buyprice=stock_df['最低'][0]
			else:
				print("没有设置，需要添加代码")
				return None
			buyprice_codes.append({code:buyprice})

		#print(buyday,buyprice)
		#倒腾理由是后面卖出类需要，但是不想传入很多个类，用一个完成数据传送
		self.__买入时间=buyday
		self.__买入价格=buyprice_codes
		self.__选股code=chose类.get_选股code()
		self.__选股代码=chose类.get_选股代码()
		self.__选股日期=chose类.get_选股日期()
		return buyprice_codes







if __name__ == '__main__':
	a=选股类()
	a.均线突破_wencai(period='D',choseday='20231215',ma='250',srhtxt='去掉北交所')

	b=买入类()
	b.买入成本(T=0,Buytype=1,chose类=a)

	print(b.get_买入价格())
	print(b.get_买入时间())
	#print(type(b.get_买入价格()))