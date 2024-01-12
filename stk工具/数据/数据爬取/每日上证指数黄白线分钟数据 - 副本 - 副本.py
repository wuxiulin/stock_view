#这个数据是需要每天定时下载的，没找到方法补全历史数据
#所以需要每天手动执行代码，保存这天是数据，以后方便用！
#这里爬取方式很偷巧，不正规，没想到好方式，所以但是可以借鉴以后canvas爬取方式！


import requests
import time
import subprocess
import json
import akshare as ak
from datetime import datetime,timedelta
import os,sys
import shutil
from PIL import ImageGrab
import pyautogui
import pygetwindow as gw
import cv2
import numpy as np
import easyocr
import re
import execjs
class 上证指数黄白线分钟数据类( ):
	def __init__(self ):
		pass


	def get_today_上证指数黄白线分钟数据_wencai_js(self):
		pass





	def __get_today_每日上证指数黄白线分钟数据_ths_exe(self,tradeday):
		#tradeday一定是交易日，
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		todaynow = datetime.now()
		last_date = todaynow
		today_date_string = todaynow.strftime("%Y%m%d")
		last_date_string =today_date_string
		while True:
			if(last_date_string not in trade_df ):
				last_date=last_date-timedelta(days=1)#最近上一个交易日
				last_date_string = last_date.strftime("%Y%m%d")
			else:
				break
		#print(last_date_string)#最近交易日
		det=datetime.strptime(last_date_string,"%Y%m%d")   -  datetime.strptime(tradeday ,"%Y%m%d") 
		#print(det.days)
		#他与最新



		#快速爬取同花顺截图，不用分析，防止意外，截图要快
		self.get_pics_ths(offset=det.days,tradeday=tradeday)


		# 设置开始时间和结束时间
		start_time = datetime.strptime("09:30", "%H:%M")
		end_time = datetime.strptime("15:00", "%H:%M")
		# 初始化当前时间为开始时间
		current_time = start_time
		# 时间间隔为1分钟
		time_interval = timedelta(minutes=1)
		# 存储结果的数组
		time_strings = []
		# 生成时间字符串数组
		while current_time <= end_time:
		    time_strings.append(current_time.strftime("%H%M"))
		    current_time += time_interval
		time_strings=time_strings[:121]+time_strings[210:]#去掉中午休息
		
		result={}
		for timestamp in time_strings:
			print(timestamp)
			#转灰度图
			tpth=self.pretreatment_pic(pic_path='./temp/temp1/{}.png'.format(timestamp))
			#解析
			data=self.analysis_pic_EasyOCR(pic_path=tpth)

			result[timestamp]=data
		print(result)
		print('**********************************************数据错误***********************************************************')
		for timestamp in time_strings:
			if(result[timestamp]["上涨数量"] ==''  or result[timestamp]["下跌数量"] =='' ):
				print(timestamp,'erro 检查修改代码')
		print('****************************************************************************************************************')

		return result
	def update_day_上证指数黄白线分钟数据(self,day):#就是某天的数据有误，重新爬取更新
		pass


	def get_day_上证指数黄白线分钟数据(self,tradeday='20231217'):
 
		#获取期间交易日list
		trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\上证指数黄白线分钟数据_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\上证指数黄白线分钟数据_有序.json')
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
		#print(tradeday)

		if(tradeday in pre_days):
			return file_content[tradeday]
		else:
			#添加附带功能，就是更新今天如果是交易日更新最新数据
			todaynow = datetime.now()
			today_date_string = todaynow.strftime("%Y%m%d")
			last_date_string =today_date_string
			while True:
				if(last_date_string not in trade_df ):
					todaynow=todaynow-timedelta(days=1)#最近上一个交易日
					last_date_string = todaynow.strftime("%Y%m%d")
				else:
					break
			#print(today_date_string,last_date_string)
			if(last_date_string==today_date_string):#今天是交易日，然后15点后在执行
				if(todaynow > datetime.strptime(today_date_string+' 15:01:00','%Y%m%d %H:%M:%S')  or 
					todaynow < datetime.strptime(today_date_string+' 05:00:00','%Y%m%d %H:%M:%S')#5点应该还有昨天的数据
					):
					temp=self.get_today_上证指数黄白线分钟数据_wencai_js()
				else:
					temp=None
			elif(last_date_string not in pre_days):#今天是非交易日 如果没有保存过
				temp=self.get_today_上证指数黄白线分钟数据_wencai_js()

			#print(temp)
			if(temp is not None):
				tempday=list(temp.keys())[0]
				#先保存后
				if(tempday not in pre_days ):
					file_content[tempday]=temp[tempday]
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

				#后判断是否符合
				if(tempday ==tradeday):
					return temp
				else:
					return None

			else:#获取不到最新交易日数据，文件中没有匹配日又没有，所以返回为空
				return None

	def get_days_上证指数黄白线分钟数据(self,start,end):

		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\上证指数黄白线分钟数据_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\上证指数黄白线分钟数据_有序.json')
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
		
		#添加附带功能，就是更新今天如果是交易日更新最新数据
		todaynow = datetime.now()
		today_date_string = todaynow.strftime("%Y%m%d")
		if((today_date_string in trade_df and today_date_string not in pre_days)   #交易日且不再文件中
			or (today_date_string not in trade_df )):#如果不是交易日，这里爬取吧，不细写了，条件太多了算了
			self.get_day_上证指数黄白线分钟数据(tradeday='19900101')#这函数附带效果是更新最新数据，更新最新日，后面方便

		crawl_days=set(sedays)-set(pre_days)
		if(len(crawl_days)>0):
			print('数据缺失,目前没法爬取补全')
			return None
		else:
			all_days=list(file_content.keys()) 
			# 将时间字符串转换为 datetime 对象
			datetime_objects = [datetime.strptime(time_str, '%Y%m%d') for time_str in all_days]
			sorted_datetime_objects = sorted(datetime_objects)
			有序alldays=[item.strftime('%Y%m%d') for item in sorted_datetime_objects]
			result=[  (day,file_content[day])     for day in 有序alldays]
			#这里应该有保存有序，但是这个特殊无法爬取历史数据，座最开始已经更新最新，所以这里不用保存
			start_index = 有序alldays.index(start)
			end_index = 有序alldays.index(end)
			return result[start_index:end_index+1]
 
		return
		#如果以后有方法爬取历史数据，能补缺，下面是继续执行的代码
		#做差集，爬取，保存
		for day in crawl_days:
			print(day)
			temp= []	#get_day_每日上涨跌数_wencai_1(day)
			file_content[day]=temp

		#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(file_content, json_file)
		#有序
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





	def 打开同花顺定位界面(self,offset,tradeday):
		#这里截图修改了代码，尽量简单，方便后面图片识别，所以这里 F  U  这里没有B股，其次是不包括涨幅为0的
		#这是值是沪深A，不包括北交所，所以注意，需要包括要改同花顺代码，以后再说吧
		title_substring="同花顺(v"
		# 获取当前所有窗口的标题
		all_titles = gw.getAllTitles()
		# 查找包含特定字符串的窗口标题
		matching_titles = [title for title in all_titles if title_substring in title]
		if(len(matching_titles)>1):
			for title in matching_titles :
				print(title)
			print('同花顺软件多个标题窗口')
			return

		elif(len(matching_titles)==0):#
			#subprocess.run([r'D:/ths/hexin.exe'], check=True)#会阻塞这里
			subprocess.Popen([r'D:/ths/hexin.exe'])
			time.sleep(5)
			#验证已经打开
			all_titles = gw.getAllTitles()
			# 查找包含特定字符串的窗口标题
			matching_titles = [title for title in all_titles if title_substring in title]
			if(len(matching_titles)>1):
				print('同花顺软件多个标题窗口，关闭多余的')
				return
			elif(len(matching_titles)==0):#
				print('同花顺软件打开有问题')
				return

		# 最大化找到的窗口
		window = gw.getWindowsWithTitle(matching_titles[0])
		if window:
		    window[0].maximize()
		    window[0].activate()
		time.sleep(1)
		# 获取屏幕的宽度和高度
		screen_width, screen_height = pyautogui.size()
		# 计算屏幕中央的坐标
		center_x, center_y = screen_width // 2, 10
		# 将鼠标移动到屏幕中央
		pyautogui.moveTo(center_x, center_y, duration=1) 
		time.sleep(1)
		# 模拟鼠标左击一下,确定激活同花顺软件
		pyautogui.click()
		# 等待一段时间，确保点击事件生效
		time.sleep(1)
		# 模拟键盘输入字符
		pyautogui.typewrite("000001")
		time.sleep(1)
		pyautogui.press('down')#选择上证指数000001
		time.sleep(1)
		# 如果需要按 Enter 键确认输入，可以添加以下行
		pyautogui.press('enter')
		time.sleep(1)
		pyautogui.moveTo(10, 300, duration=1) 
		time.sleep(1)
		# 模拟鼠标左击一下,确定打开日k图
		pyautogui.click()
		time.sleep(1)
		pyautogui.moveTo(screen_width*0.95, screen_height/2-100, duration=1) 
		time.sleep(1)
		for _ in range(23):#鼠标光标移动最有K线
			pyautogui.press('right')
		time.sleep(1)
		
		#计算一个k线多少像素
		offset_K=6

		current_mouse_x1,current_mouse_y1=pyautogui.position()


		pyautogui.moveTo(current_mouse_x1-offset_K*offset, current_mouse_y1, duration=1)  #移动到目标K线
		time.sleep(1)
		pyautogui.click(clicks=2)#打开历史分时图
		time.sleep(1)
		#验证已经打开
		all_titles = gw.getAllTitles()
		# 查找包含特定字符串的窗口标题
		matching_titles = [title for title in all_titles if '上证指数(000001)' in title]
		if(len(matching_titles)>1):
			print('同花顺软件多个标题窗口，关闭多余的')
			print(matching_titles)
			return
		elif(len(matching_titles)==0):#
			print('同花顺软件打开有问题')
			return

		temp_tradeday=tradeday[:4]+'-'+tradeday[4:6]+'-'+tradeday[6:8]
		if( temp_tradeday in  matching_titles[0]):#打开日期对的
			pass
		else:
			print('打开窗口： ',matching_titles[0],'期望： ',tradeday)
			print('调试参数 offset')


		window = gw.getWindowsWithTitle(matching_titles[0])
		if window:
			window = window[0]
			# Bring the window to the foreground
			window.activate()
			# Wait for a short moment to ensure the window is active
			time.sleep(0.5)
			x, y, _, _ = window.left, window.top, window.width, window.height
			window.left=screen_width/4
			window.top=screen_height/4
			time.sleep(2)
			#x, y = pyautogui.position()
			print(f"窗口 '{matching_titles[0]}' 坐标位置: ({x}, {y})")
			pyautogui.moveTo( window.left+window.width*0.2,window.top+window.height/2, duration=1) 
			time.sleep(1)
			pyautogui.click()
			time.sleep(1)
			for _ in range(50):#鼠标光标移动到9:30，涨跌家数位置
				pyautogui.press('left')	
			time.sleep(1)

		else:
			print(f"Window '{matching_titles[0]}' not found.")



	def 查看图片感兴趣区域坐标(self,pic_path):
		#拖拽鼠标，然后空格确认
		# 加载图像
		image = cv2.imread(pic_path)
		if image is   None :
			print(pic_path,'error')
			return
		# 显示图像
		cv2.imshow("Image", image)
		# 在图像上选择感兴趣的区域（按下键盘上的'c'键来确认选择）
		rect_box = cv2.selectROI("Image", image, fromCenter=False, showCrosshair=True)
		cv2.destroyAllWindows()
		# 输出感兴趣区域的坐标
		x_start, y_start, width, height = rect_box
		x_end = x_start + width
		y_end = y_start + height
		print(f"x_start: {x_start}, y_start: {y_start}, x_end: {x_end}, y_end: {y_end}")

	def get_pics_ths(self,offset,tradeday):

		#y由于没有找到一个网站能提供一天的上涨家数曲线，所以没法爬取，只能通过特殊方式获取了！
		#这里是通过同花顺软件，上证指数分时界面中的指标“沪深涨跌”，然后爬取4*60张图片来获取这个分钟数据，好夸张方式
		
		# 设置开始时间和结束时间
		start_time = datetime.strptime("09:30", "%H:%M")
		end_time = datetime.strptime("15:00", "%H:%M")
		# 初始化当前时间为开始时间
		current_time = start_time
		# 时间间隔为1分钟
		time_interval = timedelta(minutes=1)
		# 存储结果的数组
		time_strings = []
		# 生成时间字符串数组
		while current_time <= end_time:
		    time_strings.append(current_time.strftime("%H%M"))
		    current_time += time_interval
		time_strings=time_strings[:121]+time_strings[210:]#去掉中午休息
		#print(time_strings)


		self.打开同花顺定位界面(offset=offset,tradeday=tradeday)


		folder_path='.\\temp\\temp2'#解析图片库，不能中文，
		# 清空文件夹
		shutil.rmtree(folder_path)
		# 重新创建空文件夹
		os.makedirs(folder_path)

		#确认感兴趣坐标区域，缩小识别信息区域范围，例如定位股价信息的区域
		x_start=573
		y_start=310
		x_end=786
		y_end=334
		#self.查看图片感兴趣区域坐标(pic_path='./temp/temp2/0930_shot.png')#手动修改，不用每次都获取，这里一次写死就好了
		print(f"感兴趣区域坐标  x_start: {x_start}, y_start: {y_start}, x_end: {x_end}, y_end: {y_end}")
		#开始截屏，快速截完，防止画面有变化，后面在集中处理数据提取
		for timestamp in time_strings:
			#print(timestamp)
			pic_path=folder_path+'\\{}_shot.png'.format(timestamp)#png是无损格式，jpg是有损，所以选择png格式
			#print(pic_path)
			screenshot = ImageGrab.grab()
			screenshot.save(pic_path)

			# 转换为 OpenCV 格式
			screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
			# 截取感兴趣的区域
			roi = screenshot_cv[y_start:y_end, x_start:x_end]
			# 保存感兴趣区域为图像文件
			cv2.imwrite(folder_path+'\\{}.png'.format(timestamp), roi)

			#时间图片也可以切片判断和timestamp一致，这里先不弄了以后有问题再说！

			while  not os.path.exists(pic_path) :
				time.sleep(1)
			
			pyautogui.press('right')#选择下一min，上涨家数展示

	def pretreatment_pic(self,pic_path='./temp/temp1/0930.png'):
		# 为了更好提取信息，必须的处理截图和亮度灰度等调整， 根据你的需求调整参数或预处理图像，以提高 OCR 的准确性。
		
		image = cv2.imread(pic_path)
		if image is   None :
			print(pic_path,' error 图片空')
			return
		# 将图像转为灰度图
		gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# 保存处理后的图像
		pic_path=pic_path[:-4]+'_gray'+pic_path[-4:]
		#print(pic_path)
		cv2.imwrite(pic_path, gray_image)
		return pic_path



	def analysis_pic_Tesseract(self): #EasyOCR 的优势之一是对于多语言和多字体的支持较好。它支持多种语言，并且可以在处理包含多种字体、风格和大小的文本时表现得相对灵活。
							#适用场景： 适用于需要处理多语言、多种字体的文本的场景，例如处理混合文字和数字的图像。
		
		#放弃了需要安装exe，Tesseract算了
		pass

	def analysis_pic_EasyOCR(self,pic_path='./temp/temp1/0930.png'):#优势： Tesseract 是一个成熟的 OCR 引擎，对于清晰、标准字体的文本有很好的表现。它在处理大规模文档和单一语言文本时通常表现良好。
							#适用场景： 适用于处理大量的标准化文本，例如扫描文档、标准字体的图像等。
		df = ak.stock_zh_a_spot_em()
		maxnum=len(df)

		#图片信息提取
		image = cv2.imread(pic_path)
		# 选择要使用的语言模型，例如 'ch_sim' 表示简体中文，支持多种语言和字体
		reader = easyocr.Reader(['ch_sim', 'en'])
		# 使用 EasyOCR 识别文本
		result = reader.readtext(image)
		#print(len(result))
		# 打印提取到的文本信息
		# for detection in result:
		# 	print(result)
		txt=result[0][1]

		#print(txt)
		#为了简化正则，去掉空格和：
		txt=re.sub(r'[-:.。 ]', '', txt)
		txt=txt.replace('!','').replace('I','').replace('O','0').replace('G','6').replace('T','7')

		text=txt
		#print(text)
		failnum=''
		raisenum=''
		match = re.search(r'F(\d+)U(\d+)', txt) #取的是F和U之后的数字
		if(match):#FU在txt中
			number1 = match.group(1)
			number2 = match.group(2)
			print(number1,number2)
			if(int(number1)+int(number2) <=maxnum):#解读是正确的 # 户朵张趺F2143U1799
				failnum=number1
				raisenum=number2
			elif(len(number1)==5 and len(number2)==4):#户罕张趺F42501U6931
				if( number1[-1]=='1'  and int(number2)>maxnum and ( number2[-1]=='1' or number2[-1]=='7')):
					failnum=number1[:-1]
					raisenum=number2[:-1]
				elif( number1[-1]=='1'  and ( number2[-1]=='1' or number2[-1]=='7')):#int(number2)>maxnum 
					failnum=number1[:-1]#户朵张趺F44241U5511
					raisenum=number2
					if( int(failnum)+  int(raisenum) > maxnum):
						raisenum=number2[:-1]

			elif(len(number1)==5 and len(number2)==5):#户朵张趺F32991U14327   
				if(number1[-1]=='1' and (number2[-1]=='7' or number2[-1]=='1') ):
					failnum=number1[:-1]
					raisenum=number2[:-1]	
				elif(number1[-1]=='1' and number2[0]=='4'):#户朵张趺F36381U41116
					failnum=number1[:-1]
					raisenum=number2[1:]
			elif(len(number1)==5 and len(number2)==3):#户罕张趺F42501U6931
				if( number1[-1]=='1'  ):
					failnum=number1[:-1]
					raisenum=number2

			elif(len(number1)==4 and len(number2)==4):#户罕张趺F42501U6931
				if( number2[-1]=='1' and int(number2)>maxnum ):
					failnum=number1
					raisenum=number2[:-1]
				#else:#户朵张趺F36381U41116

			#else:  
				# temp1=int(number1[1:])+int(number2[1:])
				# temp2=int(number1[1:])+int(number2[:-1])
				# temp3=int(number1[:-1])+int(number2[1:])
				# temp4=int(number1[:-1])+int(number2[:-1])
				# temp=[temp1,temp2,temp3,temp4]
				# ttemp=[  [number1[1:] ,number2[1:]] ,[number1[1:],number2[:-1]] ,  [number1[:-1],number2[1:]],[ number1[:-1],number2[:-1] ] ]   
				# ttrp=[  i for i in range(4)  if temp[i] <=maxnum]
				# if(len(ttrp)==1):
				# 	number1=ttemp[ttrp[0]][0]
				# 	number2=ttemp[ttrp[0]][1]
				# elif(len(ttrp)==2):#[['7461', '691'], ['7461', '969'], ['3746', '691'], ['3746', '969']]
				# 	#['3746', '691'], ['3746', '969']#不好区分
				# 	#print(ttemp)
				# 	#print(text)
				# 	#print("NO No match found.添加新样式代码，提取信息")
				# 	#return#这里看看看将就一下行不行，
				# 	number1=number1[:-1]
				# 	number2=number2[:-1]
				# 	pass
				# else:
				# 	print(ttemp)
				# 	print(text)
				# 	print("No match found.添加新样式代码，提取信息")
				# 	return

		elif('F' in txt and 'U' not in txt):#户朵张趺F34981012721
			txt=txt.split('F')[1]
			if txt.isdigit() and len(txt)==11 and txt[4]=='1' and txt[5]=='0' and txt[-1]=='1' :#字符串是数字构成,#户朵张趺F34981012721
				failnum=txt[:4]
				raisenum=txt[6:-1]
			elif txt.isdigit() and len(txt)==12 and txt[4]=='1' and txt[5]=='0' and txt[6]=='4' and txt[-1]=='1' :
				#户朵张趺F366310411911
				failnum=txt[:4]
				raisenum=txt[7:-1]
			elif txt.isdigit() and len(txt)==11 and txt[4]=='1' and txt[5]=='0'  and txt[-1]=='7' :#户朵张趺F33281014847
				failnum=txt[:4]
				raisenum=txt[6:-1]
			elif txt.isdigit() and len(txt)==10 and txt[4]=='1' and txt[5]=='0'  and txt[-1]=='1' :#户朵张趺F33281014847
				failnum=txt[:4]
				raisenum=txt[6:-1]
			else:
				print(text)
				print("No match found.添加新样式代码，提取信息")
				return

		else:
			print(text)
			print("No match found.添加新样式代码，提取信息")
			return
		

		print("raisenum :", raisenum)
		print("failnum :", failnum)



		return {"上涨数量":raisenum,"下跌数量":failnum }



	def get_days_上证指数黄白线分钟数据_exe(self,start,end):
		#这个接口不要在其他地方调用，而是作为集中更新数据的函数，用，不要作为基础功能调用



		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\上证指数黄白线分钟数据_无序.json')
		data_file_path_有序=os.path.join(script_file_path,'data\\上证指数黄白线分钟数据_有序.json')
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
			temp=self.__get_today_每日上证指数黄白线分钟数据_ths_exe(tradeday=day)
			if(temp is not None):
				file_content[day]=temp

		#无序,如果需要顺序，需要按照交易日重新再梳理一遍后保存到数组中，[{20230101,dt1},{20230102,dt2},{20230103,dt3}]	
		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(file_content, json_file)
		#有序
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
		
		# #选出设定日期，返回有序
		start_index = 有序alldays.index(start)
		end_index = 有序alldays.index(end)
		return result[start_index:end_index+1]











if __name__ == '__main__':
	
	a=上证指数黄白线分钟数据类()
	out=a.get_day_上证指数黄白线分钟数据(tradeday='20240111')
	print("data:   ",out)
	#b=a.get_days_上证指数黄白线分钟数据_exe(start='20231201',end='20231214')
	#print(b)
	#a.打开同花顺定位界面()
	#a.get_pics_ths()

	#这里思路变化是，图片爬取太麻烦，单独一个接口调用，统一来做，不在get中主动爬取，而是集中图片exe方式！！！
	#所以写一个集中爬取的接口就好了