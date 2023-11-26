
#处理html虽然python自带html库，但是似乎不好用，主流是BeautifulSoup、urllib.requests
#似乎BeautifulSoup更好用

#读取指定html
#运行各种监控代码得到结论
#在html默认位置，根据结论添加文本
#输出保存html
import string
from bs4 import BeautifulSoup
import  pathlib
import pywencai



def stk_stocks_pv_monitor():#个股价量关系指标监控
	
	#
	pass

def stk_blocks_pv_monitor():#个股价量关系指标监控
	pass

def stk_special_xx_monitor():#特殊的，没有必要分开的，集合在一起比较好管理额特殊类，单独写就行不用放在这里
	pass

def stk_special_证券_monitor():#特殊的，没有必要分开的，集合在一起比较好管理额特殊类
	result=common.DataStruct()
	#搜索内容：2023年11月06日涨停，证券板块，阶段涨停
	#搜索内容：涨停，证券板块，阶段涨停
	

	res = pywencai.get(query="2020年07月03日涨停，证券板块",loop=True,query_type='stock')#测试'
	#res = pywencai.get(query="涨停，证券板块",loop=True,query_type='stock')#sort_key='所属同花顺行业'
	columns=res.columns


	#证券有个股三连板
	zt_res_col=([ i  for i in columns  if('连续涨停天数' in i)  ])#连续涨停列名字
	print(zt_res_col)
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
		print(temp)
		if(len(temp)>=1):#存在大于三连板的个股，保存信号
			#不用看是哪个股了，直接输出信号就好复盘证券所有个股和指数走势
			#输出格式是什么样子的
			#print(result.data)
			#result.append("证券个股出现三连板，指数牛市预期",keys=['stocks'])
			result.append(["证券个股出现三连板，牛市预期，关注此层面机会",'https://note.youdao.com/s/c8CQowSB'])#默认keys=空，表示全部添加
			#print(result.data)
		#二连板
		temp=[i for i in temp if(i >= 2 ) ]#二连板统计结果
		print(temp)
		if(len(temp)>=1):#存在大于二连板的个股，保存信号
			#不用看是哪个股了，直接输出信号就好复盘证券所有个股和指数走势
			#输出格式是什么样子的
			#print(result.data)
			#result.append("证券个股出现三连板，指数牛市预期",keys=['stocks'])
			tip="证券个股出现二连板，证券板块机会。是否有演化三连板可能性，激活牛市预期？"
			result.append([tip,'https://note.youdao.com/s/c8CQowSB'],keys=['blocks'])#默认keys=空，表示全部添加
			#print(result.data)
		#首版



	else:
		pass#搜索结果有问题，报错了，跳过这个检测

	#证券当日涨停数量多，需要统计一下得到一个阈值
	#上证指数，+证券个股涨停数异动
	#

	
	#中信证券3%大阳




def stk_pv_monitor():#股票的价格量能及其演化出的各种价量关系技术指标，做监控
	#个股信号
	#证券-个股---三连板
	stk_stocks_pv_monitor()

	#板块信号
	stk_blocks_pv_monitor()

	#特殊个股板块，单独拿出来，
	#证券个股和板块 信号
	stk_special_证券_monitor()


	pass


if __name__ == '__main__':
 
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
	import sys
	import os
	current_dir = os.path.dirname(os.path.abspath(__file__))
	parent_dir = os.path.dirname(current_dir)
	sys.path.append(parent_dir)
	import common

	stk_pv_monitor()
 