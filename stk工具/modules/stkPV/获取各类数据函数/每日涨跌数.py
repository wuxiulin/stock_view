import   pywencai
import akshare as ak
import os,sys 
import json
import pandas as pd
from datetime import datetime
	# '20231218上涨家数'  这个字符串，我在问财自己搜索无法得到"20231218上涨"等类似表达的结果，而是
	# 一堆指数，然后包含上涨家数。但是我用pywencai，搜索'20231218上涨家数' 能得到"20231218上涨"这种表达
	# 所以，问财接口的问题，所以要是用"20231218上涨"获得上涨股票然后再求上涨家，用get_day_每日上涨跌数_wencai_1
	# 如果'20231218上涨家数' 这种表述是用方法二，更容易在浏览器问财复现
	#其次结果方法一是同花顺全A（沪深京）所有上涨
	#方法二是同花顺全A (沪深)，当然也有同花顺全A（沪深京）等很多丰富结果，都是一次能获取，
	#所以更新历史数据，提倡方法二，依次获取，处理后一次保存更新文件
	#单纯获取一天的无所谓
class 每日上涨数类():
	def __init__(self):
		pass

	def update_day_(self,day):#某天数据有误，应该是爬取保存文件有问题，就是重新爬取更新文件
		pass
	def __get_day_每日上涨数_wencai_1(self,day):  

		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt=day+'上涨,去掉北交所'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日上涨跌数_wencai   is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"get_day_每日上涨跌数_wencai   is  none ") 
			return  None
	 
		return len(res)

	def __get_day_每日上涨数_wencai_2(self,day): #
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt=day+'上涨家数'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='zhishu')#测试'
		except Exception as e:
			print(e,"get_day_每日上涨跌数_wencai   is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"get_day_每日上涨跌数_wencai   is  none ") 
			return  None
		#print(res)	
		columns=res.columns
		col=	[ item for item in columns if "上涨家数" in item]
		if(len(col)>1 or len(col)<=0):
			print('搜索标题内容有误，核对')
		else:
			col=col[0]

		value = res.loc[res['code'] == '883421', col]
		#value = res.loc[df['指数简称'] == '同花顺全A (沪深)', col]
		value=int(list(value)[0])
		return value

	def get_day_每日上涨数_wencai(self,tradeday):  
		#查询文件
		#爬取
		#保存
		#返回值
		#不用检查日期，差不不到返回none

		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日上涨数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日上涨数_有序.json')
		#print(data_file_path)

		#获取文件中交易日期
		if os.path.exists(data_file_path):
	    # 文件存在，读取内容
			if os.path.getsize(data_file_path) > 0:
				with open(data_file_path, 'r',encoding='utf-8') as json_file:
					file_content = json.load(json_file)
			else:#文件存在但是没哟内容这里open会报错，所以处理
				file_content={}
		else:#创建文件
			with open(data_file_path, 'w',encoding='utf-8') as json_file:
				pass#为空
			file_content={}
		pre_days=file_content.keys()#已经爬取的日子

		if(tradeday in pre_days):
			return file_content[tradeday]
		else:
			#这里不通过判断，简化代码，直接爬取就是了
			temp=self.__get_day_每日上涨数_wencai_1(day=tradeday)
			#print(temp)
			if(temp is not None):

				#先保存后
				file_content[tradeday]=temp
				#无序保存
				with open(data_file_path, 'w',encoding='utf-8') as json_file:
					json.dump(file_content, json_file)
				#有序保存
				all_days=list(file_content.keys()) 
				# 将时间字符串转换为 datetime 对象
				datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
				sorted_datetime_objects = sorted(datetime_objects)
				有序alldays=[item.strftime('%Y%m%d') for item in sorted_datetime_objects]
				#print(有序alldays[-1])
				#有序读取
				result=[  (day,file_content[day])     for day in 有序alldays]
				with open(data_file_path_有序, 'w',encoding='utf-8') as json_file:
					json.dump(result, json_file)

				#后返回
				return  temp
			else:#获取不到最新交易日数据，文件中没有匹配日又没有，所以返回为空
				return None




	def get_days_每日上涨数_wencai(self,start,end):
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日上涨数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日上涨数_有序.json')
		#print(data_file_path)

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		if start in trade_df:
			sindex = trade_df.index(start)
		else:
			print(start ,"  start 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
			return

		if end in trade_df:
			eindex = trade_df.index(end)
		else:
			print(end ,"  end 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
			return

		sedays=trade_df[sindex:eindex+1]
		#print(sedays)	


		#获取文件中交易日期
		#
		if os.path.exists(data_file_path):
	    # 文件存在，读取内容
			if os.path.getsize(data_file_path) > 0:
				with open(data_file_path, 'r',encoding='utf-8') as json_file:
					file_content = json.load(json_file)
			else:#文件存在但是没哟内容这里open会报错，所以处理
				file_content={}
		else:#创建文件
			with open(data_file_path, 'w',encoding='utf-8') as json_file:
				pass#为空
			file_content={}
		pre_days=file_content.keys()#已经爬取的日子
		
		crawl_days=set(sedays)-set(pre_days)
		#做差集，爬取，保存
		for day in crawl_days:
			print(day)
			temp=self.__get_day_每日上涨数_wencai_1(day)
			file_content[day]=temp

		#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(file_content, json_file)
		
		# #选出设定日期，返回无序
		# result_dict = {key: file_content[key] for key in sedays}
		# return result_dict 
		

		#大多数需要有序，所以这里重新排序。这里代码不做修改了，就是说两种格式代码都有，
		#且以字典无序来处理为主，有序没有读取只是保存
		 	# if os.path.exists(data_file_path):
	 	# 	if os.path.getsize(data_file_path) > 0:
		#  		with open(data_file_path_有序, 'r',encoding='utf-8') as json_file:
		# 			json.dump(有序_file_content, json_file)
		# 		pre_start=有序_file_content[0][0]
		# 		pre_end=有序_file_content[-1][0]	
		# 	else:
		# 		有序_file_content=[]
		# 		pre_start=''
		# 		pre_end=''
		# else:
		# 	有序_file_content=[]
		# 	pre_start=''
		# 	pre_end=''
		# if(len(有序_file_content)==0):
		
		#修改前起始
		#all_days=set(sedays) | set(pre_days) #并集
		# 将时间字符串转换为 datetime 对象
		#datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
		# # 找到最早时间和最晚时间
		# earliest_time = min(datetime_objects)
		# latest_time = max(datetime_objects)
		# # 将结果输出为字符串格式
		# earliest_time_str = earliest_time.strftime('%Y%m%d')
		# latest_time_str = latest_time.strftime('%Y%m%d')
		# earliestindex = trade_df.index(earliest_time_str)
		# latestindex = trade_df.index(latest_time_str)

		# 有序alldays=trade_df[earliestindex:latestindex+1]#有序,d但是可能时间有的没有爬取，太宽泛
		# #这里可以对datetime_objects排序然后转为字符串，代替有序alldays，算了不改了
		# #print(有序alldays)
		# #有序读取
		# result=[]
		# for day in 有序alldays:
		# 	if(day in all_days):#有序alldays太广了，
		# 		result.append( (day,file_content[day]) )
		#修改前结束

		#修改后起始
		all_days=list(file_content.keys()) 
		# 将时间字符串转换为 datetime 对象
		datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
		sorted_datetime_objects = sorted(datetime_objects)
		有序alldays=[item.strftime('%Y%m%d') for item in sorted_datetime_objects]
		#print(有序alldays[-1])
		#有序读取
		result=[  (day,file_content[day])     for day in 有序alldays]
		#修改后结束


		with open(data_file_path_有序, 'w',encoding='utf-8') as json_file:
			json.dump(result, json_file)
	 	
	 	#选出设定日期，返回有序
		start_index = 有序alldays.index(start)
		end_index = 有序alldays.index(end)
		return result[start_index:end_index+1]
	
	def update_days_wencai(self,start='20180104',end='20231220'):
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		if start in trade_df:
			sindex = trade_df.index(start)
		else:
			print(start ,"  start 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
			return

		if end in trade_df:
			eindex = trade_df.index(end)
		else:
			print(end ,"  end 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
			return

		sedays=trade_df[sindex:eindex+1]
		dys=[(sedays[i],sedays[min(i+ 20,len(sedays)-1)]) for i in range(0, len(sedays), 20)]
		for item in dys:
			print(item)
			data=s.get_days_每日上涨数_wencai(item[0],item[1])
 


	def __group_by_week(self,data):#对时间处理，就是同一周放在一起，注意data格式微调代码
		#chatgtp给了几个方法都有问题这里自己写
		grouped_data = []
		current_week = []

		for item in data:
			date_str, value = item
			date_obj = datetime.strptime(date_str, "%Y%m%d")

			if not current_week:#每周的首个交易日
				current_week.append(item)
				# 获取星期几，其中0表示星期一，1表示星期二，以此类推
				day_of_week = date_obj.weekday()
				#本周和这个这周起始交易日的最大差是4-day_of_week
				cha_week=4-day_of_week

			else:
		        # Check if the current date is in the same week as the previous date
				if (date_obj - datetime.strptime(current_week[0][0], "%Y%m%d")).days <= cha_week:
					current_week.append(item)
				else:
					grouped_data.append(current_week)
					current_week = [item]
					date_str, value = item
					date_obj = datetime.strptime(date_str, "%Y%m%d")
					day_of_week = date_obj.weekday()
					cha_week=4-day_of_week

		if current_week:
		    grouped_data.append(tuple(current_week))

		return grouped_data
 


 
	def __group_by_month(self,data):
		# Convert data to DataFrame
		df = pd.DataFrame(data, columns=['Date', 'Value'])
		# Convert string dates to datetime objects
		df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

		# Group by month considering the entire period
		grouped_data = [ [ (timestamp.strftime('%Y%m%d'), value) for timestamp, value in group.values]
		for name, group in df.groupby(df['Date'].dt.to_period('M'))]

		return grouped_data

	def statistics_and_analysis(self):
		#爬取的数据自身的一下属性来统计研究，周期性概率性是个重要目标，--波段之门的启发
		##统计大于3000上涨，每周，每月，每年次数
		##大概用同花顺看了一下，
		data=self.get_days_每日上涨数_wencai('20220104','20231220')
		#print(data)
		data=[ item for item in data if item[1] >= 4000]#
		print([ item[0] for item in data ])

		# data_week=self.__group_by_week(data)
		
		# print(data_week)
		
		# i_num_week=[len(item) for item in data_week]#每周含有元组数，就是没有符合条件个数
		# print(i_num_week)
		# i4_num_week=[ item[0] for item in data_week if len(item)==3]
		
		# print(i4_num_week)


class 每日下跌数类():
	def __init__(self):
		pass


	def __get_day_每日下跌数_wencai_1(self,day):  

		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt=day+'下跌,去掉北交所'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"__get_day_每日下跌数_wencai_1   is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"__get_day_每日下跌数_wencai_1   is  none ") 
			return  None
	 
		return len(res)

	def __get_day_每日下跌数_wencai_2(self,day): #
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt=day+'下跌家数'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='zhishu')#测试'
		except Exception as e:
			print(e,"__get_day_每日下跌数_wencai_2  is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"__get_day_每日下跌数_wencai_2   is  none ") 
			return  None
		#print(res)	
		columns=res.columns
		col=	[ item for item in columns if "下跌家数" in item]
		if(len(col)>1 or len(col)<=0):
			print('搜索标题内容有误，核对')
		else:
			col=col[0]

		value = res.loc[res['code'] == '883421', col]
		#value = res.loc[df['指数简称'] == '同花顺全A (沪深)', col]
		value=int(list(value)[0])
		return value

	def get_day_每日下跌数_wencai(self,tradeday):  
		#查询文件
		#爬取
		#保存
		#返回值
		#不用检查日期，差不不到返回none

		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日下跌数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日下跌数_有序.json')
		#print(data_file_path)

		#获取文件中交易日期
		if os.path.exists(data_file_path):
	    # 文件存在，读取内容
			if os.path.getsize(data_file_path) > 0:
				with open(data_file_path, 'r',encoding='utf-8') as json_file:
					file_content = json.load(json_file)
			else:#文件存在但是没哟内容这里open会报错，所以处理
				file_content={}
		else:#创建文件
			with open(data_file_path, 'w',encoding='utf-8') as json_file:
				pass#为空
			file_content={}
		pre_days=file_content.keys()#已经爬取的日子

		if(tradeday in pre_days):
			return file_content[tradeday]
		else:
			#这里不通过判断，简化代码，直接爬取就是了
			temp=self.__get_day_每日下跌数_wencai_1(day=tradeday)
			#print(temp)
			if(temp is not None):

				#先保存后
				file_content[tradeday]=temp
				#无序保存
				with open(data_file_path, 'w',encoding='utf-8') as json_file:
					json.dump(file_content, json_file)
				#有序保存
				all_days=list(file_content.keys()) 
				# 将时间字符串转换为 datetime 对象
				datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
				sorted_datetime_objects = sorted(datetime_objects)
				有序alldays=[item.strftime('%Y%m%d') for item in sorted_datetime_objects]
				#print(有序alldays[-1])
				#有序读取
				result=[  (day,file_content[day])     for day in 有序alldays]
				with open(data_file_path_有序, 'w',encoding='utf-8') as json_file:
					json.dump(result, json_file)

				#后返回
				return  temp
			else:#获取不到最新交易日数据，文件中没有匹配日又没有，所以返回为空
				return None


	def update_days_wencai(self,start='20220104',end='20231220'):
		pass 
 


	def update_day_(self,day):#某天数据有误，应该是爬取保存文件有问题，就是重新爬取更新文件
		pass

	def get_days_每日下跌数_wencai(self,start,end):
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日下跌数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日下跌数_有序.json')
		#print(data_file_path)

		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		if start in trade_df:
			sindex = trade_df.index(start)
		else:
			print(start ,"  start 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
			return

		if end in trade_df:
			eindex = trade_df.index(end)
		else:
			print(end ,"  end 输入不是交易日，或者格式有误，这里输入类似  20231215 ")
			return

		sedays=trade_df[sindex:eindex+1]
		#print(sedays)	


		#获取文件中交易日期
		#
		if os.path.exists(data_file_path):
	    # 文件存在，读取内容
			if os.path.getsize(data_file_path) > 0:
				with open(data_file_path, 'r',encoding='utf-8') as json_file:
					file_content = json.load(json_file)
			else:#文件存在但是没哟内容这里open会报错，所以处理
				file_content={}
		else:#创建文件
			with open(data_file_path, 'w',encoding='utf-8') as json_file:
				pass#为空
			file_content={}
		pre_days=file_content.keys()#已经爬取的日子
		
		crawl_days=set(sedays)-set(pre_days)
		#做差集，爬取，保存
		for day in crawl_days:
			print(day)
			temp=self.__get_day_每日下跌数_wencai_1(day)
			file_content[day]=temp

		#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(file_content, json_file)
		
		# #选出设定日期，返回无序
		# result_dict = {key: file_content[key] for key in sedays}
		# return result_dict 
		

		#大多数需要有序，所以这里重新排序。这里代码不做修改了，就是说两种格式代码都有，
		#且以字典无序来处理为主，有序没有读取只是保存
		 	# if os.path.exists(data_file_path):
	 	# 	if os.path.getsize(data_file_path) > 0:
		#  		with open(data_file_path_有序, 'r',encoding='utf-8') as json_file:
		# 			json.dump(有序_file_content, json_file)
		# 		pre_start=有序_file_content[0][0]
		# 		pre_end=有序_file_content[-1][0]	
		# 	else:
		# 		有序_file_content=[]
		# 		pre_start=''
		# 		pre_end=''
		# else:
		# 	有序_file_content=[]
		# 	pre_start=''
		# 	pre_end=''
		# if(len(有序_file_content)==0):
		
		#修改前起始
		#all_days=set(sedays) | set(pre_days) #并集
		# 将时间字符串转换为 datetime 对象
		#datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
		# # 找到最早时间和最晚时间
		# earliest_time = min(datetime_objects)
		# latest_time = max(datetime_objects)
		# # 将结果输出为字符串格式
		# earliest_time_str = earliest_time.strftime('%Y%m%d')
		# latest_time_str = latest_time.strftime('%Y%m%d')
		# earliestindex = trade_df.index(earliest_time_str)
		# latestindex = trade_df.index(latest_time_str)

		# 有序alldays=trade_df[earliestindex:latestindex+1]#有序,d但是可能时间有的没有爬取，太宽泛
		# #这里可以对datetime_objects排序然后转为字符串，代替有序alldays，算了不改了
		# #print(有序alldays)
		# #有序读取
		# result=[]
		# for day in 有序alldays:
		# 	if(day in all_days):#有序alldays太广了，
		# 		result.append( (day,file_content[day]) )
		#修改前结束

		#修改后起始
		all_days=list(file_content.keys()) 
		# 将时间字符串转换为 datetime 对象
		datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
		sorted_datetime_objects = sorted(datetime_objects)
		有序alldays=[item.strftime('%Y%m%d') for item in sorted_datetime_objects]
		#print(有序alldays[-1])
		#有序读取
		result=[  (day,file_content[day])     for day in 有序alldays]
		#修改后结束


		with open(data_file_path_有序, 'w',encoding='utf-8') as json_file:
			json.dump(result, json_file)
	 	
	 	#选出设定日期，返回有序
		start_index = 有序alldays.index(start)
		end_index = 有序alldays.index(end)
		return result[start_index:end_index+1]
	


	def __group_by_week(self,data):#对时间处理，就是同一周放在一起，注意data格式微调代码
		#chatgtp给了几个方法都有问题这里自己写
		grouped_data = []
		current_week = []

		for item in data:
			date_str, value = item
			date_obj = datetime.strptime(date_str, "%Y%m%d")

			if not current_week:#每周的首个交易日
				current_week.append(item)
				# 获取星期几，其中0表示星期一，1表示星期二，以此类推
				day_of_week = date_obj.weekday()
				#本周和这个这周起始交易日的最大差是4-day_of_week
				cha_week=4-day_of_week

			else:
		        # Check if the current date is in the same week as the previous date
				if (date_obj - datetime.strptime(current_week[0][0], "%Y%m%d")).days <= cha_week:
					current_week.append(item)
				else:
					grouped_data.append(current_week)
					current_week = [item]
					date_str, value = item
					date_obj = datetime.strptime(date_str, "%Y%m%d")
					day_of_week = date_obj.weekday()
					cha_week=4-day_of_week

		if current_week:
		    grouped_data.append(tuple(current_week))

		return grouped_data
 


 
	def __group_by_month(self,data):
		# Convert data to DataFrame
		df = pd.DataFrame(data, columns=['Date', 'Value'])
		# Convert string dates to datetime objects
		df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')

		# Group by month considering the entire period
		grouped_data = [ [ (timestamp.strftime('%Y%m%d'), value) for timestamp, value in group.values]
		for name, group in df.groupby(df['Date'].dt.to_period('M'))]

		return grouped_data

	def statistics_and_analysis(self):
		#爬取的数据自身的一下属性来统计研究，周期性概率性是个重要目标，--波段之门的启发
		##统计大于3000上涨，每周，每月，每年次数
		##大概用同花顺看了一下，
		data=self.get_days_每日下跌数_wencai('20220104','20231220')
		#print(data)
		data=[ item for item in data if item[1] >= 4000]#
		print([ item[0] for item in data ])

		# data_week=self.__group_by_week(data)
		
		# print(data_week)
		
		# i_num_week=[len(item) for item in data_week]#每周含有元组数，就是没有符合条件个数
		# print(i_num_week)
		# i4_num_week=[ item[0] for item in data_week if len(item)==3]
		
		# print(i4_num_week)

	def statistics_and_analysis1(self):
		#今日下跌超过4000，然后今天上涨明天继续涨的概率
		#这里死博情绪冰点之后，反弹，可能不反弹，但是这波博反弹，修复预期，在，看什么再涨
		#
		pass




if __name__ == '__main__':
	s=每日上涨数类()
	s.update_days_wencai()
	#s.statistics_and_analysis()
	#a=s.get_day_每日上涨数_wencai(tradeday='20231218')
	#print(a)
	# data=s.get_days_每日上涨数_wencai('20231214','20231219')
	# print(data)
	

	# # print(data)

	# b=每日下跌数类()
	# data=b.get_day_每日下跌数_wencai(tradeday='20231218')
	# print(data)
	# data=b.get_days_每日下跌数_wencai('20231214','20231219')
	# print(data)










	pass