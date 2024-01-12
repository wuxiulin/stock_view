#目的为了获取花顺领先指数1c0002的数据
#确定数据源和数据爬取方式，
#手动切换不同数据源和爬取方式，不要自动切换，


#同花顺的指数代码，
#通过000001上证指数这里看到黄线跟1c0002上证领先数据还是不一致，差一点，影响不是很大。
import json
import inspect
import configparser
from datetime import datetime,timedelta
from  .爬取方式 import 爬取方式类#不要在这个文件使用这个表达方式，从其他文件调用目录结结构问题，
import os

class 同花顺领先指数1c0002类( ):
	"""docstring for ClassName"""
	def __init__(self):
		self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
		self.cfgpath= os.path.join( self.current_dir , 'crawl.cfg')
		
	def read_cfg(self):
		os.makedirs(self.current_dir, exist_ok=True)  # 创建文件夹，如果存在则不报错
		if not os.path.exists(self.cfgpath):
            # 如果配置文件不存在，创建一个空的配置文件
			with open(self.cfgpath, 'w'):
				pass
        # 读取配置文件，最新更新日期，不要重复爬取
		self.conf = configparser.ConfigParser()
		self.conf.read(self.cfgpath, encoding='utf-8')


	def crawl_同花顺领先指数1c0002_min(self):
		'''这里是个统一接口，不同爬取方式，手动接切换，
		'''
		#爬取时间配置避免反复爬取
		# if '1c0002' in self.conf and 'min_since_date' in self.conf['1c0002']:
		# 	since_date=self.conf.get('1c0002', 'min_since_date')#上一次爬取数据时候得到的当时交易日时间，不是执行代码时间
		# else:
		# 	since_date='19910809'

		#由于这个接口周六周日执行爬取周五数据，或者其他情况，判断复杂，且这里爬取没有多少内容所以重复爬取没有关系
		#所以不参考配置文件内容了
		return self.crawl_同花顺领先指数1c0002_min_by_requests_get()
		


	def crawl_同花顺领先指数1c0002_min_by_requests_get(self):
		'''
			获取当下最近一个交易日的数据，无法获取历史数据，所以没有day或者tradeday设置
			盘中执行，获取部分当天数据；盘前执行，要看当下时刻，网站数据是未更新还是昨日数据，还是已经清空昨日而今日未开盘为空
			替换utrl，注意header替换，其次旧代码注释掉，不要删除，也没有必要重写新函数。可以用if 0 方式注意也是可以。
		'''
		# 构造请求头部信息
		headers = {
		    'Accept': '*/*',
		    'Accept-Encoding': 'gzip, deflate, br',
		    'Accept-Language': 'zh-CN,zh;q=0.9',
		    'Cache-Control': 'no-cache',
		    'Connection': 'keep-alive',
		    'Cookie': '__utmz=156575163.1702529122.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=156575163.1697276506.1702529122.1702529122.1703600460.2; Hm_lvt_722143063e4892925903024537075d0d=1702871348,1702994719,1703071880,1703600485; Hm_lvt_929f8b362150b1f77b477230541dbbc2=1702871349,1702994720,1703071880,1703600485; historystock=1A0001%7C*%7C300033%7C*%7C833284%7C*%7C833249; user=MDp6ZXJvYVA6Ok5vbmU6NTAwOjM0MDQzODUwMzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNDo6OjMzMDQzODUwMzoxNzA0MDMwMzYzOjo6MTQ2MDEyMTg0MDo2MDQ4MDA6MDoxMmI4M2ExYmJmMmY1OWEwYWQ3MWViN2ZjMzE4Yzg5YWM6ZGVmYXVsdF80OjE%3D; userid=330438503; u_name=zeroaP; escapename=zeroaP; ticket=3611331482ac2603c6acaf7278271e66; user_status=0; utk=4d2406a4155c1037c0d2f53322e61e0b; Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1=1703599022,1703966825,1704030361,1704415357; v=A0N3xx5DIjN3ve5H5xp2MtaE0gziuNf6EUwbLnUgn6IZNG3w_YhnSiEcq3iG',
		    'Host': 'd.10jqka.com.cn',
		    'Pragma': 'no-cache',
		    'Referer': 'https://m.10jqka.com.cn/stockpage/hs_1A0001/',
		    'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114"',
		    'Sec-Ch-Ua-Mobile': '?0',
		    'Sec-Ch-Ua-Platform': '"Windows"',
		    'Sec-Fetch-Dest': 'script',
		    'Sec-Fetch-Mode': 'no-cors',
		    'Sec-Fetch-Site': 'same-site',
		    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.289 Safari/537.36'
		}

		url='https://d.10jqka.com.cn/v6/time/hs_1A0001/last.js'
		
		#获取目标网页
		content=爬取方式类().crawl_by_requests_get(url=url,headers=headers)
		if(content is None):
			print('error from {}'.format(inspect.currentframe().f_code.co_name))
			return None
		#print(content)
		try:
			#定制化处理网页，找到目标数据，不同url，后面处理过程不一样，所以注意这里无法复用，都是特定网址特定处理。
			start_index = content.find('(')
			end_index = content.find(')')
			# 删除第一个括号及其以外的内容
			content = content[start_index + 1:end_index]
			res=json.loads(content)
			res=res['hs_1A0001']
			tradeday=res['date']
			#print(type(res['data']))
			#print(res['data'])
			#处理一下，格式化一下数据，
			time_periods = res['data'].split(';')
			formatted_data = [tuple(period.split(',')) for period in time_periods]
		except Exception as e:
			print(e)
			print('error 网页格式变化，处理有问题 from {}'.format(inspect.currentframe().f_code.co_name))
			return None 
		if len(formatted_data)<240:
			return None#数据不完整
		else:
			return {tradeday:formatted_data}


	def  gouza(self):
		#同花顺反爬，'hexin-v'时效是2min，就不能用，所以每次调用接口更新V就好了
		with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'aes.min.js'), 'r') as f:
			jscontent = f.read()
		context = execjs.compile(jscontent)#应该是加载功能函数意思或者回调，钩子？？
		url = 'http://d.10jqka.com.cn/v6/time/48_{}/last.js?hexin-v={}'.format(blk,context.call("v"))
		#构造需要v的url
		pass


		
