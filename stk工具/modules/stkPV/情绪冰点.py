#多个角度统计情绪冰点提示
#目前不好统计这些情绪冰点的节奏，周期就是说一定后面如何演化，目前看不到怎么分析出这个结论
#作为提示，特别关注是背离就是指数，但是情绪冰点这种提示

#

import os,sys
class 情绪冰点类( ):
 
	def __init__(self):
		pass

	def 情绪冰点_上涨家数(self):
		a=每日涨跌数.每日上涨数类()
		上涨数=a.get_day_每日上涨数_wencai(tradeday='20231221')
		#print(上涨数)
		return 上涨数

	def 情绪冰点_下跌家数(self):
		a=每日涨跌数.每日下跌数类()
		下跌数=a.get_day_每日下跌数_wencai(tradeday='20231221')
		#print(下跌数)
		return 下跌数
		pass



class 情绪高点类():
	def __init__(self):
		pass

	def 情绪高点_上涨家数(self):
		a=每日涨跌数.每日上涨数类()
		上涨数=a.get_day_每日上涨数_wencai(tradeday='20231221')
		#print(上涨数)
		return 上涨数

	def 情绪高点_下跌家数(self):
		a=每日涨跌数.每日下跌数类()
		下跌数=a.get_day_每日下跌数_wencai(tradeday='20231221')
		#print(下跌数)
		return 下跌数
		pass

if __name__ == '__main__':
	sys.path.append(os.path.abspath('../../'))
	#print(os.path.abspath('../../'))
	from modules.stkPV.获取各类数据函数 import 每日涨跌数

	a=情绪高点类( )
	print(a.情绪高点_上涨家数())
	print(a.情绪高点_下跌家数())

	b=情绪冰点类( )
	print(b.情绪冰点_上涨家数())
	print(b.情绪冰点_下跌家数())

