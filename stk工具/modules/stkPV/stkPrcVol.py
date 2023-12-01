

import sys
import os
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
parent_dir = os.path.dirname(current_dir)
#print(parent_dir)
sys.path.append(parent_dir)



#处理html虽然python自带html库，但是似乎不好用，主流是BeautifulSoup、urllib.requests
#似乎BeautifulSoup更好用

#读取指定html
#运行各种监控代码得到结论
#在html默认位置，根据结论添加文本
#输出保存html

import string
from bs4 import BeautifulSoup
import  pathlib
import akshare as ak
import datetime
from datetime import date
from datetime import datetime

import pywencai 
from  stk工具.common import DataStruct
import pandas as pd

class 证券():
	"""docstring for ClassName"""
	def __init__(self):
		self.result=DataStruct()

		
	def 证券个股连板(self,searchtxt="2020年07月03日涨停，证券板块"):
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"证券个股连板  pywencai.get    is error ") 
			return None
		#res = pywencai.get(query="涨停，证券板块",loop=True,query_type='stock')#sort_key='所属同花顺行业'
		#print(res)
		if(res is None):
			return  None
		columns=res.columns
		#证券有个股三连板
		zt_res_col=([ i  for i in columns  if('连续涨停天数' in i)  ])#连续涨停列名字
		#print(zt_res_col)
		if(len(zt_res_col)!=1):#结果df列名字有问题
			res = pywencai.get(query="涨停，证券板块",loop=True,query_type='stock')#sort_key='所属同花顺行业'
			columns=res.columns
			zt_res_col=([ i  for i in columns  if('连续涨停天数' in i)  ])#连续涨停列名字
			if(len(zt_res_col)!=1):
				print(" 连续涨停天数 搜索结果没有这列名字")
		if(len(zt_res_col)==1):#处理完所有事项,形成”证券有个股三连板“代码功能块，代码不要写出去
			zt_res_col=zt_res_col[0]#列名字
			temp=list(res[zt_res_col])
			#print(temp)
			temp=[i for i in temp if(i >= 3 ) ]#三连板统计结果
			#print(temp)
			if(len(temp)>=1):#存在大于三连板的个股，保存信号
				#不用看是哪个股了，直接输出信号就好复盘证券所有个股和指数走势
				#输出格式是什么样子的
				#print(result.data)
				#result.append("证券个股出现三连板，指数牛市预期",keys=['stocks'])
				self.result.append(["证券个股出现三连板，牛市预期，关注此层面机会",'https://note.youdao.com/s/c8CQowSB'])#默认keys=空，表示全部添加
				#print(result.data)
			#二连板
			temp=[i for i in temp if(i >= 2 ) ]#二连板统计结果
			#print(temp)
			if(len(temp)>=1):#存在大于二连板的个股，保存信号
				#不用看是哪个股了，直接输出信号就好复盘证券所有个股和指数走势
				#输出格式是什么样子的
				#print(result.data)
				#result.append("证券个股出现三连板，指数牛市预期",keys=['stocks'])
				tip="证券个股出现二连板，证券板块机会。是否有演化三连板可能性，激活牛市预期？"
				self.result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])#默认keys=空，表示全部添加
				#print(result.data)
			#涨停板
			temp=[i for i in temp if(i >= 1) ]#
			if(len(temp)>=3):#证券板块有三个个股涨停首板 #证券当日涨停数量多，需要统计一下得到一个阈值
				tip="证券个股出现三个以上首板，证券板块机会。是否有演化二连板可能性，激活牛市预期？"
				self.result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])#默认keys=空，表示全部添加
		else:
			pass#搜索结果有问题，报错了，跳过这个检测

		return self.result
		
	def 证券个股异动(self):
		#个股信号
		#stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600030", period="daily", start_date="20231001", end_date='', adjust="qfq")
		#print(stock_zh_a_hist_df)
	 
		#中信证券3%大阳
		tempday = date.today()
		tempday = datetime.datetime.strftime(tempday,"%Y%m%d")
		stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="600030", period="daily", start_date=tempday[:4]+"0101", end_date=tempday, adjust="qfq")
		#print(stock_zh_a_hist_df)
		if(list(stock_zh_a_hist_df['涨跌幅'])[-1] > 0):
			tip="中信证券大涨，证券机会"
			self.result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])
		return self.result


		

class sktPriceVol():
	"""docstring for ClassName"""
	def __init__(self):
		self.result=DataStruct()
		self.情绪周期=[[]]

	def 连板统计(self):
		#爬取数据，每日循环，然后保存json
		#每次都直接读取后json

		#画出曲线
		#然后

	def stocks_竞价跌停(self):#竞价跌停
		pass

	def stock_天地板(self,searchtxt=""):# 这里获取涨跌停时间不同搜索语句，获得不同方式，这是一种，为了好弄天地天等
		#这里很松散的一种爬取方式，自由组合， 这里看到先天后地，先地后天，还有只要天地有就行，都选出来
		#首先都是情绪周期理论是个极致的现象，之前说过就是共识一致达成过程，是否成功看博弈结果。
		#但是有资金就是利用周期理论特殊节点，拉动极致的天地，给出重要周期信号，强行得到周期理论结论，
		#试图达成共识，成不成功另说，至少是情绪周期理论一个重要节点，大资金才会尝试去引导给情绪周期理论信号
		#试图让市场看到进而得到确定周期理论--看涨追高，但是不一定成功，看市场资金认不认可了！
		#日内一致到分歧，#出现天地板都是周期性的一般都是大行情某个调整阶段或顶部，较大分歧了，
		#搜索涨跌停时间，去掉st，这样结果是涨跌停的票，但是不一定会涨跌停，所以改变如下搜索
		#一般前面极致抱团极致妖股，才会出现这种！
		try:
			res_zt = pywencai.get(query=searchtxt + "首次涨停时间，去掉st",loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"证券个股连板  pywencai.get   is error ") 
			return None

		try:
			res_dt = pywencai.get(query=searchtxt + "首次跌停时间，去掉st",loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"证券个股连板  pywencai.get   is error ") 
			return None

		#合并下，有涨跌停时间的
		codes = set(list(res_zt["股票代码"])) & set(list(res_dt["股票代码"]))
		codes = list(codes)
		if(len(codes)==0):
			return None
		#print(codes)
		res_zt=res_zt[res_zt['股票代码'].isin(codes)]
		res_dt=res_dt[res_dt['股票代码'].isin(codes)]
		#print(res_zt)
		#print(res_dt)
		# print(res_zt.columns)
		# print(res_dt.columns)
		sc_zt_col=[col   for  col in res_zt.columns if("首次涨停时间" in col)]
		if(len(sc_zt_col)!=1):
			print(" 涨跌停时间 搜索结果没有这列名字",sc_zt_col)
			return None
		sc_zt_col=sc_zt_col[0]

		sc_dt_col=[col   for  col in res_dt.columns if("首次跌停时间" in col)]
		if(len(sc_dt_col)!=1):
			print(" 涨跌停时间 搜索结果没有这列名字",sc_dt_col)
			return None
		sc_dt_col=sc_dt_col[0]
		#print(sc_zt_col,sc_dt_col)
		#print(list(res_zt[sc_zt_col]),list(res_dt[sc_dt_col]))
		#print(res_zt ,res_dt )
		#return 
		#合并dataframe
		jj_col=list(set(res_zt.columns) &  set(res_dt.columns))
		#print(jj_col)
		
		merged_df = pd.merge(res_zt, res_dt, on=jj_col)
		#print(merged_df[sc_zt_col][0],merged_df[sc_dt_col][0])
		

		#print(sc_dt_col,sc_zt_col)
		# #时间字符串前后空格，去掉
		merged_df[sc_zt_col]= merged_df[sc_zt_col].apply(lambda x: x.strip())
		merged_df[sc_dt_col]= merged_df[sc_dt_col].apply(lambda x: x.strip())
		#print(merged_df[sc_dt_col][0])
		#print(merged_df[sc_zt_col][0],merged_df[sc_dt_col][0])
		#return
		merged_df[sc_zt_col] = pd.to_datetime(merged_df[sc_zt_col],format='%H:%M:%S')
		merged_df[sc_dt_col] = pd.to_datetime(merged_df[sc_dt_col],format='%H:%M:%S')
		#print(merged_df)
		#print(merged_df[sc_zt_col][0],merged_df[sc_dt_col][0])

		df_天地=merged_df[merged_df[sc_zt_col] < merged_df[sc_dt_col] ]#先涨停，后跌停，天地（地天地不算）
		# print(df_天地.columns)
		# #
		# zt_state=[col   for  col in df_天地.columns if("涨停[20" in col)]
		# zt_state=zt_state[0]
		# dt_state=[col   for  col in df_天地.columns if("涨停状态[20" in col)]
		# dt_state=dt_state[0]
		# print(  zt_state  ,    dt_state)
		# if(zt_state=="涨停"):#可能又空格需要处理，   就是说判断   天地地，还是天地天
		# 	pass
		# elif(dt_state="跌停"):

		#df_地天=merged_df[merged_df[sc_zt_col] > merged_df[sc_dt_col] ]#地天

		#print(df_地天)

		
		if(len(df_天地)>0):#有天地就是分歧，就是高点，极限恐慌
			self.result.append(["天地板，情绪周期重要节点，做多情绪松动点，突然冷水，疯狂贪婪清醒，做多热情不一定马上熄灭，但是开始惊弓之鸟，\
				此后高位票开始剧烈震旦，随时核按钮，抢跑，随时暴跌砸盘，风险情绪一点点扩散，其中可能又波折，但是出现这个天地，\
				做多周期进入下一个杯弓蛇影做空情绪蔓延阶段。蔓延速度不好说。情绪周期界定点",
				"https://note.youdao.com/s/c8CQowSB"],keys=['index'])
		# if(len(df_地天)):#有地天就是一致，有底部，有反核，不一定是底部，只能说可能是个转折点短线，
		# 	self.result.append(["地天板，情绪周期重要节点，能激活多少做多情绪不好说，但是有资金想开始一个新周期，是否成功不好说，\
		# 		算是一个情绪周期界定点，之后走势很复杂不好说",
		# 		"https://note.youdao.com/s/c8CQowSB"],keys=['index'])
			return True
		else :
			return False

	def stock_地天板(self,searchtxt=""):# 这里获取涨跌停时间不同搜索语句，获得不同方式，这是一种，为了好弄天地天等
		#这里很松散的一种爬取方式，自由组合， 这里看到先天后地，先地后天，还有只要天地有就行，都选出来
		#首先都是情绪周期理论是个极致的现象，之前说过就是共识一致达成过程，是否成功看博弈结果。
		#但是有资金就是利用周期理论特殊节点，拉动极致的天地，给出重要周期信号，强行得到周期理论结论，
		#试图达成共识，成不成功另说，至少是情绪周期理论一个重要节点，大资金才会尝试去引导给情绪周期理论信号
		#试图让市场看到进而得到确定周期理论--看涨追高，但是不一定成功，看市场资金认不认可了！
		#日内一致到分歧，#出现天地板都是周期性的一般都是大行情某个调整阶段或顶部，较大分歧了，
		#搜索涨跌停时间，去掉st，这样结果是涨跌停的票，但是不一定会涨跌停，所以改变如下搜索
		#一般前面极致抱团极致妖股，才会出现这种！
		try:
			res_zt = pywencai.get(query=searchtxt + "首次涨停时间，去掉st",loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"证券个股连板  pywencai.get   is error ") 
			return None

		try:
			res_dt = pywencai.get(query=searchtxt + "首次跌停时间，去掉st",loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"证券个股连板  pywencai.get   is error ") 
			return None

		#合并下，有涨跌停时间的
		codes = set(list(res_zt["股票代码"])) & set(list(res_dt["股票代码"]))
		codes = list(codes)
		if(len(codes)==0):
			return None
		#print(codes)
		res_zt=res_zt[res_zt['股票代码'].isin(codes)]
		res_dt=res_dt[res_dt['股票代码'].isin(codes)]
		#print(res_zt)
		#print(res_dt)
		# print(res_zt.columns)
		# print(res_dt.columns)
		sc_zt_col=[col   for  col in res_zt.columns if("首次涨停时间" in col)]
		if(len(sc_zt_col)!=1):
			print(" 涨跌停时间 搜索结果没有这列名字",sc_zt_col)
			return None
		sc_zt_col=sc_zt_col[0]

		sc_dt_col=[col   for  col in res_dt.columns if("首次跌停时间" in col)]
		if(len(sc_dt_col)!=1):
			print(" 涨跌停时间 搜索结果没有这列名字",sc_dt_col)
			return None
		sc_dt_col=sc_dt_col[0]
		#print(sc_zt_col,sc_dt_col)
		#print(list(res_zt[sc_zt_col]),list(res_dt[sc_dt_col]))
		#print(res_zt ,res_dt )
		#return 
		#合并dataframe
		jj_col=list(set(res_zt.columns) &  set(res_dt.columns))
		#print(jj_col)
		
		merged_df = pd.merge(res_zt, res_dt, on=jj_col)
		#print(merged_df[sc_zt_col][0],merged_df[sc_dt_col][0])
		

		#print(sc_dt_col,sc_zt_col)
		# #时间字符串前后空格，去掉
		merged_df[sc_zt_col]= merged_df[sc_zt_col].apply(lambda x: x.strip())
		merged_df[sc_dt_col]= merged_df[sc_dt_col].apply(lambda x: x.strip())
		#print(merged_df[sc_dt_col][0])
		#print(merged_df[sc_zt_col][0],merged_df[sc_dt_col][0])
		#return
		merged_df[sc_zt_col] = pd.to_datetime(merged_df[sc_zt_col],format='%H:%M:%S')
		merged_df[sc_dt_col] = pd.to_datetime(merged_df[sc_dt_col],format='%H:%M:%S')
		#print(merged_df)
		#print(merged_df[sc_zt_col][0],merged_df[sc_dt_col][0])

		#df_天地=merged_df[merged_df[sc_zt_col] < merged_df[sc_dt_col] ]#先涨停，后跌停，天地
		# print(df_天地.columns)
		# #
		# zt_state=[col   for  col in df_天地.columns if("涨停[20" in col)]
		# zt_state=zt_state[0]
		# dt_state=[col   for  col in df_天地.columns if("涨停状态[20" in col)]
		# dt_state=dt_state[0]
		# print(  zt_state  ,    dt_state)
		# if(zt_state=="涨停"):#可能又空格需要处理，   就是说判断   天地地，还是天地天
		# 	pass
		# elif(dt_state="跌停"):

		df_地天=merged_df[merged_df[sc_zt_col] > merged_df[sc_dt_col] ]#有地天，且是先地后天(“天地天”的不算)

		#print(df_地天)

		
		# if(len(df_天地)>0):#有天地就是分歧，就是高点，极限恐慌
		# 	pass
		# 	self.result.append(["天地板，情绪周期重要节点，做多情绪松动点，突然冷水，疯狂贪婪清醒，做多热情不一定马上熄灭，但是开始惊弓之鸟，\
		# 		此后高位票开始剧烈震旦，随时核按钮，抢跑，随时暴跌砸盘，风险情绪一点点扩散，其中可能又波折，但是出现这个天地，\
		# 		做多周期进入下一个杯弓蛇影做空情绪蔓延阶段。蔓延速度不好说。情绪周期界定点",
		# 		"https://note.youdao.com/s/c8CQowSB"],keys=['index'])
		if(len(df_地天)>0):#有地天就是一致，有底部，有反核，不一定是底部，只能说可能是个转折点短线，
			self.result.append(["地天板，情绪周期重要节点，能激活多少做多情绪不好说，但是有资金想开始一个新周期，是否成功不好说，\
				算是一个情绪周期界定点，之后走势很复杂不好说",
				"https://note.youdao.com/s/c8CQowSB"],keys=['index'])
			return True
		else :
			return False



	def stk_stocks_pv_monitor(self):#个股价量关系指标监控
		
		#不同股票池意义不同，就是所有个股统计，和人气股票池统计，得到核按钮结论不同
		#所有个股统计，个股网站人气股统计，自己选择的龙头妖股等，不同地位得到不一样结论，
		#所以这里方式，是股票池+函数，函数里不出现代码相关东西
		#
		#


		return self.result

	def stk_blocks_pv_monitor(self):#个股价量关系指标监控
 
		return self.result
	 

	def stk_indexs_pv_monitor(self):
		
		#大盘成交量能决定行情级别，所以决定自己参与总体现金仓位占比。控制整体风险最重要一道保险。
		df1 = ak.stock_zh_index_daily_em(symbol="sh000001")
		df2 = ak.stock_zh_index_daily_em(symbol="sz399001")
		#print(df1,df2)
		#print(list(df1['amount'])[-1]+list(df2['amount'])[-1])
		亿=100000000
		if(list(df1['amount'])[-1]+list(df2['amount'])[-1] < 10000*亿):#
			self.result.append(["小于万亿市场，仓位控制在50%下","https://www.baidu.com/"],keys=['index'])
		if(list(df1['amount'])[-1]+list(df2['amount'])[-1] < 15000*亿 and list(df1['amount'])[-1]+list(df2['amount'])[-1] > 10000*亿 ):
			self.result.append(["大于1万亿市场，仓位70%，活跃市场","https://www.baidu.com/"],keys=['index'])
		if(list(df1['amount'])[-1]+list(df2['amount'])[-1] > 15000*亿):
			self.result.append(["大于1.5万亿市场，仓位100%，牛市","https://www.baidu.com/"],keys=['index'])

		
		return self.result

	def stk_special_xx_monitor(self):#特殊的，没有必要分开的，集合在一起比较好管理额特殊类，单独写就行不用放在这里
 
		return self.result

	def stk_special_证券_monitor(self):#特殊的，没有必要分开的，集合在一起比较好管理额特殊类
 
		#搜索内容：2023年11月06日涨停，证券板块，阶段涨停
		#搜索内容：涨停，证券板块，阶段涨停
		inst证券=证券()
		inst证券.证券个股连板(searchtxt="涨停，证券板块")
		inst证券.证券个股异动()
		inst证券.result.data
		#print(inst证券.data)
		self.result.update(inst证券.result)#合并DataStruct的数据 
		return self.result

	def stk_special_情绪周期_monitor(self):
		#x轴是时间，Y轴是最高连板（这里手动给个文档就是删除个股和时间段的统计不作为最好连板，
		#类似利好停盘不断涨停这种连板意义不大，所以复盘历史时候通过增加辅助文件个股和时间区间，去掉就是）
		#实时的也可以利用这个给个期限就是
		#不用太纠结卡位接力这种，至少说明一个重要转折点来了，至于新周期也好啥周期也好谨慎一点，不用那么较真
		#慢慢再细化，太机械，太情绪周期理论了，感觉容易被收割！
		notes=""#保存情绪周期的提示
		status=self.stock_天地板()
		if(status):
			notes=notes+"天地板 "

		status=self.stock_地天板()
		if(status):
			notes=notes+"地天板 "




	#测试代码，其他函数没有输出，这里作为测试使用
	def test_txt(self):
 
		self.result.append(["测试代码codes","https://note.youdao.com/s/c8CQowSB"],keys=['blocks'])
		return self.result




	def stk_pv_monitor(self):#股票的价格量能及其演化出的各种价量关系技术指标，做监控

	#使用的是common.DataStruct()数据结果，在common.DataStruct().data中字典，三个级别的信号，意思是里面产生了三个级别信号，
	#然后返回之后，要分类之后，分别显示在不同级别文件中！

		#个股信号，能产生各个级别的异动信息
		self.stk_stocks_pv_monitor()

		#板块信号，能产生各个级别的异动信息
		self.stk_blocks_pv_monitor()
		#指数
		self.stk_indexs_pv_monitor()
		#特殊个股板块，单独拿出来，
		#证券个股和板块 信号，能产生各个级别的异动信息
		self.stk_special_证券_monitor()
		#写入


		self.stk_情绪周期()


		return self.result



if __name__ == '__main__':
	pass
 
	#DataStruct，在stktool中被import，所以如果执行stktool，这里不引用代码也是对
	#但是单独执行这里代码，没法目前目录结构没法直接引用，
	#
	##要像被其他代码调用，一种是，目录管理，被上层的代码调用，
	#或者放在将模块放在与你的项目代码相同的目录中。
	#将模块放在 Python 的标准库路径中。#
	#将模块所在的目录添加到 sys.path 中。
	#做成共享模块：
	#比较方便时sys和在最上层调用调试
	#这里用sys.path 调试临时用！最后的代码可以没有这个

	#out=sktPriceVol().stk_pv_monitor()
	#print(out.data)
	# a=sktPriceVol().stock_天地板(searchtxt="2023年11月29日")
	# print(a.data)



 