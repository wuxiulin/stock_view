#右侧指数
#左侧是统计数据，问财爬取？

import pywencai
import akshare as ak
import datetime
from datetime import date
import json
import os
import time
def get_days_wencai(start="",end="",txt="涨停,证券板块"):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	print(current_dir)
	#爬取多日
	##处理时间
	trade_date_df = ak.tool_trade_date_hist_sina()#获取交易日
	trade_date_list = trade_date_df["trade_date"].astype(str).tolist()
	#print(trade_date_list)#时间带 -
	if(start==''):#返回，为了更好兼容这个代码，上层处理更多情况，这里不处理，必须输入start
		# start=date.today()-datetime.timedelta(days=15)#这借口太长时间没有数据报错
		# start=datetime.datetime.strftime(start,"%Y-%m-%d")
		#print(start)
		print("start is null,input start time!")
		return
	if('-' not in start):#获取交易日的接口格式是"2023-11-01"，所以做处理
		start=start[:4]+'-'+start[4:6]+'-'+start[6:8]

	tempday=datetime.datetime.strptime(start,"%Y-%m-%d") 
	while datetime.datetime.strftime(tempday,"%Y-%m-%d")  not in trade_date_list:  # 如果当前日期不在交易日期列表内，则当前日期天数减一
		tempday =  tempday + datetime.timedelta(days=1)
	start=datetime.datetime.strftime(tempday,"%Y-%m-%d")#


	if(end==''):
		tempday = date.today()
		tempday = datetime.datetime.strftime(tempday,"%Y-%m-%d")
		while(tempday not in  trade_date_list):#今天是周末或假期
			tempday=datetime.datetime.strptime(tempday,"%Y-%m-%d")-datetime.timedelta(days=1)
			tempday=datetime.datetime.strftime(tempday,"%Y-%m-%d")
		end=tempday
	else:
		if('-' not in end):#获取交易日的接口格式是"2023-11-01"，所以做处理
			tempday=end[:4]+'-'+end[4:6]+'-'+end[6:8]
		#print(tempday)
		tempday=datetime.datetime.strptime(tempday,"%Y-%m-%d")
		while datetime.datetime.strftime(tempday,"%Y-%m-%d")  not in trade_date_list:  # 如果当前日期不在交易日期列表内，则当前日期天数减一
			tempday =  tempday - datetime.timedelta(days=1)
		
		end=datetime.datetime.strftime(tempday,"%Y-%m-%d")

	#print("set:",start,end)
	tradedays=trade_date_list[trade_date_list.index(start):trade_date_list.index(end)+1]#g根据输入获得tradedays
	#print(tradedays)
	#结果队列

	#为了保持交易日的list的顺序，这里处理一下防止中间有些日子没有爬取数据，
	file_path = txt+".json"
	# 检查文件是否存在
	if os.path.exists(file_path):
	    # 文件存在，读取内容
		with open(file_path, 'r') as json_file:
			pre_data = json.load(json_file)
			#print(pre_data)
			#print(type(pre_data))
			#pre_data=eval(pre_data)
			pre_tradedays=pre_data['date']
			#print("上一次",pre_tradedays)
			#在tradedays  和tradedays都是有序的数列，比较看真正的扩大版额，不要取交集了，都爬取了
			# print((datetime.datetime.strptime(pre_tradedays[0],"%Y-%m-%d")- datetime.datetime.strptime(tradedays[0],"%Y-%m-%d")).days)
			# print(pre_tradedays[0],tradedays[0])
			if((datetime.datetime.strptime(pre_tradedays[0],"%Y-%m-%d")- datetime.datetime.strptime(tradedays[0],"%Y-%m-%d")).days>0):
				deal_day_start=tradedays[0] #选择时间更早一点的
			else:
				deal_day_start=pre_tradedays[0]

			if((datetime.datetime.strptime(pre_tradedays[-1],"%Y-%m-%d")- datetime.datetime.strptime(tradedays[-1],"%Y-%m-%d")).days>0):
				deal_day_end=pre_tradedays[-1]#选择时间更晚一点的！
			else:
				deal_day_end=tradedays[-1]
			# print(deal_day_start,deal_day_end)
			#扩大版的爬取是日期方便简单处理一些
			all_deal_tradedays = trade_date_list[trade_date_list.index(deal_day_start):trade_date_list.index(deal_day_end)+1]#g根据输入获得tradedays
 		    
			#print("kuoda:",all_deal_tradedays)
 		    #差集，要新增爬取的days，扩大版本的，尽可能补齐数据
			temp_tradedays = [element for element in all_deal_tradedays if (element not in pre_tradedays)]

		#print("paqu",temp_tradedays)
		print(f' Data loaded from {file_path}')
		if(len(temp_tradedays)==0):
			print(f'all days is ok return...')
			return pre_data####要不要根据start，end截取，后面再瘦！
	else:
	    # 文件不存在，跳过 
		temp_tradedays=tradedays #上面是差集，这里也是差集，为0而已，扩大版的所有需要处理的天数
		all_deal_tradedays=tradedays
		print(f'{file_path} does not exist. Skipping...')
		if(len(temp_tradedays)==0):
			print(f'no days is ok return...')
			return 


	result=	 {key: value for key, value in zip(tradedays,[{}]*len(tradedays)) }#新增的统计结果，后面会合并，保存对应日期day和结果

	#print(temp_tradedays)
	sx=0
	ex=9#连板数最大统计到哪里
	#0代表今日满足条件个数，
	for day in temp_tradedays:#去掉已经爬取的后的日子
		print(day)
		#本想吧day_result放在外面，没必要每次都创建，但是发现有问题，就是赋值时候跟想的不一样，
		#不做处理直接赋值，每次迭代对象都是同一个，有问题用copy赋值对象也不行有问题，
		day_result= {str(key): value for key, value in zip(range(sx,ex),[0]*len(range(sx,ex)) ) }
		#print(day_result)
		#爬取单日
		res = pywencai.get(query=day + txt,loop=True,query_type='stock')#测试'
		if(res is None):
			result[day]=day_result#初始化0，day_result循环创建，所以没有迭代历史数据
			continue
		columns=res.columns#列名字不同每天
		zt_res_col=([ i  for i in columns  if('连续涨停天数' in i)  ])[0]#连续涨停列名字
		#print(zt_res_col)
		lxztts=list(res[zt_res_col])
		if(len(lxztts)==0):
			#day_result 初始化为0
			result[day]=day_result#初始化0
			continue
		for i in lxztts:
			#print(i,day_result[i])
			try:
				day_result[str(i)]=day_result[str(i)]+1
			except Exception as e:#更多连板的，没有建立字典，以后再说，这里可以添加字典，但是出去之后要处理缺失的days
				print("没有建立足够多的key保存这么多数据选项，调节ex值",lxztts)
				print(e)
			#print(i,day_result[i])
		day_result[str(0)]=len(res.index)
		#print(day_result)
		
		result[day]=day_result#不能直接赋值，而是每次循环重新创建，

	#print(result)

	line_result= {str(key): value for key, value in zip(range(sx,ex),[[]]*len(range(sx,ex))) }
	#print(line_result)
	keys=result[temp_tradedays[0]].keys()
	for key in keys:
		templine=[]#必须建立临时变量负责迭代有问题
		for day in temp_tradedays:
			temp=result[day][str(key)]
			templine.append(temp)
		#print(templine)
		line_result[str(key)]=templine
	#print(line_result)	
	

	#画图
	
	#结果保存，频繁更新但是大量计算的可以保存结果，方便后面使用更加快捷
	#但是不经常使用的无所谓，但是大量计算的考虑
	

	#处理合并#


	if os.path.exists(file_path):
		#print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
		#print(pre_data)
		##print({"date":temp_tradedays,"line":line_result,"result":result} )
		#print('################################')
		#print(result)
		#print(pre_data['result'])
		result.update(pre_data['result'])#合并
		#print(result)
		#print('################################')

		temp_line_result= {str(key): value for key, value in zip(range(sx,ex),[[]]*len(range(sx,ex))) }
		#print(temp_line_result)
		keys=result[temp_tradedays[0]].keys()
		for key in keys:
			templine=[]#必须建立临时变量负责迭代有问题
			for day in all_deal_tradedays: #重新赋值一遍，这样list的顺序就是对的
				#print(day,type(day))
				#print(temp_tradedays)
				#print(pre_data['date'])
				#print(pre_data['date'][0],type(pre_data['date'][0]))

				# if(day not in temp_tradedays):   
				# 	#print(")))))")
				# 	#print(type(pre_data['result'][day]))
				# 	#print(")))))")
				# 	#print(key,type(key))
				# 	temp=pre_data['result'][day][str(key)]
				# 	templine.append(temp)
				# else:
				# 	temp=result[day][key]
				# 	templine.append(temp)
				#不是合并了了么？
				templine.append(result[day][str(key)])

			#print(templine)
			temp_line_result[str(key)]=templine

		out={"date":all_deal_tradedays,"line":temp_line_result,"result":result} 
	else:
		out={"date":all_deal_tradedays,"line":line_result,"result":result} 

	#print("**********************************")
	#print(out)
	#print("**********************************")
	# 指定保存的文件路径
	file_path = txt+".json"
	if os.path.exists(file_path):
		if os.path.exists('old_'+file_path):
			os.remove('old_'+file_path)
			os.rename(file_path, 'old_'+file_path)#备份
		else:
			os.rename(file_path, 'old_'+file_path)#备份

	# 使用 json.dump 将字典保存为 JSON 文件
	with open(file_path, 'w') as json_file:
		json.dump(out, json_file)

	print(f'Data has been saved to {file_path}')

	return out


if __name__ == '__main__':
	tt=[
			['20230101','20230201'],
			['20230201','20230301'],
			['20230301','20230401'],
			['20230401','20230501'],
			['20230501','20230601'],
			['20230601','20230701'],
			['20230701','20230801'],
			['20230801','20230901'],
			['20230901','20231001'],
			['20231001','20231101'],
			['20231101','20231125'],

	]
	for i in tt:
		print(i)
		try:
			get_days_wencai(start=i[0],end=i[1],txt="涨停,证券板块")
		except Exception as e:
			time.sleep(60)
			print(e)
	
 
	#get_days_wencai(start='20231110',end='20231123')
