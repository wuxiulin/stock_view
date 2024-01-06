import akshare as ak
# from modules.stkPV.获取各类数据函数 import 每日涨跌数
# from modules.stkPV.获取各类数据函数 import 每日上证指数黄白线分钟数据
from  获取各类数据函数 import 每日最高连板数
from  财联社每日涨停复盘 import 财联社涨停分析
from  datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import os ,sys
import re


class 复盘涨停板类( ):
	"""docstring for 复盘涨停板类"""
	def __init__(self):
		pass

	def 复盘stocks_昨日最高涨停连板高度(self):
		#昨日高度股，今日表现，可能跟其他重复，所以这里分析断板？或者说分析也可以，在某个地方保存所有已经分析过的票就是了比较差集后再分析！
		#
		pass
		#



	def 最高涨停连板高度(self):

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		todaynow = datetime.now()
		last_date=todaynow
		last_date_string =todaynow.strftime("%Y%m%d")
		last_yetd_date_string =''
		#print(last_date_string,trade_df[1])
		while True:
			if(last_date_string not in trade_df):
				last_date=last_date-timedelta(days=1)#最近上一个交易日
				last_date_string = last_date.strftime("%Y%m%d")

			else:
				lastindex= trade_df.index(last_date_string)
				last_yetd_date_string=trade_df[lastindex-1]
				break

		print(last_yetd_date_string,last_date_string)#最近交易日
		last_date_string='20231229'
		last_yetd_date_string='20231228'

		#复盘  最高涨停连板高度 角度，解读市场信息
		highest连板=每日最高连板数.每日最高连板数类()
		#昨日  最高涨停连板高度
		high连板高度_ystd=highest连板.get_day_每日最高连板数_wencai( tradeday=last_yetd_date_string)
		#今日  最高涨停连板高度
		high连板高度_last=highest连板.get_day_每日最高连板数_wencai( tradeday=last_date_string)
		high连板高度_last_龙头股=highest连板.get_day_每日最高连板数_龙头股_wencai( tradeday=last_date_string)
		high连板高度_last_num=len(high连板高度_last_龙头股)

		print(high连板高度_last_龙头股)
		txt_str='今天有{}空间板龙头，最高涨停连板数是{}，相比昨天{}。'
		#比较看出
		if(high连板高度_last > high连板高度_ystd):#最新日大于上一个交易日
			txt_str.format(high连板高度_last_num,high连板高度_last,'空间开拓，积极信号')
		elif(high连板高度_last == high连板高度_ystd):
			txt_str.format(high连板高度_last_num,high连板高度_last,'空间维持，中性信号')

		else:
			txt_str.format(high连板高度_last_num,high连板高度_last,'空间压制，风险信号')

		#早盘竞价情况，给今天提示信号
		for stock in high连板高度_last_龙头股:
			#print(last_date_string)
			stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock, period="daily", start_date=last_yetd_date_string, end_date=last_date_string, adjust="qfq")
			#print(stock_zh_a_hist_df['开盘'][0])
			#print(stock_zh_a_hist_df.columns)
			lastday_open=stock_zh_a_hist_df['开盘'][1]#最近交易日开盘价
			lastday_ystd_close=stock_zh_a_hist_df['收盘'][0]#上一个交易日收盘价
			lastday_开盘涨幅=round((lastday_open/lastday_ystd_close-1),4)
			print(lastday_开盘涨幅)

			#竞价情况
			txt_str=txt_str+'/n /t  {}:今日竞价开盘涨幅{}，{}。'
			if(lastday_开盘涨幅>0):
				txt_str.format(stock,lastday_开盘涨幅,'积极信号,涨幅越大，积极信号越强，越能激发做多情绪，利于今天打板资金敢于打板封板')
			elif(lastday_开盘涨幅==0):
				txt_str.format(stock,lastday_开盘涨幅,'没有溢价，就不利于给今天打板资金信心去打板')
			else:
				txt_str.format(stock,lastday_开盘涨幅,'开盘弱，分歧，弱转强，越低，说明越恐慌，不利于今天个股走势，不利于激活市场打板做多热情')


		#大长腿情况
		for stock in high连板高度_last_龙头股:
			#print(last_date_string)
			stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stock, period="daily", start_date=last_yetd_date_string, end_date=last_date_string, adjust="qfq")
			#print(stock_zh_a_hist_df['开盘'][0])
			#print(stock_zh_a_hist_df.columns)
			#lastday_open=stock_zh_a_hist_df['开盘'][1]#最近交易日开盘价
			lastday_low=stock_zh_a_hist_df['最低'][1]#最近交易日开盘价
			lastday_close=stock_zh_a_hist_df['收盘'][1]#最近交易日收盘价
			lastday_ystd_close=stock_zh_a_hist_df['收盘'][0]#上一个交易日收盘价
			lastday_大长腿=round(((lastday_close-lastday_low)/lastday_ystd_close-1),4)
			#print(lastday_大长腿)

			#竞价情况
			txt_str=txt_str+'/n /t  {}:振幅{}，{}。'
			if(lastday_大长腿>0.15):
				txt_str.format(stock,lastday_大长腿,'大长腿，看似积极信号，情绪加速，但是也是透支表现，持续大长腿，退潮也是核按钮剧烈')
			elif(lastday_大长腿==0):
				#txt_str.format(stock,lastday_大长腿,'没有溢价，就不利于给今天打板资金信心去打板')
				pass
			else:
				txt_str.format(stock,lastday_大长腿,'高开高走，情绪不错')
				pass

			#不好量化。只能是手动笔记，在网页中添加提醒，自己这里要手动关注这些角度，手动笔记。方法是增加一个标签，鼠标移动到就显示，或者点击就显示内容文字，
			#再次点击就隐藏这样不占用网页空间

			#前30min博弈细节情况要关注的角度总结，
			#前30min和大盘走势关系
			#整天分时走势和大盘关系



			#不好量化。只能是手动笔记，在网页中添加提醒，自己这里要手动关注这些角度，手动笔记。方法是增加一个标签，鼠标移动到就显示，或者点击就显示内容文字，
			#再次点击就隐藏这样不占用网页空间

			#前30min博弈细节情况要关注的角度总结，
			#前30min和大盘走势关系
			#整天分时走势和大盘关系


		#昨天复盘工作，网站，快速选择题，填写列表，各种预判工作，预判竞价，预判收盘，预判各种走势量化！
		#
		#早盘竞价9:25使用这个昨日预判，得到所谓超预期信号，弱，强，？说明昨天市场整体多空力量、观望离场力量，情绪反应是什么，发现异动信号，但是这里需要预判是啥，才能得到超预期，自己可能不够格准确
		#
		#收盘后，比较昨日预期和实际情况，得到自己预判情况，对错误的，分析。完善自己思维和代码！
		 

		#为了形成自己预判，然后得到所谓超预期。这先不管是否超预期。
		#而是复盘工作要盯着这几个角度，然后分析数据，得到市场当下状态情绪状态，筹码和资金状态，，然后预测预判明天买卖行为
		#然后竞价佐证买卖行为或者超预期，就总结失望，
		#
		#观察角度（1）竞价开出来情况，

	    #开盘后走势5min、15min、30min是否有符合预期，是怎么变化和博弈的，反应市场情绪，跟其他资金一起，看博弈资金情况
	    
	    #个股分时多空博弈，个股分时和大盘分时，个股和板块联动(很多时候板块不纯，不如白酒、证券银行，概念板块不好用这种信号)，
	    #个股和其他个股联动或跷跷板（人气股和各个板块龙头花在做一个图），个股和大盘联动和跷跷板

	    #需要图表，包含所有涨停股个股，大盘分时，板块分时，然后自己点击看，太复杂，以后再说，应该足够了！

	    #

	    #需要漫长时间学习，然后量化工作，
	    #




        #实时盯盘处理，就是9:25竞价出来，自动化工具。爬取数据得到复盘竞价数据，然后自动分析形成结论，很多角度，自动得到结果，
        #笔记自己思考更加全面。然后得到机会股，风险提示等。！！

		#昨天龙头空间板竞价情况反映，昨天多空力量博弈在情况，竞价数据爬取看看看有没有
		#昨天自己选股观察标的
		#昨天各个板块龙头标的
		#


		#今日  最高涨停连板高度 信息解读

	def get_笔记_cls_分时叠加图(self,blkname,tradeday,src='./财联社每日涨停复盘/static/'):#get_chart_blk_stocks_分时叠加()得到的html，做了做笔记，这里获取然后跟这里代码自动获得的笔记对比，
		tempnotepath='C:\\Users\\DELL\\Desktop\\stk\\modules\\stkPV\\财联社每日涨停复盘\\static\\临时笔记  '
		print('关闭笔记页面，并保存到 ' +tempnotepath)
		print('关闭笔记页面，并保存到 ' +tempnotepath)
		print('关闭笔记页面，并保存到 ' +tempnotepath)
		#看看自己遗漏和新增的，新增就是要量化的角度，完善代码，同时提醒自己有的地方今天没有注意到
		#读取src下文件，
		files = [f for f in os.listdir(src) if os.path.isfile(os.path.join(src, f))]#获取所有文件名字
		files =[ f for f in files  if  tradeday in f ]#最新一个交易日的文件list
		#print(files)

		notefiles = [f for f in os.listdir(src+'/临时笔记') if os.path.isfile(os.path.join(src+'/临时笔记', f))]#获取所有文件名字
		notefiles =[ f for f in notefiles  if  tradeday in f ]#最新一个交易日的文件list

		notefiles =[ f for f in notefiles  if  blkname in f ]#最新一个交易日的文件list
		if(len(notefiles)!=1):
			print('error namenote')
			result=None
		else:

			with open(src+'/临时笔记/'+notefiles[0], 'r',encoding='utf-8') as f:
				result=f.read()

		print(result)



if __name__ == '__main__':
	#涨停股复盘
	print('第一步，执行财联社代码，整理图片信息，保存今日复盘基本情况基础数据 ')
	#财联社涨停分析.财联社类( ).get_chart_blk_stocks_分时叠加(tradeday='20231229',iswebopen=1)
	print('第二步，各种分时图叠加大盘等html生成，然后自己直观的观察数据和分析， 做手动笔记')
	print('第二步，做手动笔记')
	print('第二步，先自己观察和思考，看到最直观东西，不要被代码复盘角度制约，所以后面再看，先自己观察和思考')
	print('第二步，做手动笔记')
	
	
	print('第三步，执行涨停板复盘代码，生成复盘笔记')
	#复盘涨停板类().最高涨停连板高度()
	
	print('第四步，合并手动复盘笔记和代码复盘笔记，然后手动再次复盘比较两个笔记，')
	print('第四步，新增的角度内容，要量化完善复盘代码，遗漏的角度，再次思考市场影响')
	print('第四步，直到自己先写笔记全部被代码包含，甚至自己好多角度都没有关注到和回想到和关注到,说明足够复盘代码足够完善了')
	
	复盘涨停板类().get_笔记_cls_分时叠加图(tradeday='20231229',blkname='市场焦点股')



	

	pass
		