
class 每日涨停封单额类( ):
 
	def __init__(self):
		pass

	def __get_day_每日涨停封单额_wencai(self,tradeday='20231217'):
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt=tradeday+'涨停封单额，去掉st，去掉北交所，去掉科创板'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日上涨跌数_wencai   is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"get_day_每日上涨跌数_wencai   is  none ") 
			return  None
		temp=[ item for item in res.columns if '涨停封单额' in item ]

		if(len(temp)==1):
			temp_col=temp[0]
		else:
			print('error 涨停封单金额 不在结果中')
			return None

		return round(sum(res[temp_col])/100000000,2)
 
	def __get_day_每日最大涨停封单额_wencai(self,tradeday='20231217'):
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt=tradeday+'涨停封单额，去掉st，去掉北交所，去掉科创板'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"get_day_每日上涨跌数_wencai   is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"get_day_每日上涨跌数_wencai   is  none ") 
			return  None
		temp=[ item for item in res.columns if '涨停封单额' in item ]

		if(len(temp)==1):
			temp_col=temp[0]
		else:
			print('error 涨停封单金额 不在结果中')
			return None

		return round(max(res[temp_col])/100000000,2)
 


	def get_day_每日涨停封单额_wencai(self,tradeday):  
		#查询文件
		#爬取
		#保存
		#返回值
		#不用检查日期，差不不到返回none
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日涨停封单额_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日涨停封单额_有序.json')
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
			temp=self.__get_day_每日涨停封单额_wencai(tradeday=tradeday)
			# print(temp)
			# return 
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

	def get_day_每日最大涨停封单额_wencai(self,tradeday):  
		#查询文件
		#爬取
		#保存
		#返回值
		#不用检查日期，差不不到返回none
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日最大涨停封单额_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日最大涨停封单额_有序.json')
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
			temp=self.__get_day_每日最大涨停封单额_wencai(tradeday=tradeday)
			# print(temp)
			# return 
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


	def get_days_每日涨停封单额_wencai(self,start,end):
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日涨停封单额_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日涨停封单额_有序.json')
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
		#print(crawl_days)
		#方案一
		#做差集，爬取，保存
		for day in crawl_days:
			print(day)
			temp=self.__get_day_每日涨停封单额_wencai(day)
			if(temp is not None):
				file_content[day]=temp

		#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(file_content, json_file)

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
	 	
	 	#选出设定日期，返回有序
		start_index = 有序alldays.index(start)
		end_index = 有序alldays.index(end)
		return result[start_index:end_index+1]
		#方案二
		#这里不用一次次调取，而ak接口能依次读取所有历史
		# if(len(crawl_days)>0):#重新爬取保存所有历史数据
		# 	try:
		# 		df1=ak.stock_zh_index_daily_em(  symbol="sh000001")
		# 		df2=ak.stock_zh_index_daily_em(  symbol="sz399001")

		# 	except Exception as e:
		# 		raise e
		# 	index_min=min(len(df1),len(df2))
		# 	#截取相同不部分，因为起始时间可能不同 
		# 	df1_amount = df1['amount'][-index_min:]
		# 	df2_amount = df2['amount'] [-index_min:]
		# 	HSamount=[ round((i+j)/100000000,1)  for i,j in  zip(list(df1_amount),list(df2_amount))]
			
		# 	df_date=list(df1['date'][-index_min:])
		# 	file_content={ i[:4]+i[5:7]+i[8:]  :j  for i,j in   zip(df_date,HSamount)}
		# 	#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		# 	with open(data_file_path, 'w',encoding='utf-8') as json_file:
		# 		json.dump(file_content, json_file)

		# 	result=[  [i[:4]+i[5:7]+i[8:] ,j]  for i,j in   zip(df_date,HSamount)]
		# 	with open(data_file_path_有序, 'w',encoding='utf-8') as json_file:
		# 		json.dump(result, json_file)
		# else:
		# 	with open(data_file_path_有序, 'r',encoding='utf-8') as json_file:
		# 		result=json.load(json_file)
		# 	df_date=[ item[0]  for item in result]
			

		# try:
		# 	start_index = df_date.index(start)
		# 	end_index = df_date.index(end)
		# except Exception as e:
		# 	print('输入正确交易日时间，注意格式 20221217,且必须是交易日')
		# 	raise e			#选出设定日期，返回有序
		# #print(start_index,end_index)
		# #print(result)
		# return result[start_index:end_index+1]
	def get_days_每日最大涨停封单额_wencai(self,start,end):
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日最大涨停封单额_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日最大涨停封单额_有序.json')
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
		#print(crawl_days)
		#方案一
		#做差集，爬取，保存
		for day in crawl_days:
			print(day)
			temp=self.__get_day_每日最大涨停封单额_wencai(day)
			if(temp is not None):
				file_content[day]=temp

		#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(file_content, json_file)

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
	 	
	 	#选出设定日期，返回有序
		start_index = 有序alldays.index(start)
		end_index = 有序alldays.index(end)
		return result[start_index:end_index+1]
		#方案二
		#这里不用一次次调取，而ak接口能依次读取所有历史
		# if(len(crawl_days)>0):#重新爬取保存所有历史数据
		# 	try:
		# 		df1=ak.stock_zh_index_daily_em(  symbol="sh000001")
		# 		df2=ak.stock_zh_index_daily_em(  symbol="sz399001")

		# 	except Exception as e:
		# 		raise e
		# 	index_min=min(len(df1),len(df2))
		# 	#截取相同不部分，因为起始时间可能不同 
		# 	df1_amount = df1['amount'][-index_min:]
		# 	df2_amount = df2['amount'] [-index_min:]
		# 	HSamount=[ round((i+j)/100000000,1)  for i,j in  zip(list(df1_amount),list(df2_amount))]
			
		# 	df_date=list(df1['date'][-index_min:])
		# 	file_content={ i[:4]+i[5:7]+i[8:]  :j  for i,j in   zip(df_date,HSamount)}
		# 	#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		# 	with open(data_file_path, 'w',encoding='utf-8') as json_file:
		# 		json.dump(file_content, json_file)

		# 	result=[  [i[:4]+i[5:7]+i[8:] ,j]  for i,j in   zip(df_date,HSamount)]
		# 	with open(data_file_path_有序, 'w',encoding='utf-8') as json_file:
		# 		json.dump(result, json_file)
		# else:
		# 	with open(data_file_path_有序, 'r',encoding='utf-8') as json_file:
		# 		result=json.load(json_file)
		# 	df_date=[ item[0]  for item in result]
			

		# try:
		# 	start_index = df_date.index(start)
		# 	end_index = df_date.index(end)
		# except Exception as e:
		# 	print('输入正确交易日时间，注意格式 20221217,且必须是交易日')
		# 	raise e			#选出设定日期，返回有序
		# #print(start_index,end_index)
		# #print(result)
		# return result[start_index:end_index+1]

	def update_days_manmod(self,tradedays=['20211224'],data={}):#某天数据有误，应该是爬取保存文件有问题，就是重新爬取更新文件
		#目前用到此处一个是爬取时候多线程的问题吧导致接口数据是对的但是保存有问题！所以这里通过输入tradedays=['20211224']，,data={}
		#来重新爬取tradeday，data是空的
		#第二种是data是不是空，那么就把一个是tradedays重新爬取，然后再用data填充，注意先后顺序

		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日涨停封单额_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日涨停封单额_有序.json')
		#print(data_file_path)
		if(len(tradedays)>0):
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

			#删除需要重新爬取的days
			for iday in tradedays:
				file_content.pop(iday, None)#None是key不存在返回，否则返回删除的数值
			

			#保存修改内容

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

			#重新爬取
			for iday in tradedays:
	 			self.get_day_每日涨停封单额_wencai(tradeday=iday)

		elif(len(data)>0):#需要手动修改内容
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
			for key, value in data.items():
				file_content[key]=value

			#保存修改内容

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

	def update_days_ak(self,start='20180104',end='20231220'):
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
			data=s.get_days_每日涨停封单额_wencai(item[0],item[1])
 


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
		pass

	def statistics_and_analysis(self):
		pass

	#把数据写入到html模板中展示
	def get_chart_html_template1(self,dynamic_data,name,iswebopen=0,src_html_path= \
		'../../../html_template1/templates/template.html',des_html_path='./static/每日涨停封单额.html'):
		#运行这个 Python 脚本，它将生成一个 HTML 文件（比如 output.html）
		#其中包含动态数据的 JavaScript 代码。打开这个 HTML 文件，
		#你应该能够看到 Highcharts 图表，其中的曲线数据是你在 Python 中指定的动态数据。
		#读取模板文件
		with open(src_html_path, 'r', encoding='utf-8') as template_file:
		    template_content = template_file.read()

		# 创建 Jinja2 模板对象
		template = Template(template_content)

		# 使用模板渲染 HTML，传递动态数据
		#在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
		#模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
		#html_output = template.render(data=dynamic_data)
		html_output = template.render(data=dynamic_data )
		# 将生成的 HTML 写入文件
		output_file_path=des_html_path
		with open(output_file_path, 'w', encoding='utf-8') as output_file:
		    output_file.write(html_output)
		if(iswebopen==1):
			# 用默认浏览器打开生成的 HTML 文件
			webbrowser.open(os.path.abspath( output_file_path))#用output_file_path  有问题

	def get_chart_html_template2(self,dynamic_data ,iswebopen=0,src_html_path= \
		'../../../html_template2/templates/template_highcharts_核密度图.html',des_html_path='./static/每日涨停封单额_核密度图.html'):
		#这里是采用搜索替代字符串替代方式，统一了文字以后都用这段文字就好了

		with open(src_html_path, 'r', encoding='utf-8') as template_file:
		    template_content = template_file.read()
		substr='//统一替代文字说明尽量用统一文字方便后面统一代码'
		substr_list=[substr]*len(dynamic_data[1])
		for substring ,item in zip(substr_list,dynamic_data):
			#print(substring)
			#print(item)
			template_content = template_content.replace(substring, item,1)

		#print(template_content)
		# 将生成的 HTML 写入文件
		output_file_path=des_html_path
		with open(output_file_path, 'w', encoding='utf-8') as output_file:
		    output_file.write(template_content)
		if(iswebopen==1):
			# 用默认浏览器打开生成的 HTML 文件
			webbrowser.open(os.path.abspath( output_file_path))#用output_file_path  有问题

	def get_chart_每日涨停封单额_核密度图(self,start='20220104',end='20231220',iswebopen=0):

		#统计数据
		data=self.get_days_每日涨停封单额_wencai(start=start,end=end)
		#print(data)
		data=[  float(item[1])  for item in data]
		#print(data)
		#设置区间，20个区间，bins是区间的最大最小的list
		bins = np.linspace(min(data), max(data), 20)
		bins= [float(item)  for item in bins]
		counts, bins = np.histogram(data, bins=bins)
		counts=[ round(item/len(data),4)  for item in counts]
		counts1= [ round(sum(counts[:i]),4)      for i in range(len(counts))]
		xAxis='categories: '+str(list(bins))+','
		data='data: '+str(list(counts))+','
		data1='data: '+str(list(counts1))+','
		self.get_chart_html_template2([xAxis,data,xAxis,data1] ,iswebopen=iswebopen,src_html_path= \
		'../../../html_template2/templates/template_highcharts_核密度图.html',des_html_path='./static/每日涨停封单额_核密度图.html') 




	def get_chart_每日涨停封单额(self,start='20220104',end='20231220',iswebopen=0):
 		#测试模板案例1  ：   左侧是上证指数，右侧是统计的每日最高连板数，

		#上涨指数数据
		index_df = ak.stock_zh_index_daily_em(symbol="sh000001")
		#index_df=index_df.tail(5)
		start_frmt=start[:4]+'-'+start[4:6]+'-'+start[6:]
		#start_index=index_df[index_df['date'] == start_frmt].index
		end_frmt=end[:4]+'-'+end[4:6]+'-'+end[6:]
		#end_index=index_df[index_df['date'] == end_frmt].index
		try:
			h1 = index_df.index[index_df['date'] == start_frmt].tolist()[0]
			h2 = index_df.index[index_df['date'] == end_frmt].tolist()[0]
		except Exception as e:
			print('输入 start end 可能不是交易日')
			raise e

		# 提取行号在 (h1, h2) 范围内的所有行
		selected_rows = index_df.loc[h1 : h2 ]
		#print(selected_rows)
		selected_index_data=[ [ (datetime.strptime(idate, "%Y-%m-%d")).timestamp()*1000   ,idata]   for idate,idata in zip(selected_rows['date'],selected_rows['close'])  ]
		#print(selected_index_data)

		#统计数据
		data=self.get_days_每日涨停封单额_wencai(start=start,end=end)
		#print(data)
		
		每日_data=[ [ (datetime.strptime(idata[0], "%Y%m%d")).timestamp()*1000   ,float(idata[1])]   for idata in data]
		#print(每日上涨数_data)

		#hightchart会自动补全非交易日数据且有问题，所以这里就是使用上个交易日数据来补全

		#格式化
		左纵=0
		右纵=1
		dydata={'上证指数':[selected_index_data,左纵],'每日涨停封单额':[每日_data,右纵]}
		self.get_chart_html_template1(dydata,"无",iswebopen=iswebopen)
		#生成html

	def get_chart_highchart(self,data_左,data_右,start='20220104',end='20231220',iswebopen=0,des_html_path='./static/测试.html'):
 		#测试模板案例1  ：   左侧是上证指数，右侧是统计的每日最高连板数，
		dydata={}
		左纵=0
		右纵=1
		for key,value in data_左.items():
			temp=[ [ (datetime.strptime(idata[0], "%Y%m%d")).timestamp()*1000   ,float(idata[1])]   for idata in value]
			dydata[key]=[temp,左纵]
		for key,value in data_右.items():
			temp=[ [ (datetime.strptime(idata[0], "%Y%m%d")).timestamp()*1000   ,float(idata[1])]   for idata in value]
			dydata[key]=[temp,右纵]

		self.get_chart_html_template1(dydata,"无",iswebopen=iswebopen,des_html_path=des_html_path)
		#生成html



		pass
if __name__ == '__main__':

	import warnings
	import numpy as np
	import   pywencai
	import os,sys
	import  json
	from  datetime import datetime
	import akshare as ak
	import webbrowser
	from jinja2 import Template






	a=每日涨停封单额类()
	#c=a.get_day_每日涨停封单额_wencai( tradeday='20231217')
	#print(c)
	#a.update_days_manmod(tradedays=['20190605','20191113' ],data={})
	#c=a.get_day_每日涨停封单额_wencai( tradeday='20211224')
	#print(c)

	bb=a.get_days_每日涨停封单额_wencai( start='20230103',end='20231222')
	#print(bb)
 
	#a.get_chart_每日涨停封单额(start='20230103',end='20231222',iswebopen=1)
	#a.get_chart_每日两市流通市值_核密度图(start='20190103',end='20231222',iswebopen=1)
	#修补曲线
	#a.update_days_manmod(tradedays=['20180605','20180611' ,'20180920' ],data={})

	import 每日最高连板数 
	e=每日最高连板数.每日最高连板数类()
	ee=e.get_days_每日最高连板数_wencai(start='20230103',end='20231222')
	#print(ee)


	#a.get_chart_highchart(data_左={'每日涨停封单额':bb,},data_右={'每日最高连板数':ee},iswebopen=1,des_html_path='./static/测试.html')

	dd=a.get_days_每日最大涨停封单额_wencai( start='20230103',end='20231222')

	a.get_chart_highchart(data_左={'每日涨停封单额':bb,'每日最大涨停封单额':dd},data_右={'每日最高连板数':ee},iswebopen=1,des_html_path='./static/测试.html')





