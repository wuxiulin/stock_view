
##选股方式（1）爬取数据，然后计算，比较，选股
#（2）自然语言，说想法，然后问财等方式选股！ 文字表达要准确需要测试，通用的的句式，才能复用方便，需要测试，

import pywencai

class 选股类( ):
	def __init__(self):
		self.__选股日期=''
		self.__选股代码=[]
		self.__选股code=[]
		pass
	def get_选股日期(self):
		return self.__选股日期

	def get_选股代码(self):
		return self.__选股代码

	def get_选股code(self):
		return self.__选股code

	def 均线突破_wencai(self,period='D',choseday='20231215',ma='250',srhtxt=''):#以后可以添加股票池
		#这里不检查choseday，通过问题，反应到给上层，
		if(period=='D'):
			searchtxt="{}收盘价上穿{}的{}日均线".format(choseday,choseday,ma)
			searchtxt=searchtxt+' , '+srhtxt
		if(period=='W'):
			searchtxt="{}收盘价上穿{}的{}周均线".format(choseday,choseday,ma)
			searchtxt=searchtxt+' , '+srhtxt
 		
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"  pywencai.get    is error ",'  searchtxt is ',searchtxt) 
			return None
		#print(res.columns)
		self.__选股code=list(res['code'])
		self.__选股日期=choseday
		self.__选股代码=list(res['股票代码'])
		return list(res['股票代码'])
		





if __name__ == '__main__':
	# a=选股类()
	# a.均线突破_wencai(period='D',choseday='20231215',ma='250',srhtxt='去掉北交所')
	# print(a.get_选股日期())
	# print(a.get_选股代码())
	# print(a.get_选股code())


	a=[[]]*2
	print(a)
	print(len(a))
