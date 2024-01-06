import akshare as ak
import time
import datetime
from datetime import timedelta
from selenium import webdriver  
#https://blog.csdn.net/jsy6666/article/details/129802261?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-129802261-blog-129605194.235^v39^pc_relevant_anti_vip_base&spm=1001.2101.3001.4242.1&utm_relevant_index=3
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
# stock_lhb_detail_em_df = ak.stock_lhb_detail_em(start_date="20231205", end_date="20231205")
# #print(stock_lhb_detail_em_df)
# print(stock_lhb_detail_em_df.columns)

# print(stock_lhb_detail_em_df['市场总成交额'])
import sys
import os


class 龙虎榜( ):
	"""docstring for ClassName"""
	def __init__( self ):
		pass

	def stocks_每日龙虎榜(self,day='20200629'):
		#print(day)
		df = ak.stock_lhb_detail_em(start_date=day, end_date=day)
		codes=list(df['代码'])
		return codes

	def get_stock_每日龙虎榜_东方财富(self,day='2020-06-29',stock='000032'):
		url="https://data.eastmoney.com/stock/lhb,{},{}.html".format(day,stock)
 		#安装google就可以了   
 		#https://blog.csdn.net/jsy6666/article/details/129802261?utm_medium=distribute.pc_relevant.none-task-blog-2~default~baidujs_baidulandingword~default-0-129802261-blog-129605194.235^v39^pc_relevant_anti_vip_base&spm=1001.2101.3001.4242.1&utm_relevant_index=3
 
		service = ChromeService(executable_path=ChromeDriverManager().install())
		# chrome_options = Options()
		# chrome_options.add_argument("--headless")  # 使浏览器在后台运行 有问题
		driver = webdriver.Chrome(service=service)
		driver.set_window_size(100, 100)#打开网页大小
		driver.set_window_position(100, 500)#网页位置
		driver.get(url)
		time.sleep(3)#必须简单的等待加载
		#print(driver.page_source)
		dynamic_content = driver.page_source#页面不存在可能返回不确定页面
		driver.quit()
		#print(dynamic_content) 
		soup  = BeautifulSoup(dynamic_content,'html.parser')
		link_elements=soup.find_all('div',class_='sub-content')
		#print(len(link_element))
		#个股可能同时又多个多个上榜理由，
		#
		if(len(link_elements)==1):#看上榜原因，多个上榜理由，这里不看，只看数据以后要看在写函数处理
		# 	print("个股多个原因上榜，")#除了三日，其他理由数据应该是一样的，以后补充
		# 	for link_i in range(len(link_elements)):
		# 		reason=link_element[i].div.div.string#上榜理由
		# 		print(reason)
		# 		if("连续三个交易日内" in reason):
		# 			pass
		# 		else:
		# 			link_element=link_element[i]#非三日数据，而是单日数据，无论上理由，都应该是一样数据
		# 			#所以选一个看一个
			pass
		elif(len(link_elements)>1):
			pass
		else:
			print("龙虎榜网页爬取有问题")
			return None

		out_lhb=[]
		for link_element in link_elements:
			#link_element=link_elements[0]#目前只有一个 'div',class_='sub-content'
			title=link_element.div.div.string#上榜理由
			#print(link_element.div)#z只有一个div所可以直接用
			tables=link_element.find_all('table')
			bug_table=tables[0]
			#print(tables[0])
			sell_table=tables[1]
			#print(tables[1])
			bugs_trs=bug_table.tbody.find_all('tr')#具体明细 ,五个买入
			#print(bugs_trs)	
			buy_res={}	
			for bugs_tr in bugs_trs:
				#print(bugs_tr)
				bugs_tr_tds=bugs_tr.find_all('td')#五个列，统计角度
				#print(bugs_tr_tds)
				buyindex=bugs_tr_tds[0].string
				#print(buyindex )
				bugs_tr_tds[1]#营业部
				buydpt=bugs_tr_tds[1].div.a.string
				#print(buydpt)
				bug_amount=bugs_tr_tds[2].span.string#买入金额
				#print(bug_amount)
				buy_res[buyindex]={"营业部":buydpt,"买入金额":bug_amount}

			sells_trs=sell_table.tbody.find_all('tr')#具体明细 ,五个买入
	 		#sells_trs_tds=sells_trs.find('td')# ，统计角度
			#print(sells_trs)

			#len(sells_trs)>1 and len(sells_trs)<=6):
			all_sum=sells_trs[-1]#最后统计结果
			sells_trs=sells_trs[:-1]#只有卖
			sell_res={}	
			for sells_tr in sells_trs:
				#print(bugs_tr)
				sells_tr_tds=sells_tr.find_all('td')# ，统计角度
				#print(bugs_tr_tds)
				sellindex=sells_tr_tds[0].string
				#print(sellindex)
				#sells_tr_tds[1]#营业部
				selldpt=sells_tr_tds[1].div.a.string
				#print(selldpt) 
				sell_amount=sells_tr_tds[4].span.string#买入金额
				#print(bug_amount)
				sell_res[sellindex]={"营业部":selldpt,"卖出金额":bug_amount}


			lhb={'bug':buy_res,'sell':sell_res,"reason":title}#要爬取条目以后再扩充
			out_lhb.append(lhb)
		return out_lhb




	def   get_龙虎榜_东方财富(self,start,end):
		#读取历史爬取记录
		current_dir = os.path.dirname(os.path.abspath(__file__)) 
		#print(current_dir)
		filename="龙虎榜" + ".json"
		old_filename='old_'+filename
		file_path = os.path.join(current_dir,filename)
		old_file_path = os.path.join(current_dir,old_filename)


		##处理时间
		trade_date_df = ak.tool_trade_date_hist_sina()#获取交易日
		trade_date_list = trade_date_df["trade_date"].astype(str).tolist()
		#print(trade_date_list)#时间带 -
		if(start==''):#返回，为了更好兼容这个代码，上层处理更多情况，这里不处理，必须输入start
			print("start is null,input start time!")
			return
		if('-' not in start):#获取交易日的接口格式是"2023-11-01"，所以做处理
			start=start[:4]+'-'+start[4:6]+'-'+start[6:8]
		tempday=datetime.datetime.strptime(start,"%Y-%m-%d") 
		while datetime.datetime.strftime(tempday,"%Y-%m-%d")  not in trade_date_list:  # 如果当前日期不在交易日期列表内，则当前日期天数减一
			tempday =  tempday + datetime.timedelta(days=1)
		if(datetime.datetime.strftime(tempday,"%Y-%m-%d") not in trade_date_list):
			print(tempday," start iserror,input start time!")
			return
		start=datetime.datetime.strftime(tempday,"%Y-%m-%d")#通过输入确定start

		if(end==''):
			tempday = date.today()
			tempday = datetime.datetime.strftime(tempday,"%Y-%m-%d")
			while(tempday not in  trade_date_list):#今天是周末或假期
				tempday=datetime.datetime.strptime(tempday,"%Y-%m-%d")-datetime.timedelta(days=1)
				tempday=datetime.datetime.strftime(tempday,"%Y-%m-%d")
			if(tempday not in trade_date_list):
				print(tempday,"end iserror,input start time!")
				return
			end=tempday
		else:
			if('-' not in end):#获取交易日的接口格式是"2023-11-01"，所以做处理
				tempday=end[:4]+'-'+end[4:6]+'-'+end[6:8]
			#print(tempday)
			tempday=datetime.datetime.strptime(tempday,"%Y-%m-%d")
			while datetime.datetime.strftime(tempday,"%Y-%m-%d")  not in trade_date_list:  # 如果当前日期不在交易日期列表内，则当前日期天数减一
				tempday =  tempday - datetime.timedelta(days=1)
			if(datetime.datetime.strftime(tempday,"%Y-%m-%d") not in trade_date_list):
				print(tempday,"end iserror,input start time!")
				return
			end=datetime.datetime.strftime(tempday,"%Y-%m-%d")

		#print("set:",start,end)，需要爬取的如下，#得到设置的start  end
		tradedays=trade_date_list[trade_date_list.index(start):trade_date_list.index(end)+1]#g根据输入获得tradedays

		#为了保持交易日的list的顺序，这里处理一下防止中间有些日子没有爬取数据，
		# 检查文件是否存在
		if os.path.exists(file_path):
		    # 文件存在，读取内容
			with open(file_path, 'r') as json_file:
				pre_data = json.load(json_file)
				if(len(pre_data)==0):#空文件
					temp_tradedays=tradedays #上面是差集，这里也是差集，为0而已，扩大版的所有需要处理的天数
					all_deal_tradedays=tradedays
					print(f'{file_path} is null. Skipping...')
					if(len(temp_tradedays)==0):
						print(f'no days is ok return...')
						return None 

				#非空文件
				pre_tradedays=pre_data['date']
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
	 		    
				#print("kuoda:",all_deal_tradedays[0],all_deal_tradedays[-1])
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
				return  None

			#print(tradedays)
			#结果队列

			#文档读取结果，处理时间
       #爬取需要爬取那些days数据
		days_lhb={}
		for day in temp_tradedays :
			print(day)
			codes=self.stocks_每日龙虎榜(day=day.replace("-", ""))
			day_lhb={}
			for code in codes:
				print(code)
				lhb=self.get_stock_每日龙虎榜_东方财富(day=day,stock=code)#多个理由
				day_lhb[code]=lhb

			days_lhb[day]=day_lhb

	#合并数据局
		if(os.path.exists(file_path)):
			days_lhb.update(pre_data['data']) 

		out={"date":all_deal_tradedays,"data":days_lhb}
		# 指定保存的文件路径
		
		if os.path.exists(file_path):
			if os.path.exists('old_'+file_path):
				os.remove('old_'+file_path)
				os.rename(file_path, 'old_'+file_path)#备份
			else:
				os.rename(file_path, 'old_'+file_path)#备份

			# 使用 json.dump 将字典保存为 JSON 文件
		with open(file_path, 'w') as json_file:
			json.dump(out, json_file)

		#print(out)
		return out#注意格式




if __name__ == '__main__':
	#龙虎榜( ).get_stock_每日龙虎榜_东方财富(day='2023-11-01',stock='002682')
	龙虎榜( ).get_龙虎榜_东方财富(start ='20231121',end ="20231205")
	#龙虎榜().stocks_每日龙虎榜(day='20231205')
	#600351
	#print(龙虎榜().stocks_每日龙虎榜( day='20231101'))

