
from 买入 import 买入类
from 选股 import 选股类
from 卖出 import 卖出类

class 盈利类( ):
	"""docstring for 盈利"""
	def __init__(self):
		self.__盈利涨幅=[]
		pass

	def get_盈利涨幅(self):
		return self.__盈利涨幅


	def 盈利计算(self,buy类:type[买入类],sell类:type[卖出类],profittype=1):#倒腾理由是后面卖出类需要，但是不想传入很多个类，用一个完成数据传送
		#虽然买和卖价格得到，这里是可能又其他计算方式，
		#此处是普通方式实现
		buyprice=buy类.get_买入价格()
		sellprice=sell类.get_卖出价格()

		profit = [{key: round(100*sellprice[idx][key]/ buyprice[idx][key] -100,2)  for key in sellprice[idx]} for idx in range(len(sellprice))]
		
		# print(profit)
		
		self.__盈利涨幅=profit
		return profit





if __name__ == '__main__':
	
	a=选股类()
	a.均线突破_wencai(period='D',choseday='20231213',ma='250',srhtxt='去掉北交所')

	b=买入类()
	b.买入成本(T=1,Buytype=1,chose类=a)

	print(b.get_买入价格())
	print(b.get_买入时间())

	c=卖出类()
	c.卖出价格(T=1,Selltype=1,buy类=b)	#这里是为了传递买入的成本和时间等信息

	print(c.get_卖出价格())
	print(c.get_卖出时间())
	
	d=盈利类()
	d.盈利计算(buy类= b ,sell类= c,profittype=1)

	print(d.get_盈利涨幅())
 
