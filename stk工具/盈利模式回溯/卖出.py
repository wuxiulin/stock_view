import akshare as ak
from 买入 import 买入类
from 选股 import 选股类


class 卖出类( ):
	def __init__(self):
		self.__卖出时间=''
		self.__卖出价格=0

		pass
	def get_卖出价格(self):
		return self.__卖出价格
	def get_卖出时间(self):
		return self.__卖出时间
		pass
	def 卖出价格(self,buy类:type[买入类],T=1,Selltype=1):#提示buy类是买入类类型，但是无法不报错
		if(T<=0):
			print('error T 至少为1，因为A股，T+1,')
			return None
		codes=buy类.get_选股code()
		if(len(codes)==0):
			print('codes 空')
			return None
		elif(len(codes[0])!=6):#或者A股池子获取判断，是股票代码也行，这里判断是代码格式有问题！
			print('codes 格式有问题，这里是需要类似  000001 ')
			return None

		#第一个大类，先是持股时间T 决定  choseday是选股日，为基准
		buytime=buy类.get_买入时间()  #卖出至少是隔日，隔日，因为A股，T+1
		if(len(buytime)==0):
			print("先通过买入类.买入价格()，对象获取买入时间，这里代码有误")
        
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		if buytime in trade_df:
			index = trade_df.index(buytime)
		else:
			print(choseday ,"  choseday 输入不是交易日，或者格式有误，这里输入类似  20231215 ")

		sellday=trade_df[index+T]#在这天卖

		sellprice_codes=[]
		for code in codes:
			#股价信息
			stock_df = ak.stock_zh_a_hist(symbol=code, period="daily", start_date=sellday, end_date=sellday, adjust="qfq")
			#print(stock_df)
			#进一步确认买点成本，
			if(len(stock_df)==0):#数据缺失
				print('数据缺失，尝试补缺')
				
				买入价格=buy类.get_买入价格() 
				target_value = next((item.get( code, 0) for item in 买入价格 if  code in item),-10000)
				if(sellprice==-10000):
					print(买入价格)
					print("数据缺失，补缺失败，给定极限值")
				else:
					print('成功缺失，数据为买入成本价')
             
			else:
				try:
					if(Selltype==0):#早竞价0 
						sellprice=stock_df['开盘'][0]
					elif(Selltype==1):# 收盘1，
						sellprice=stock_df['收盘'][0] 
					elif(Selltype==2):# 最高2， 
						sellprice=stock_df['最高'][0]
					elif(Selltype==3):#  最低3，
						sellprice=stock_df['最低'][0]
					else:
						print("没有设置，需要添加代码")
						return None
				except Exception as e:
					print(code,sellday,stock_df)
					print(e)
					continue
					#raise e

			sellprice_codes.append({code:sellprice})
		#print(buyday,buyprice)
		#倒腾理由是后面卖出类需要，但是不想传入很多个类，用一个完成数据传送
		self.__卖出时间=sellday
		self.__卖出价格=sellprice_codes

		return sellprice_codes




        #二大类是价格或涨幅到，时间不确定，

        #三类规定一二结合，在规定时间内，涨幅到就是卖出，涨幅没到直接卖哪怕割肉




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
	#
