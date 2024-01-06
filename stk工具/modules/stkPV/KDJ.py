import akshare as ak
import pandas as pd
import pylab as plt
from matplotlib.pyplot import MultipleLocator
import requests
import datetime
import time
		
class KDJ类():
	def __init__(self, ):
		pass
		

	def get_kdj(self): #结果有点不对，估计算法有问题
		data= ak.stock_zh_index_daily(symbol="sh000001")

		data=data.tail(10).reset_index(drop=True)
		#print(data)
		#print(data['close'])
		#data.to_excel('股票000001历史行情.xls')
		df=pd.DataFrame()
		df['close']=data['close'][-10:]
		#print(df)
		DATE=[]
		RSV=[]
		K_value=[]
		K_value.append(50)
		D_value=[]
		D_value.append(50)
		J_value=[] 
		for i in range(8,len(data)): 
			#print(data['date'])
			DATE.append(data['date'][i]) 
			high_price=data['high'][i-8:i+1].max() 
			low_price=data['low'][i-8:i+1].min() 
			close_price=data['close'][i] 
			RSV.append(100*(close_price-low_price)/(high_price-low_price)) 

			for i in range(1,len(RSV)): 
				K_value.append(2/3*K_value[i-1]+1/3*RSV[i]) 

			for i in range(1,len(RSV)): 
				D_value.append(2/3*D_value[i-1]+1/3*K_value[i]) 

			for i in range(len(K_value)): 
				J_value.append(3*K_value[i]-2*D_value[i]) 

		print(K_value[-1],D_value[-1],J_value[-1])

		plt.subplot(3,1,1)
		plt.plot(data['date'],df['close'],label=u'收盘价')
		plt.title('股票行情')
		plt.ylabel(u"价格线")
		x_major_locator=MultipleLocator(120)
		ax=plt.gca()
		ax.xaxis.set_major_locator(x_major_locator)
		plt.subplot(3,1,2)
		plt.plot(DATE,RSV,label=u'RSV线')
		x_major_locator=MultipleLocator(120)
		ax=plt.gca()
		ax.xaxis.set_major_locator(x_major_locator)
		plt.title('RSV线分析')
		plt.ylabel(u"RSV线")
		plt.subplot(3,1,3)
		#print(len(DATE),len(K_value),len(J_value))
		nummin=min([len(DATE),len(K_value),len(J_value)])

		plt.plot(DATE[-nummin:],K_value[-nummin:],'r',label=u'K值线')
		plt.plot(DATE[-nummin:],D_value[-nummin:],'g',label=u'D值线')
		plt.plot(DATE[-nummin:],J_value[-nummin:],'b',label=u'J值线')
		plt.rcParams['font.sans-serif']=['SimHei']
		plt.rcParams['axes.unicode_minus']=False
		plt.title('KDJ线分析')
		plt.ylabel(u"KDJ指标")
		x_major_locator=MultipleLocator(120)
		ax=plt.gca()
		ax.xaxis.set_major_locator(x_major_locator)
		plt.legend()
		plt.show()

 

	def get_实时日k级别kdj_昨日KDJ推算今日实时(self,yK=47.99,yD=31.9,yJ=80.19):


		#本来免费的网站想抓取历史数据，太卡了，算了！有能找到最新的也行不一定是很多历史数据
		#这里手动改就是了


		#RSV=（收盘价−最低价）/(最高价−最低价)*100
		#K=2/3*(前日K)+1/3当日RSV
		#D=2/3*（前日D）+1/3当日K
		#J=3*（当日K）-2*当日D
		while True:
			#获取当下实时数据
			stock_zh_index_spot_df = ak.stock_zh_index_spot()
			if(stock_zh_index_spot_df['代码'][0]=='sh000001'):
				pass
			else:
				print('格式有问题')
				time.sleep(60)
				continue
				
			close=stock_zh_index_spot_df['最新价'][0]
			low=stock_zh_index_spot_df['最低'][0]
			high=stock_zh_index_spot_df['最高'][0]


			RSV=(close-low)/(high-low)*100
			#print(RSV)
			K=2/3*yK+1/3*RSV
			D=2/3*yD+1/3*K
			J=3*K-2*D
			#print(K,D,J)
			

			current_time = datetime.datetime.now().time()
			target_time = datetime.time(15, 0) 
			if current_time > target_time:
				return None
			else:
			    time.sleep(60)




if __name__ == '__main__':
		#kdj算法知道，从头计算，计算量大
		#所以需要需要大量历史，就历史数据保存本地，
		#否则获取近期的kdj然后推算到当下！

		#这里有一些免费接口，能获取5min30min，但是跟日k不一样，这里看日k级别的！一般都是盘后算日k
		#但是盘中需要看这个日k的KDJ值，所以需要盘中自己计算
		#所以需要获取前几日的，然后快速推算今天实时的！


	KDJ类().get_实时日k级别kdj_昨日KDJ推算今日实时()

