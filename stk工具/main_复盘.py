#最后在打包方便调用
import sys
import os
import akshare as ak
import shutil
current_dir = os.path.dirname(os.path.abspath(__file__)) 
#print(current_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

#模块根目录要在运行中写入path，然后可以通过
#from  common import DataStruct 等类似绝对路径来读取引入模块，但是测试单独模块式后可能还是有问题，
#所以单独在sys.path.append(parent_dir)   根目录就是了，后面在注销掉，影响不大！

from datetime import datetime,timedelta

import modules.noteplt as noteplt
from modules.stkPV import sktPriceVol
from modules.stkPV import 概念板块
from modules.可视化stock.stocks可视化 import HC可视化
from common import DataStruct,TimePoint

#notes中添加一个list来回顾历史的notes页，可以通过执行复制就是了，新生成时候这问题不大应该
#就是notes保存历史在一个文件夹，然后添加到list是可以@
from modules.noteplt import 复盘笔记类 
from lunardate import LunarDate
import lunardate
import webbrowser


from modules.stkPV.获取各类数据函数 import 每日涨跌数
from modules.stkPV.获取各类数据函数 import 每日上证指数黄白线分钟数据
from modules.stkPV.获取各类数据函数 import 每日最高连板数
from modules.stkPV.获取各类数据函数 import 每日两市成交额
from modules.stkPV.获取各类数据函数 import 每日北向资金 
from modules.stkPV.获取各类数据函数 import 每日涨跌停家数

from modules.stkPV import 动态监控
"""
This is a docstring for your module.
"""
class 复盘笔记():
	    """
    This is a docstring for MyClass.
    """
	def __init__(self):

		pass

	def init_files_templates_废弃但是好用(self,src_path='./modules/noteplt',des_path='./out/',init=1):#init=1删除目标位置对应所有文件，只是目标日期文件夹
		#初始化复盘笔记文件，这里是从文件中复制过来模板，然后再次基础上修改尽量不要弄乱模版
		

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		todaynow = datetime.now()
		today_date_string = todaynow.strftime("%Y%m%d")
		last_date_string =today_date_string
		while True:
			if(last_date_string not in trade_df ):
				todaynow=todaynow-timedelta(days=1)#最近上一个交易日
				last_date_string = todaynow.strftime("%Y%m%d")
			else:
				break
		#print(last_date_string)#最近交易日

		des_absdir=des_path+last_date_string#目标日期文件夹

		##判断目的地是否存在，不存在创建，且目标日期文件夹
		if(os.path.exists(des_absdir)):
			if(init==1):#删除重建
				shutil.rmtree(des_absdir)
				shutil.copytree(src_path+'/help-center', des_absdir+'/help-center')
				shutil.copytree(src_path+'/static', des_absdir+'/static')
				shutil.copy2(src_path+'/main.html', des_absdir)

			else:#不重建，但是需要判断是否完整
				dcmp = filecmp.dircmp(src_path+'/help-center', des_absdir+'/help-center')
				# 复制不同的文件
				for name in dcmp.diff_files:
				    source_file = os.path.join(src_path, name)
				    destination_file = os.path.join(des_absdir, name)
				    shutil.copy2(source_file, destination_file)
				    print(f"Copied: {source_file} -> {destination_file}")
				# 递归比较子目录
				for sub_dir in dcmp.subdirs.values():
				    sub_source_dir = os.path.join(src_path, sub_dir)
				    sub_destination_dir = os.path.join(des_absdir, sub_dir)
				    compare_and_copy(sub_source_dir, sub_destination_dir)

				dcmp = filecmp.dircmp(src_path+'/static', des_absdir+'/static')
				# 复制不同的文件
				for name in dcmp.diff_files:
					source_file = os.path.join(src_path, name)
					destination_file = os.path.join(des_absdir, name)
					shutil.copy2(source_file, destination_file)
					print(f"Copied: {source_file} -> {destination_file}")
				# 递归比较子目录
				for sub_dir in dcmp.subdirs.values():
					sub_source_dir = os.path.join(src_path, sub_dir)
					sub_destination_dir = os.path.join(des_absdir, sub_dir)
					compare_and_copy(sub_source_dir, sub_destination_dir)

				# 检查两个文件是否相同
				if not filecmp.cmp(src_path+'/main.html',  des_absdir+'/main.html', shallow=False):
			        # 如果文件不同，复制并替换目标文件
					shutil.copy2(source_file, destination_file)


		else:
			#os.makedirs(des_absdir)#创建日期目标文件
			shutil.copytree(src_path+'/help-center', des_absdir+'/help-center')
			shutil.copytree(src_path+'/static', des_absdir+'/static')
			shutil.copy2(src_path+'/main.html', des_absdir)


	############################################################################################################
	##
	##  同花顺，财联社等新增板块及时关注研究，快鱼吃慢鱼
	##
	##关注新的渠道板块，分类，需要人气足够才行，关注才能容易共识，很小众的分类没有关注共识合力，分类再好精巧意义不大
	###########################################################################################################
	def 新增概念板块(self,isopenweb=0,page_type=20):
		概念板块1=概念板块()#新增板块的分析，放在有道云笔记中，这里引用链接就好，需要加个空链接，然后手动改保存，下次就有！
		out2=概念板块1.get_新增概念板块_同花顺(dayset=30)#
		#print("同花顺新增板块：",out2)
		out1=概念板块1.get_新增概念板块_财联社(dayset=30)#代码爬取网站带时间，所以比较半年内输出，所以控制了持续输出且控制半年内
		#print("财联社新增板块：",out1)
		#选择特定时间内写入notes中做的中间处理
		temp=DataStruct()#笔记格式公共类
		空格换行=["********************************************************************"]
		temp.append([[out1,空格换行,out2],""],keys=["blocks"])
		temp.append([[out1,'\n\n',out2],""],keys=["blocks"])
		#写入到notes中 附带链接
		#print(temp.data)
		复盘笔记类().notes_stocks(data=temp.data,page_type=20,isopenweb=isopenweb) #page_type，设置需要改那个页面内容


	############################################################################################################
	##
	##  时间点
	##
	## 某个时间点是涉及某个事件才重要，所以很多人关注时间点背后的事件，涉及到重要人、事件和文件，达成共识时间点和窗口
	##
	###########################################################################################################

	def 重要时间点(self,isopenweb=0,page_type=24):
		temp=TimePoint()
		now = datetime.now()
		# 提取月份
		current_month = now.month
		#print("当前月份是:", current_month)
 
		# 获取下一个农历春节的阳历时间
		next_spring_festival_lunar1 =lunardate.LunarDate(now.year, 1, 1, 0)
		next_spring_festival_lunar2 =lunardate.LunarDate(now.year+1, 1, 1, 0)
		next_spring_festival_solar1 = next_spring_festival_lunar1.toSolarDate()
		next_spring_festival_solar2 = next_spring_festival_lunar2.toSolarDate()
		#print(next_spring_festival_solar1,next_spring_festival_solar2)
		if(now.date() >  next_spring_festival_solar1):
			next_spring_festival_solar = next_spring_festival_solar2.strftime("%Y%m%d")
		else:
			next_spring_festival_solar = next_spring_festival_solar1.strftime("%Y%m%d")
		#print(next_spring_festival_solar,type(next_spring_festival_solar))
 
		if(now >= datetime.strptime(str(now.year)+'0815','%Y%m%d') and  now <= datetime.strptime(str(now.year)+'1015','%Y%m%d')):
			temp.append(['周期性：大环境周期性缺钱，大盘周期性震荡缩量趋势，大盘大概率要震荡跌','https://note.youdao.com/s/VGwgwulB'],keys=["time"])
		
		if(now >= datetime.strptime(str(now.year)+'1201','%Y%m%d') and  now <= datetime.strptime(next_spring_festival_solar,'%Y%m%d')):
			temp.append(['周期性：12月底很多行业年底结算，年报等，持续到农历春节也是缺钱；大环境周期性缺钱，大盘周期性震荡缩量趋势，大盘大概率要震荡跌','https://note.youdao.com/s/VGwgwulB'],keys=["time"])


		if(current_month==12):#12月
			temp.append(['12月三大会议解读','https://note.youdao.com/s/KYAD9bWe'],keys=["time"])


		复盘笔记类().notes_stocks(data=temp.data,page_type=24,isopenweb=isopenweb) #page_type，设置需要改那个页面内容

	############################################################################################################
	##
	##  时间点
	##
	## 某个时间点是涉及某个事件才重要，所以很多人关注时间点背后的事件，涉及到重要人、事件和文件，达成共识时间点和窗口
	##
	###########################################################################################################

	def 情绪指标(self,tradeday='',isopenweb=0,page_type=25):
		temp=[]#笔记格式公共类
		clasUP=每日涨跌数.每日上涨数类()
		data=clasUP.get_day_每日上涨数_wencai(tradeday=tradeday)

		#print(data)
		# data=s.get_days_每日上涨数_wencai('20231214','20231219')
		# print(data)

		if(data>=4000):
			temp.append('上涨家数：{},情绪极致高潮。大概率大量个股明天回撤收阴，熊市越深越早卖信号甚至盘中卖，注意早盘高抛'.format(data))
		elif(data>=3000 ):
			temp.append('上涨家数：{},情绪小高潮。如果资金没有增量小心明天回撤，大概率明天很多收阴'.format(data))
		
		#这里有个复盘是盘中的上涨家数，不一定是尾盘给的，所以需要盘中数据，但是没有有找到好接口

		clasDW=每日涨跌数.每日下跌数类()
		data=clasDW.get_day_每日下跌数_wencai(tradeday=tradeday)
		#print(data)
		# data=clasDW.get_days_每日下跌数_wencai('20231214','20231219')
		# print(data)
		if(data>=4000):
			temp.append('下跌家数：{},情绪极致冰点。明天概率修复，但是修复力度不确定。大修复就是普涨，小修复就是小部分涨，可能很多继续继续跌'.format(data))			
		elif(data>=3000):
			temp.append('下跌家数：{},情绪小冰点。'.format(data))			
		复盘笔记类().notes_stocks(data={'emotional_cycle':temp},page_type=25,isopenweb=isopenweb) #page_type，设置需要改那个页面内容

		#这里是不是可以添加连接，给图表，看历史冰点记录？？或者叠加，
		#涨跌冰点同花顺能看到，没看出太多意义，

		data=每日上证指数黄白线分钟数据.上证指数黄白线分钟数据类().get_day_上证指数黄白线分钟数据(tradeday=tradeday)
		#print(data)
		白黄差30=[ float(item[1])-float(item[3]) for item in data if(float(item[1])-float(item[3])>=30) ]#白减黄大于30
		白黄差20=[ float(item[1])-float(item[3]) for item in data if(float(item[1])-float(item[3])>=20 and float(item[1])-float(item[3])<30) ]#白减黄大于30
		白黄差10=[ float(item[1])-float(item[3]) for item in data if(float(item[1])-float(item[3])>=10 and float(item[1])-float(item[3])<20) ]#白减黄大于30
		if(len(白黄差30)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证白线-黄线>30,情绪极端恶劣']},page_type=25,isopenweb=isopenweb)
		elif(len(白黄差20)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证白线-黄线>20,情绪恶化谨慎']},page_type=25,isopenweb=isopenweb)
		elif(len(白黄差10)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证白线-黄线>10,情绪变弱注意']},page_type=25,isopenweb=isopenweb)

		#print(data)
		黄白差30=[ float(item[3])-float(item[1]) for item in data if(float(item[3])-float(item[1])>=30) ]#白减黄大于30
		黄白差20=[ float(item[3])-float(item[1]) for item in data if(float(item[3])-float(item[1])>=20 and float(item[3])-float(item[1])<30) ]#白减黄大于30
		黄白差10=[ float(item[3])-float(item[1]) for item in data if(float(item[3])-float(item[1])>=10 and float(item[3])-float(item[1])<20) ]#白减黄大于30
		if(len(黄白差30)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证黄线-白线>30,情绪极致高潮']},page_type=25,isopenweb=isopenweb)
		elif(len(黄白差20)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证黄线-白线>20,情绪高潮留意']},page_type=25,isopenweb=isopenweb)
		elif(len(黄白差10)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证黄线-白线>10,情绪变好留意']},page_type=25,isopenweb=isopenweb)



		data=每日最高连板数.每日最高连板数类().get_day_每日最高连板数_wencai( tradeday=tradeday)
		if(data==2):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['最高连板是 2连板 情绪极致冰点，积极试错首板和2板，操作打板龙头 ']},page_type=25,isopenweb=isopenweb)
		elif(data==3):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['最高连板是 3连板 情绪极致冰点，积极试错，操作打板龙头 ，可能恶化到2板，']},page_type=25,isopenweb=isopenweb)			



	############################################################################################################
	##
	##  游资炒作研究后得到一些结论，量化后或者增加提示
	##
	## 某个时间点是涉及某个事件才重要，所以很多人关注时间点背后的事件，涉及到重要人、事件和文件，达成共识时间点和窗口
	##
	###########################################################################################################


	def 游资规律研究(self):


		temp=DataStruct()
		now = datetime.now()
		# 提取月份
		current_month = now.month



		#跨年龙 概念板块，时间点提醒，添加笔记分析，逻辑，时间点到了，需要看笔记，看预测预判板块是否有机会能炒作起来？都需要当下判断，不要潜伏，
		#需要当下动态评估，这都在笔记里有研究，	
		#print("当前月份是:", current_month)
		if (now.month ==11 and  now.day>=15) or (now.month ==12 and now.day <=25) :#25号之前都没有酝酿，算了这个板块
			temp.append(['跨年概念','https://note.youdao.com/s/JLw4NhhW'],keys=["blocks"])
		







	def 日常复盘笔记_市场核心摘要(self,isopenweb=0):


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

		print(last_date_string)#最近交易日


		#爬取各种数据
		data={}
		last_index_money=每日两市成交额.每日两市成交额类().get_day_每日两市成交额_ak( tradeday=last_date_string )
		last_yetd_money=每日两市成交额.每日两市成交额类().get_day_每日两市成交额_ak( tradeday=last_yetd_date_string )
		#print(last_index_money,last_yetd_money)
		data['今日大盘成交额']=last_index_money

		a = int(last_index_money) - int(last_yetd_money)
		data['增减大盘量能']='{}'.format( '放量' + str(a) if a > 0 else '缩量' + str(a) )

		#这里应该有个类类似其他文件爬取数据，但是这里先这样，以后在增加保存本地的代码
		#

		data['北向资金']=每日北向资金.每日北向资金类().get_day_每日北向资金_dfcf(tradeday=last_date_string)
		data['上涨家数']=每日涨跌数.每日上涨数类().get_day_每日上涨数_wencai(tradeday=last_date_string)
		data['下跌家数']=每日涨跌数.每日下跌数类().get_day_每日下跌数_wencai(tradeday=last_date_string)
		data['实际涨停']=每日涨跌停家数.每日涨跌停家数类().get_day_每日涨跌停家数_wencai( tradeday=last_date_string)[0]
		data['实际跌停']=每日涨跌停家数.每日涨跌停家数类().get_day_每日涨跌停家数_wencai( tradeday=last_date_string)[1]

		
		复盘笔记类().notes_stocks(data={'daily_notes':[data,]},page_type=12,isopenweb=isopenweb)			


	def 复盘_消息面(self):
		#这里如果是节前复盘明天要开市，这里做的笔记提示角度
		txt='关注假期消息，如果没什么大的消息，市场也是沿着原有的轨迹运行；如果有新的大消息，注意市场节奏变化推演'
		
	def 复盘_大盘(self,tradeday='20240103',isopenweb=0):#tradeday肯定是交易日，只是有没有开市的问题

		大盘分时txt=复盘大盘分时_程序笔记类().复盘大盘分时类().get笔记_复盘大盘分时_day(tradeday=tradeday,data=大盘分时数据,ydata=大盘分时数据_yetd)
		复盘笔记类().notes_stocks(data={'daily_dapan_notes':[大盘分时txt]},page_type=12,ttype='daily_dapan_notes',isopenweb=isopenweb)			

		

		
		#每日缩量提示

		##月初缩量提示不是好事，明天能否放量修复就很重要



	def 生成复盘文档(self,src_path='./modules/noteplt',des_path='./out/',isopenweb=0): #init=1,不是迭代添加html内容，而是从模板重建
		'''删除旧文件'''
		directory='./modules/noteplt/help-center/'
		try:
	        # 获取指定路径下的所有文件和子目录
			file_list = os.listdir(directory)
			#print(file_list)
	        # 遍历文件列表
			for file_name in file_list:
				file_path = os.path.join(directory, file_name)

	            # 判断是否为文件，如果是则删除
				if os.path.isfile(file_path):
					os.remove(file_path)
					print(f"文件 {file_path} 已删除")

			print(f"所有文件在路径 {directory} 下已删除")

		except Exception as e:
			print(f"删除文件时发生错误: {e}")


		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		todaynow = datetime.now()
		last_date=todaynow
		today_date_string = todaynow.strftime("%Y%m%d")
		last_date_string =today_date_string
		while True:
			if(last_date_string not in trade_df ):
				last_date=last_date-timedelta(days=1)#最近上一个交易日
				last_date_string = last_date.strftime("%Y%m%d")
			else:
				break
		#print(last_date_string)#最近交易日

		print("start 日常复盘笔记")
		self.日常复盘笔记_市场核心摘要()
		#把信息存到模板html中
		print("start 新增概念板块")
		self.新增概念板块()
		print("start 重要时间点")
		self.重要时间点()
		print("start 情绪指标")
		self.情绪指标(tradeday=last_date_string)

		

		#这里思路变化是在模板文件生成结果不再改代码，而是把结果复制过来重命名就好了！
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		todaynow = datetime.now()
		last_date=todaynow
		today_date_string = todaynow.strftime("%Y%m%d")
		last_date_string =today_date_string
		while True:
			if(last_date_string not in trade_df ):
				last_date=last_date-timedelta(days=1)#最近上一个交易日
				last_date_string = last_date.strftime("%Y%m%d")
			else:
				break
		#print(last_date_string)#最近交易日

		des_absdir=des_path+last_date_string#目标日期文件夹

		##判断目的地是否存在，不存在创建，且目标日期文件夹
		if(os.path.exists(des_absdir)):
			#删除重建
			shutil.rmtree(des_absdir)
			shutil.copytree(src_path+'/help-center', des_absdir+'/help-center')
			shutil.copytree(src_path+'/static', des_absdir+'/static')
			shutil.copy2(src_path+'/main.html', des_absdir)
		else:
			#os.makedirs(des_absdir)#创建日期目标文件
			shutil.copytree(src_path+'/help-center', des_absdir+'/help-center')
			shutil.copytree(src_path+'/static', des_absdir+'/static')
			shutil.copy2(src_path+'/main.html', des_absdir)

		if(isopenweb==1):
			webbrowser.open(os.path.dirname(__file__)+'/out/'+last_date_string+'/main.html')










#这个文档好处是，纷杂的工作不用记忆，不用重复，不用切换，不用花很多时间精力，专注更重要东西
#例如，证券个股三连板重要信号，不太容易在同花顺比较方便的得到这个信号，花费心力每天盯着，但是有这个文件，就不用花费，
#而是需要关注新指标增删就好了，和直接利用结论文档复盘，
#很多指标自己都容易忘记，错过很多机会，或者说太多指标浪费太多心力去查看，导致自己每天忙在切换和查看上，浪费心力，不是每天都有信号，时间长了
#倦怠。所以需要工具来解决重复工作！更多时间精力在更重要信号思考上，而不是重复查看是否有信号上！
#
#
#不同工具配合使用，虽然想集成，但是很多不好在同花顺实现，不好在python代码中，能实现就实现，不要强求，集成一大部分就好了！
#
#
# ***需要监控的指标做好分类，可以先写，先用，积累一段时间后，后面在分类，毕竟太少不好精确分类！
#分类后方便修改查找！
#
#********添加一个指标，功能，都要做好记录备注使用方便后面用，和上传github，做好保存防止丢失
#每个指标标题后面加上链接，能链接到有道云笔记，看这个指标的notes注解，和跟踪注解，和指标经典
#
#
#输出信号分类别和级别的！
#可以交叉重复无所谓的！就是说信号即是个股信号也是板块信号，也是大盘信号，那么三个地方都输出就是，无所谓
#所以给出不同类型的数组？看看信号输出哪里就是了！

#a=common.DataStruct()
#print(a.data) 


def fun1():
	#收集股票价量异动信息
	a=sktPriceVol()
	#out=a.stk_pv_monitor()#所有监控#a.data也行
	#print(out)
	#res=a.test_txt()#测试代码
	#print(res.data)

	#保存html文档notes
	#noteplt.notes_stocks(data=out.data,page_type=20) #page_type，设置需要改那个页面内容


	#获取并格式化 折线图数据，每日最高板折线图
	连板折线data=a.多日连板统计(start="20231115",end="20231204")
	#连板折线tradedays = 连板折线data["date"][   连板折线data['date'].index("2023-11-15") : 连板折线data['date'].index("2023-12-01")+1  ]#g根据输入获得tradedays
	连板折线tradedays = 连板折线data["date"][   连板折线data['date'].index("2023-11-15") :  ]#g根据输入获得tradedays
	连板折线dydata=[]
	for day in 连板折线tradedays:#按照时间顺序，读取，然后push
		#print(day)
		连板折线dydata.append(连板折线data['data'][day])

	#获取天地板信息
	aa=sktPriceVol().多日天地板(start="20231120",end="20231204")
	label天地板=[]
	for day in aa['date']:
		if(aa['data'][day] ):#非空字典
			label天地板.append(aa['data'][day])
		##处理标签的位置，让标签在折线图中的每日最高板位置（y值位置）
	for idata in label天地板:
		tempdate=idata['date']
		temp=[ i[1] for i in 连板折线dydata if(i[0]==tempdate)]
		idata['yValue']=temp[0]


	#获取地天板信息
	aa=sktPriceVol().多日地天板(start="20231120",end="20231204")
	label地天板=[]
	for day in aa['date']:
		if(aa['data'][day] ):#非空字典
			label地天板.append(aa['data'][day])
		##处理标签的位置，让标签在折线图中的每日最高板位置（y值位置）
	#print(连板折线dydata)
	for idata in label地天板:
		tempdate=idata['date']
		#print(datetime.fromtimestamp(int(tempdate)/1000))
		#print(idata)
		temp=[ i[1] for i in 连板折线dydata if(i[0]==tempdate)]
		idata['yValue']=temp[0]

	#可视化，形成html，形成折线图，且画带标签的
	HC可视化().get_标注曲线(dynamic_data=连板折线dydata,labelxy天地板=label天地板,labelxy地天板=label地天板,name="情绪连板",isopen=1)





if __name__ == '__main__':
	#这里不要放在一个函数，而是一步某块一个模块，然后打印输出提示到哪里了！！！

	复盘笔记单独一个，且不同角度复盘要分开，不要掺和在一起，就是一角度笔记一个地方，方便管理，不怕多次爬取调用，规划好数据流就好

	复盘其他东西都是单独一个不要混
 
	#增加执行到哪里提示
	#每日更新数据类

	#动态监控.动态监控类().复盘股价监控(tradeday='20240104')
	a=复盘笔记()
	#a.复盘_大盘()
	a.生成复盘文档(isopenweb=1)

	#webbrowser.open(os.path.dirname(__file__)+'/out/'+'20231229'+'/main.html')