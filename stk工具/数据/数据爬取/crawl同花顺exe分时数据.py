import pyautogui
import pygetwindow as gw
import time
import os
from datetime import datetime,timedelta
import configparser
import shutil
from PIL import ImageGrab
import cv2
import numpy as np
import re
import easyocr
import subprocess

class crawl同花顺exe分时数据类( ):
	def __init__(self,GlobalCfg =None):
		self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
		self.conf = GlobalCfg

		self.cfgpath_local= os.path.join( self.current_dir , '配置文件.cfg')
		if not os.path.exists(self.cfgpath_local):
    		# 如果配置文件不存在，创建一个空的配置文件
			with open(self.cfgpath_local, 'w'):
				pass
			print('配置文件没有配置')
			return
    	# 读取配置文件，最新更新日期，不要重复爬取
		self.conf_local = configparser.ConfigParser()
		self.conf_local.read(self.conf_local, encoding='utf-8')
		self.offset_K=6
			


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
		print('配置内容： ',f"x_start: {x_start}, y_start: {y_start}, x_end: {x_end}, y_end: {y_end}")

	def print_mouse_index(self):
		while True:
			print(pyautogui.position())
			time.sleep(3)
	def 打开同花顺定位界面(self,cfgset):
		#chosenum :含义同一个代码多个选项，选第几个，输入中文有问题，输入法，所以这里只能输入数字，但是相同数字指数和股票代码需要默认是第几个
		#所以需要手动尝试，然后设置，可以写个配置文件
		
		#这里截图修改了代码，尽量简单，方便后面图片识别，所以这里 F  U  这里没有B股，其次是不包括涨幅为0的
		#这是值是沪深A，不包括北交所，所以注意，需要包括要改同花顺代码，以后再说吧
		code=self.conf.get(cfgset, 'code')
		offset = int(self.conf.get(cfgset, 'offset'))
		tradeday=self.conf.get(cfgset, 'tradeday')
		chosenum=int(self.conf.get(cfgset, 'chosenum'))

		title_substring="同花顺(v"
		# 获取当前所有窗口的标题
		all_titles = gw.getAllTitles()
		# 查找包含特定字符串的窗口标题
		matching_titles = [title for title in all_titles if title_substring in title]
		if(len(matching_titles)>1):
			for title in matching_titles :
				print(title)
			print('同花顺软件多个标题窗口，手动关闭多余窗口')
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
		pyautogui.typewrite(code)
		time.sleep(1)
		for _ in range(chosenum-1):
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
		pyindex=473#让鼠标这个y值，日k图不会点击到均线
		pyautogui.moveTo(screen_width*0.95, pyindex, duration=1) 
		#self.print_mouse_index() #pyindex如果不合适，这里微调，打开注释执行代码，设置pyindex
		#return
		time.sleep(1)
		for _ in range(23):#鼠标光标移动最右K线
			pyautogui.press('right')
		time.sleep(1)
		
		current_mouse_x1,current_mouse_y1=pyautogui.position()#获取当下鼠标位置，日k最右边
		pyautogui.moveTo(current_mouse_x1-self.offset_K*offset, current_mouse_y1, duration=1)  #移动到目标K线
		time.sleep(3)
		pyautogui.click(clicks=2)#打开历史分时图
		time.sleep(2)
		
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
			print('error 打开窗口： ',matching_titles[0],'期望： ',tradeday,'调试参数 offset 参数')
			return
		print('打开分时窗口成功')
		window = gw.getWindowsWithTitle(matching_titles[0])
		if window:

			while True:
				window = window[0]
				# Bring the window to the foreground
				window.activate()
				# Wait for a short moment to ensure the window is active
				time.sleep(2)
				x, y, _, _ = window.left, window.top, window.width, window.height
				print(x,y)
				setx=1051 
				sety=531
				window.left=setx#移动窗口位置
				window.top=sety
				time.sleep(2)#d等生效
				print("当前窗口位置：", window.left, window.top)
				if(window.left == setx and window.top==sety ):#设置没有生效
					break

			#x, y = pyautogui.position()
			
			pyautogui.moveTo( 1167,760, duration=1) 
			time.sleep(3)
			pyautogui.click()
			time.sleep(1)
			pyautogui.click()
			time.sleep(1)
			for _ in range(50):#鼠标光标移动到9:30，涨跌家数位置
				pyautogui.press('left')	
			time.sleep(1)

		else:
			print(f"Window '{matching_titles[0]}' not found.")



	def get_pics_ths(self):
		folder_path=self.conf.get('同花顺分时图截图_上证领先', '截屏图片路径')
		pattern =re.compile('[\u4e00-\u9fa5]')
		if bool(pattern.search(folder_path)):
			print('error 路径中有中文，推荐 ./temp/temp1')
			return None

		#确认感兴趣坐标区域，缩小识别信息区域范围，例如定位股价信息的区域
		坐标=eval(self.conf.get('同花顺分时图截图_上证领先', '坐标'))
		x_start=坐标[0]
		y_start=坐标[1]
		x_end=坐标[2]
		y_end=坐标[3]
		
		
		print(f"数据区域坐标  x_start: {x_start}, y_start: {y_start}, x_end: {x_end}, y_end: {y_end}")
		#解析图片库，不能中文
		print('截取图片临时保存目录：',os.path.abspath(folder_path))#解析图片库，不能中文,不要随便改

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


		# 清空文件夹
		if(os.path.exists(folder_path)):
			shutil.rmtree(folder_path)
		# 重新创建空文件夹
		os.makedirs(folder_path)

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
		
 
		return  folder_path

	def pretreatment_pic(self,pic_path):
		# 为了更好提取信息，必须的处理截图和亮度灰度等调整， 根据你的需求调整参数或预处理图像，以提高 OCR 的准确性。
		#print(os.path.abspath(pic_path))
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

	def analysis_pic_EasyOCR_分时领先指数(self,pic_path):
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
		txt=re.sub(r'[,: ;]', '', txt)

		pattern = re.compile(r'^领先(\d{4}\.\d{2})最新(\d{4}\.\d{2})$')
		match=pattern.match(txt)


	
		if match:
			leading_value = match.group(1)
			latest_value = match.group(2)
			return {'领先':float(leading_value),'最新':float(latest_value)}
		
		pattern = re.compile(r'^领先(\d{4}\.\d{2})最新(\d{6})$')
		match=pattern.match(txt)
		if match:
			leading_value = match.group(1)
			latest_value = match.group(2)
			return {'领先':float(leading_value),'最新':float(latest_value)/100}

		pattern = re.compile(r'^领先(\d{6})最新(\d{4}\.\d{2})$')
		match=pattern.match(txt)
		if match:
			leading_value = match.group(1)
			latest_value = match.group(2)
			return {'领先':float(leading_value)/100,'最新':float(latest_value)}	
		
		pattern = re.compile(r'^领先(\d{6})最新(\d{6})$')
		match=pattern.match(txt)
		if match:
			leading_value = match.group(1)
			latest_value = match.group(2)
			return {'领先':float(leading_value)/100,'最新':float(latest_value)/100}	

		print('error 新模式 ',txt)


		pass
	def analysis_pic_EasyOCR_分时涨跌数(self,pic_path):
	#优势： Tesseract 是一个成熟的 OCR 引擎，对于清晰、标准字体的文本有很好的表现。它在处理大规模文档和单一语言文本时通常表现良好。
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


	def 解析图片(self,cfgset):
		pic_dir=self.conf.get(cfgset, '截屏图片路径')
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

		if cfgset == '同花顺分时图截图_分时涨跌数' :
			for timestamp in time_strings:
				#print(timestamp)
				#转灰度图
				temppath=os.path.join(pic_dir,'{}.png'.format(timestamp))
				#print(temppath)
				path_rename=self.pretreatment_pic(pic_path=temppath)
				#print(path_rename)
	 
				#解析
				data=self.analysis_pic_EasyOCR_分时涨跌数(pic_path=path_rename)
				#print(data)
				result[timestamp]=data
			print(result)
			print('**********************************************数据错误***********************************************************')
			for timestamp in time_strings:
				if(result[timestamp]["上涨数量"] ==''  or result[timestamp]["下跌数量"] =='' ):
					print(timestamp,'erro 检查修改代码')
					return None
			print('****************************************************************************************************************')

		elif cfgset == '同花顺分时图截图_上证领先' :
			for timestamp in time_strings:
				print(timestamp)
				#转灰度图
				temppath=os.path.join(pic_dir,'{}.png'.format(timestamp))
				#print(temppath)	
				path_rename=self.pretreatment_pic(pic_path=temppath)
				#print(path_rename)
				#解析
				data=self.analysis_pic_EasyOCR_分时领先指数(pic_path=path_rename)
				#print(data)
				#return
				result[timestamp]=data

			
			print('**********************************************数据错误***********************************************************')
			try:

				for timestamp in time_strings:
					print(timestamp)
					print(result[timestamp]["领先"],result[timestamp]["最新"])
				print('****************************************************************************************************************')
				pass
			except Exception as e:
				raise e
		else:
			pass

		print(result)
		return result




