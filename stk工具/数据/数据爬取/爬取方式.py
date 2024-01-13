import requests
import time
import configparser
import os
from crawl同花顺exe分时数据  import crawl同花顺exe分时数据类

class 爬取方式类( ):
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


	def crawl_by_requests_get(self,url, headers):
		'''
		1、注意精选url。不同url获取类似数据，但是难度相差很大，反爬力度等不一样
		2、这种方式突然不能用，看url打开网址是否可以，其次检查headers
		'''
		crlnum=0
		while True:
			# 发起GET请求
			response = requests.get(url, headers=headers)
			#print(response.status_code)
			# 检查响应状态码
			if response.status_code == 200:
			    # 输出网页内容
				content=response.text
				#print(content)
			    #print(type(content))
				return content
			else:
				crlnum=crlnum+1
				if(crlnum>20):
					print(f"Failed to retrieve content. Status code: {response.status_code}")
					return None
				time.sleep(5)
				continue



	def get_today_上证指数黄白线分钟数据_wencai_js(self):
 
		pass


		#关闭浏览器


	def crawl_by_action_records(self,filename_act_recd):
		'''
		通过某个软件或者手动模拟，记录操作某个软件步骤，就是键盘和鼠标动作，然后截图，然后图片识别，解析数据，保存数据，重复这个过程，直到保存完整数据
		'''	
		pass

		#比较简单重复的可以用这个，但是稍微复杂需要配合的，这里可能没有那么容易实现，所以需要定制化，
		#目前遇到的，没有那么复杂，所以定制化，也没有机会，以后再说提炼抽象的问题!，
		pass

	def crawl_by_action_records_同花顺_exe_分钟数据(self,cfgset):
		#self.conf.get('同花顺分时图截图_上证领先', '1c0002_min')

		'''
		同花顺上类似分时图获取数据都是类似操作，需要微调
		通过模拟通过同花顺获取数据步骤，用py模拟，然后截图，然后解析图片获取数据，保存，然后重复步骤获取全部数据。
		这种方式获取历史数据，建议是集中统一时间获取，然后手动复查数据，清洗数据。保证数据正确之后，再被使用
		'''
		#没有其他数据源，无法通过其他方式获取太多历史数据，只能通过这种方式获取历史数据，比较原始和笨重方式，比手动记录强一点
		#单独一个文件。py,简化这里代码

		#1、确定需要截取图片的坐标,调用函数：查看图片感兴趣区域坐标(pic_path)
		#调试定位界面，需要手动修改参数步骤，但是类似的界面，应该是一样的
		

		temp类=crawl同花顺exe分时数据类(GlobalCfg=self.conf)

		temp类.打开同花顺定位界面(cfgset=cfgset)

		#截屏图片
		out=temp类.get_pics_ths()
		
		#temp类.查看图片感兴趣区域坐标(pic_path=os.path.join(out,'0930_shot.png'))#手动修改，不用每次都获取，这里一次写死就好了
		#return
		if(out is None):
			return None

		#截取特定图片、处理图片、解析图片
		data=temp类.解析图片(cfgset=cfgset)
		return data
		
		pass
