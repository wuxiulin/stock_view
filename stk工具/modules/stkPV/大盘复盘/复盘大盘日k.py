class 复盘大盘日k类():
	def __init__(self):
		pass

	def get笔记_复盘大盘日k_day(self,tradeday):#data可以是黄白线数据，或者白线数据
		#print(data)
		pass
		昨日收盘白=float(ydata[-1][1])
		昨日收盘黄=float(ydata[-1][3])
		#print(昨日收盘白)
		今日分时白=[ float(item[1])  for item in data]
		今日分时黄=[ float(item[3])  for item in data]


		#波动点数，波动振幅，这是是一个东西么？看点数波动，还是振幅波动，以后再说吧
		#data是黄白线数据，所以这里做一个处理
		#第一种是昨日收盘比较，比较
		#第二种是早盘(9:30比较开盘价比较（高开或低开后，可能一天波动很小）

		#第一种 白（波动点数，涨幅，振幅）  黄（波动点数，涨幅，振幅）
		result1白=[round(max(今日分时白)-min(今日分时白),2),round(100*今日分时白[-1]/昨日收盘白-100,2),round((max(今日分时白)-min(今日分时白))*100/昨日收盘白,2)]
		result1黄=[round(max(今日分时黄)-min(今日分时黄),2),round(100*今日分时黄[-1]/昨日收盘黄-100,2),round((max(今日分时黄)-min(今日分时黄))*100/昨日收盘黄,2)]

		#第二种 白（波动点数，涨幅，振幅）  黄（波动点数，涨幅，振幅）

		result2白=[round(max(今日分时白)-min(今日分时白),2),round(100*今日分时白[-1]/今日分时白[0]-100,2),round((max(今日分时白)-min(今日分时白))*100/今日分时白[0],2)]
		result2黄=[round(max(今日分时黄)-min(今日分时黄),2),round(100*今日分时黄[-1]/今日分时黄[0]-100,2),round((max(今日分时黄)-min(今日分时黄))*100/今日分时黄[0],2)]

		
		#print(result1白,result1黄,result2白,result2黄,(max(今日分时白)-min(今日分时白))/今日分时白[0])
		txt='今日上证指数波动{}点，涨幅{}%，振幅{}%;'.format(result1白[0],result1白[1],result1白[2])
		txt=txt+'情绪黄线波动{}点，涨幅{}%，振幅{}%；'.format(result1黄[0],result1黄[1],result1黄[2])
		txt=txt+'如果以今日9:30为基准，白线涨幅{}%，振幅{}%；黄线涨幅{}%，振幅{}%'.format(result2白[1],result2白[2],result2黄[1],result2黄[2])

		return txt

	def get_日k图形(self):
		#单日k图给的信号，这里是共识，不是说技术图有用没用，而是信息传达出来的共识！
		#小阳中阳大阳，小阴中阴大阴线，，然后当下有没有特别信号传达出来
		pass


if __name__ == '__main__':
	pass