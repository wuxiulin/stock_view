#路径管理，sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#添加到os.path.dirname(,一直到stk这个跟目录，然后sys.path.append(，把stk加进入
#然后通过from xxx  import    from  xxx.xxx  import   from xxx.xxx.xxx import   方式调用
#所以这就就是统一sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))  这里统一到stk
#然后from xxx  import    from  xxx.xxx  import   from xxx.xxx.xxx import   就能统一从stk根目录开始，
#每个文件中，就可以不用再头部放一个sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))。
#所有代码导入一次就好，在main.py中，如果调试， 临时添加sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
#但是调试每个部分时候要临时天添加根目录，最后删除是否问题不大



import sys
import os
#添加根目录
current_dir = os.path.dirname(os.path.abspath(__file__)) 
#print(current_dir)
sys.path.append(current_dir)



import akshare as ak
import shutil
from datetime import datetime,timedelta
from lunardate import LunarDate
import lunardate
import webbrowser


from modules.stkPV.stkPrcVol import stkPriceVol
from modules.stkPV.板块 import 概念板块
from modules.可视化stock.stocks可视化 import HC可视化
from common import DataStruct,TimePoint

#notes中添加一个list来回顾历史的notes页，可以通过执行复制就是了，新生成时候这问题不大应该
#就是notes保存历史在一个文件夹，然后添加到list是可以@
from modules.noteplt.notes_template import 复盘笔记类

from modules.stkPV.获取各类数据函数.每日涨跌数 import 每日上涨数类
from modules.stkPV.获取各类数据函数.每日涨跌数 import 每日下跌数类
from modules.stkPV.获取各类数据函数. 每日上证指数黄白线分钟数据 import  上证指数黄白线分钟数据类
from modules.stkPV.获取各类数据函数.每日最高连板数  import  每日最高连板数类 
from modules.stkPV.获取各类数据函数.每日两市成交额 import  每日两市成交额类
from modules.stkPV.获取各类数据函数.每日北向资金 import  每日北向资金类
from modules.stkPV.获取各类数据函数.每日涨跌停家数 import 每日涨跌停家数类

from modules.stkPV.动态监控 import 动态监控类




from modules.stkPV.大盘复盘.复盘大盘分时 import  复盘大盘分时_程序笔记类
from modules.stkPV.大盘复盘.复盘大盘分时 import  复盘大盘分时_手动复盘类
"""
This is a docstring for your module.
"""
class 复盘笔记():

	def __init__(self):

		pass

	def init复盘(self,directory='./modules/noteplt/help-center/'):  
		#删除临时结果文件，这里已经按照时间保存在out文件夹中了，这里删除是临时文件
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

			print(f"	所有文件在路径 {directory} 下已删除")

		except Exception as e:
			print(f"删除文件时发生错误: {e}")


	def 日常复盘(self ,tradeday):
		print('		笔记_市场核心摘要')
		#爬取各种数据
		data={}
		last_index_money=每日两市成交额类().get_day_每日两市成交额_ak( tradeday=tradeday )
		last_yetd_money=每日两市成交额类().get_day_每日两市成交额_ak( tradeday=tradeday )
		#print(last_index_money,last_yetd_money)
		data['今日大盘成交额']=last_index_money
		a = int(last_index_money) - int(last_yetd_money)
		data['增减大盘量能']='{}'.format( '放量' + str(a) if a > 0 else '缩量' + str(a) )
		#这里应该有个类类似其他文件爬取数据，但是这里先这样，以后在增加保存本地的代码
		data['北向资金']=每日北向资金类().get_day_每日北向资金_dfcf(tradeday=tradeday)
		data['上涨家数']=每日上涨数类().get_day_每日上涨数_wencai(tradeday=tradeday)
		data['下跌家数']=每日下跌数类().get_day_每日下跌数_wencai(tradeday=tradeday)
		data['实际涨停']=每日涨跌停家数类().get_day_每日涨跌停家数_wencai( tradeday=tradeday)[0]
		data['实际跌停']=每日涨跌停家数类().get_day_每日涨跌停家数_wencai( tradeday=tradeday)[1]
		复盘笔记类().notes_stocks(data={'daily_notes':[data,]},page_type=12,ttype='daily_notes')	#读取模版填写	

 	
		print('		每日大盘分时复盘')
		大盘分时txt=复盘大盘分时_程序笔记类().get笔记_复盘大盘分时_day(tradeday=tradeday)
		复盘笔记类().notes_stocks(data={'daily_dapan_notes':[大盘分时txt]},page_type=12,ttype='daily_dapan_notes')			

		
		#每日缩量提示

		##月初缩量提示不是好事，明天能否放量修复就很重要


	def 动态监控(self,tradeday):
		动态监控类().复盘股价监控(tradeday=tradeday)


	def 大盘异动(self):
		pass






	def 板块异动(self):

		print('		正在执行 ：新增概念板块异动')
		概念板块1=概念板块()#新增板块的分析，放在有道云笔记中，这里引用链接就好，需要加个空链接，然后手动改保存，下次就有！
		out2=概念板块1.get_新增概念板块_同花顺(dayset=30)#
		#print("同花顺新增板块：",out2)
		out1=概念板块1.get_新增概念板块_财联社(dayset=30)#代码爬取网站带时间，所以比较半年内输出，所以控制了持续输出且控制半年内
		#print("财联社新增板块：",out1)
		#选择特定时间内写入notes中做的中间处理
		temp=DataStruct()#笔记格式公共类
		空格换行= [ "..................................."]
		temp.append([[out1,空格换行,out2],"https://note.youdao.com/s/4P2lfkZG"],keys=["blocks"])
		#写入到notes中 附带链接
		#print(temp.data)
		复盘笔记类().notes_stocks(data=temp.data,page_type=22,isopenweb=0) #page_type，设置需要改那个页面内容





	def 个股异动(self):
		pass



	############################################################################################################
	##
	##  时间点
	##
	## 某个时间点是涉及某个事件才重要，所以很多人关注时间点背后的事件，涉及到重要人、事件和文件，达成共识时间点和窗口
	##
	###########################################################################################################

	def 时间点(self):
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


		复盘笔记类().notes_stocks(data=temp.data,page_type=24) #page_type，设置需要改那个页面内容




		#游资规律；特殊时间点提示
		temp=DataStruct()
		if (now.month ==11 and  now.day>=15) or (now.month ==12 and now.day <=25) :#25号之前都没有酝酿，算了这个板块
			temp.append(['跨年概念','https://note.youdao.com/s/JLw4NhhW'],keys=["blocks"])



	############################################################################################################
	##
	##  情绪周期
	##
	##  
	##
	###########################################################################################################

	def 情绪周期(self,tradeday ):
		temp=[]#笔记格式公共类
		clasUP=每日上涨数类()
		data=clasUP.get_day_每日上涨数_wencai(tradeday=tradeday)

		#print(data)
		# data=s.get_days_每日上涨数_wencai('20231214','20231219')
		# print(data)

		if(data>=4000):
			temp.append('上涨家数：{},情绪极致高潮。大概率大量个股明天回撤收阴，熊市越深越早卖信号甚至盘中卖，注意早盘高抛'.format(data))
		elif(data>=3000 ):
			temp.append('上涨家数：{},情绪小高潮。如果资金没有增量小心明天回撤，大概率明天很多收阴'.format(data))
		
		#这里有个复盘是盘中的上涨家数，不一定是尾盘给的，所以需要盘中数据，但是没有有找到好接口

		clasDW=每日下跌数类()
		data=clasDW.get_day_每日下跌数_wencai(tradeday=tradeday)
		#print(data)
		# data=clasDW.get_days_每日下跌数_wencai('20231214','20231219')
		# print(data)
		if(data>=4000):
			temp.append('下跌家数：{},情绪极致冰点。明天概率修复，但是修复力度不确定。大修复就是普涨，小修复就是小部分涨，可能很多继续继续跌'.format(data))			
		elif(data>=3000):
			temp.append('下跌家数：{},情绪小冰点。'.format(data))			
		复盘笔记类().notes_stocks(data={'emotional_cycle':temp},page_type=25) #page_type，设置需要改那个页面内容

		#这里是不是可以添加连接，给图表，看历史冰点记录？？或者叠加，
		#涨跌冰点同花顺能看到，没看出太多意义，

		data=上证指数黄白线分钟数据类().get_day_上证指数黄白线分钟数据(tradeday=tradeday)
		#print(data)
		白黄差30=[ float(item[1])-float(item[3]) for item in data if(float(item[1])-float(item[3])>=30) ]#白减黄大于30
		白黄差20=[ float(item[1])-float(item[3]) for item in data if(float(item[1])-float(item[3])>=20 and float(item[1])-float(item[3])<30) ]#白减黄大于30
		白黄差10=[ float(item[1])-float(item[3]) for item in data if(float(item[1])-float(item[3])>=10 and float(item[1])-float(item[3])<20) ]#白减黄大于30
		if(len(白黄差30)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证白线-黄线>30,情绪极端恶劣']},page_type=25)
		elif(len(白黄差20)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证白线-黄线>20,情绪恶化谨慎']},page_type=25 )
		elif(len(白黄差10)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证白线-黄线>10,情绪变弱注意']},page_type=25 )

		#print(data)
		黄白差30=[ float(item[3])-float(item[1]) for item in data if(float(item[3])-float(item[1])>=30) ]#白减黄大于30
		黄白差20=[ float(item[3])-float(item[1]) for item in data if(float(item[3])-float(item[1])>=20 and float(item[3])-float(item[1])<30) ]#白减黄大于30
		黄白差10=[ float(item[3])-float(item[1]) for item in data if(float(item[3])-float(item[1])>=10 and float(item[3])-float(item[1])<20) ]#白减黄大于30
		if(len(黄白差30)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证黄线-白线>30,情绪极致高潮']},page_type=25 )
		elif(len(黄白差20)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证黄线-白线>20,情绪高潮留意']},page_type=25 )
		elif(len(黄白差10)>0):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['上证黄线-白线>10,情绪变好留意']},page_type=25 )



		data=每日最高连板数类().get_day_每日最高连板数_wencai( tradeday=tradeday)
		if(data==2):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['最高连板是 2连板 情绪极致冰点，积极试错首板和2板，操作打板龙头 ']},page_type=25 )
		elif(data==3):
			复盘笔记类().notes_stocks(data={'emotional_cycle':['最高连板是 3连板 情绪极致冰点，积极试错，操作打板龙头 ，可能恶化到2板，']},page_type=25 )			



	 
		





	def Dest复盘(self,src_path='./modules/noteplt',des_path='./out/'):
		
		#获取最新交易日，创建 xxxx/out/最新交易日文件夹,复制模版中的css，js文件
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



	def 手动复盘笔记(self,tradeday):
		print('开始【手动复盘】，之后【程序复盘】')
		print('如何复盘笔记：https://note.youdao.com/s/VUus438k')

		print('		大盘分时复盘')
		print('			网页笔记txt文档保存到   \\stk\\modules\\stkPV\\大盘复盘\\static\\'+tradeday )
		复盘大盘分时_手动复盘类().get_chart_今日影响大权重分时叠加图(tradeday=tradeday,iswebopen=1)
		print('			网页笔记txt文档保存到   \\stk\\modules\\stkPV\\大盘复盘\\static\\'+tradeday )
		复盘大盘分时_手动复盘类().get_chart_今日影响大行业板块分时叠加图(tradeday=tradeday,iswebopen=1)
		复盘大盘分时_手动复盘类().get_chart_多日影响大权重分时叠加图(tradeday=tradeday,iswebopen=1 )
		复盘大盘分时_手动复盘类().get_chart_多日影响大行业板块分时叠加图(tradeday=tradeday,iswebopen=1)




	def 程序复盘笔记(self,tradeday):

		print('初始化复盘')
		笔记.init复盘(directory='./modules/noteplt/help-center/')

		print('开始执行 ：日常复盘')
		笔记.日常复盘(tradeday=tradeday)


		print('开始执行 ：动态监控')
		print('		正在执行：动态监控类.复盘股价监控()')#打印输出提示执行到哪个模块了
		笔记.动态监控(tradeday=tradeday)



		print('开始执行 ：大盘异动')
		笔记.大盘异动()




		print('开始执行 ：板块异动')
		笔记.板块异动()




		print('开始执行 ：个股异动')
		笔记.个股异动()



		print('开始执行 ：时间点')
		笔记.时间点()



		print('开始执行 ：情绪周期')
		笔记.情绪周期(tradeday=tradeday)
	 
		#在out中创建日期文件夹，然后从模板文件中把产生的html，复制到out中，按照时间分类保存
		笔记.Dest复盘(src_path='./modules/noteplt',des_path='./out/')
		webbrowser.open(os.path.dirname(__file__)+'/out/'+tradeday+'/main.html')				



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


	#应该有个接口，只更新今天所有数据
	#然后再运行复盘代码，但是这样有时候没有必要，所以更新数据交叉在复盘代码中灭有大影响
	#这里不要放在一个函数，而是一步某块一个模块，然后打印输出提示到哪里了！！！
	#复盘笔记单独一个，且不同角度复盘要分开，不要掺和在一起，就是一角度笔记一个地方，方便管理，不怕多次爬取调用，规划好数据流就好
	#复盘其他东西都是单独一个不要混
	#代码整理，就是这里调用到类，然后直接用就可以，代码简单点   from modules.stkPV.获取各类数据函数.每日涨跌停家数 import 每日涨跌停家数类
	#每日涨跌停家数类()  __init__ 文件清空，不要有内容





if __name__ == '__main__':

	#这里如果是节前复盘明天要开市，这里做的笔记提示角度
	txt='关注假期消息，如果没什么大的消息，市场也是沿着原有的轨迹运行；如果有新的大消息，注意市场节奏变化推演'
		
	#获取期间交易日list
	trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
	trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
	todaynow = datetime.now()
	last_date=todaynow
	tradeday =todaynow.strftime("%Y%m%d")
	tradeday =''
	#print(tradeday,trade_df[1])
	while True:
		if(tradeday not in trade_df):
			last_date=last_date-timedelta(days=1)#最近上一个交易日
			tradeday = last_date.strftime("%Y%m%d")

		else:
			lastindex= trade_df.index(tradeday)
			last_yetd_date_string=trade_df[lastindex-1]
			break

	print('复盘交易日 ： ',tradeday)#最近交易日




	笔记=复盘笔记()
	笔记.手动复盘笔记(tradeday=tradeday)
	#笔记.程序复盘笔记(tradeday=tradeday)






