import   pywencai
import os,sys
import  json
from  datetime import datetime
import akshare as ak
import webbrowser
from jinja2 import Template

class 每日涨跌停家数类():

	def __init__(self ):
		pass


	def __get_day_每日涨跌停家数_wencai(self,tradeday='20231217'):		
		#通过问财爬取，历史数据，然后保存到熬本地
		searchtxt = tradeday+'涨停数,去掉st,去掉北交所'
		res = None
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=False,query_type='stock')#测试'
		except Exception as e:
			pass
		if(res is None or len(res)==0):
			ztnum=0
		else:
			ztnum=len(res)

		res = None
		searchtxt = tradeday+'跌停数,去掉st,去掉北交所'
		try:
			#这里没有循环，因为没有必要，首页内容，所以加快爬取速度
			res = pywencai.get(query=searchtxt,loop=False,query_type='stock')#测试'
		except Exception as e:
			pass
	 	
		if(res is None or len(res)==0):
			dtnum=0
		else:
			dtnum=len(res)
		return [ztnum,dtnum]


	def get_day_每日涨跌停家数_wencai(self,tradeday):  
		#查询文件
		#爬取
		#保存
		#返回值
		#不用检查日期，差不不到返回none
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日涨跌停家数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日涨跌停家数_有序.json')
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
			temp=self.__get_day_每日涨跌停家数_wencai(tradeday=tradeday)
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



	def get_days_每日涨跌停家数_wencai(self,start,end):
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日涨跌停家数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日涨跌停家数_有序.json')
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
			temp=self.__get_day_每日涨跌停家数_wencai(day)
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

	def update_days_manmod(self,tradedays=['20211224'],data={}):#某天数据有误，应该是爬取保存文件有问题，就是重新爬取更新文件
		#目前用到此处一个是爬取时候多线程的问题吧导致接口数据是对的但是保存有问题！所以这里通过输入tradedays=['20211224']，,data={}
		#来重新爬取tradeday，data是空的
		#第二种是data是不是空，那么就把一个是tradedays重新爬取，然后再用data填充，注意先后顺序

		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\每日涨跌停家数_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\每日涨跌停家数_有序.json')
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
	 			self.get_day_每日涨跌停家数_wencai(tradeday=iday)

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
			data=s.get_days_每日涨跌停家数_wencai(item[0],item[1])
 


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
		'../../../html_template1/templates/template.html',des_html_path='./static/每日涨跌停家数.html'):
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


	def get_chart_每日涨跌停家数(self,start='20220104',end='20231220',iswebopen=0):
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
		data=self.get_days_每日涨跌停家数_wencai(start=start,end=end)
		#print(data)
		
		每日_data涨停=[ [ (datetime.strptime(idata[0], "%Y%m%d")).timestamp()*1000   ,int(idata[1][0])]   for idata in data]
		每日_data跌停=[ [ (datetime.strptime(idata[0], "%Y%m%d")).timestamp()*1000   ,int(idata[1][1])]   for idata in data]


		#hightchart会自动补全非交易日数据且有问题，所以这里就是使用上个交易日数据来补全

		#格式化
		左纵=0
		右纵=1
		dydata={'上证指数':[selected_index_data,左纵],'每日涨停家数':[每日_data涨停,右纵],'每日跌停家数':[每日_data跌停,右纵]}
		self.get_chart_html_template1(dydata,"无",iswebopen=iswebopen)
		#生成html

if __name__ == '__main__':








	a=每日涨跌停家数类()
	b=a.get_day_每日涨跌停家数_wencai( tradeday='20231229')
	print(b)
	#d=a.get_days_每日涨跌停家数_wencai( start='20231211',end='20231220')
	#print(d)
	#a.get_chart_每日涨跌停家数(start='20231225',end='20231229',iswebopen=1)
	#a.update_days_manmod(tradedays=['20230704','20230807'],data={})