#目的为了获取花顺领先指数1c0002的数据
#确定数据源和数据爬取方式，
#手动切换不同数据源和爬取方式，不要自动切换，


#同花顺的指数代码，
#通过000001上证指数这里看到黄线跟1c0002上证领先数据还是不一致，差一点，影响不是很大。
import json
import inspect
import configparser
from datetime import datetime,timedelta

import os,sys
import akshare as ak

sys.path.append( os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ))
sys.path.append( os.path.dirname(os.path.abspath(__file__)) )


from  数据保存.数据保存 import 数据保存类
from  爬取方式 import 爬取方式类#不要在这个文件使用这个表达方式，从其他文件调用目录结结构问题，

class 同花顺领先指数1c0002类( ):
	"""docstring for ClassName"""
	def __init__(self,GlobalCfg =None):
		self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
		self.conf = GlobalCfg

		self.cfgpath_local= os.path.join( self.current_dir , '配置文件.cfg')
		print(self.cfgpath_local)
		if not os.path.exists(self.cfgpath_local):
    		# 如果配置文件不存在，创建一个空的配置文件
			with open(self.cfgpath_local, 'w'):
				pass
			print('配置文件没有配置')
			return
    	# 读取配置文件，最新更新日期，不要重复爬取
		self.conf_local = configparser.ConfigParser()
		self.conf_local.read(self.cfgpath_local, encoding='utf-8')

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

	def crawl_同花顺领先指数1c0002_min_by_同花顺exe(self,cfgset):
		start_day=self.conf_local.get(cfgset, 'start_day')#设置开始爬取日期
		end_day=self.conf_local.get(cfgset, 'end_day')#设置结束日期
		if(end_day == ''):
			end_day=datetime.now().strftime("%Y%m%d")
		since_day=self.conf_local.get(cfgset, 'since_day')#上一次爬取时间
		if(since_day == ''):
			since_day='19910809'

		if since_day < start_day:#计算比较设置值和上次爬取时间明确需要爬取确切时间，不重复爬取
			pass
		elif since_day < end_day:
			start_day=since_day
		else:
			print('更新完成')
			return

		trade_df = ak.tool_trade_date_hist_sina()#正序列表 
		trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
		#加快寻找时间，虽小时间范围，
		days=(datetime.strptime(str(datetime.now().year)+'1231', "%Y%m%d")-datetime.strptime(start_day, "%Y%m%d")).days
		trade_df=trade_df[-days:]#快速缩小范围
		#print(trade_df)
		while True:               #调整时间为真实最近交易日
			if(start_day not in trade_df):
				start_day=(datetime.strptime(start_day,'%Y%m%d')+timedelta(days=1)).strftime('%Y%m%d')
			else:
				break		
		while True:#调整时间为真实最近交易日
			if(end_day not in trade_df):
				end_day=(datetime.strptime(end_day,'%Y%m%d')-timedelta(days=1)).strftime('%Y%m%d')
			else:
				break	

		#获取期间交易日list
		#print(start_day,end_day)
		startindex = trade_df.index(start_day)
		#print(startindex)
		endindex = trade_df.index(end_day)
		days=trade_df[startindex:endindex+1]
		#print(days)

		print('计算需要爬取日期{} - {}'.format(start_day,end_day))

		#获取最新交易日，计算offset
		today_str=datetime.now().strftime("%Y%m%d")
		last_day=today_str
		while True:               #调整时间为真实最近交易日
			if(last_day not in trade_df):
				#print(last_day)
				last_day=(datetime.strptime(last_day,'%Y%m%d')-timedelta(days=1)).strftime('%Y%m%d')
			else:
				break		
		if(today_str ==last_day):#今天是交易日
			tt1=datetime.now().strftime("%Y%m%d")< datetime.strptime(today_str+' 04:00:00','%Y%m%d %H:%M:%S')#一般执行很久，所以不要在快要开盘执行，所以充足时间
			tt2=datetime.now().strftime("%Y%m%d")> datetime.strptime(today_str+' 15:01:00','%Y%m%d %H:%M:%S')#一般执行很久，所以不要在快要开盘执行，所以充足时间
			if(not(tt1 or tt2)):
				print('没有足够更新时间，代码执行过程可能会出问题')
				return
			if(tt1): #交易日,没开市
				last_day=(datetime.strptime(last_day,'%Y%m%d')-timedelta(days=1)).strftime('%Y%m%d')#
		
		for day in days:
			print('开始爬取：',day)
			offset= (datetime.strptime(last_day,'%Y%m%d') - datetime.strptime(day,'%Y%m%d')).days
			self.conf_local.set(cfgset,'offset',str(offset))#调整offset

			self.conf_local.set(cfgset,'tradeday',str(day))#正在交易日设置
			data=爬取方式类(GlobalCfg=self.conf_local).crawl_by_action_records_同花顺_exe_分钟数据(cfgset=cfgset)

			data={day:data}
			file_dir=self.conf_local.get(cfgset, '数据保存路径')
			#print(file_dir)
			file_path=os.path.join(file_dir,'{}.json'.format(list(data.keys())[0]))
			#print(file_path)
			数据保存类(GlobalCfg=self.conf_local).save_to_json(data=data,file_path=file_path)

			#更新时间，防止中途停止，下一次重复爬取太多
			self.conf_local.set(cfgset,'since_day',str(day))
			with open(self.cfgpath_local, 'w',encoding='utf-8') as configfile:
				self.conf_local.write(configfile)
			

		
		






if __name__ == '__main__':
	#由于同花顺爬取方式，这种是在这个文件调试就好了不要在其他地方调用，
	#这里拿出大块时间来爬取，不能实时爬取，容易出错
	同花顺领先指数1c0002类().crawl_同花顺领先指数1c0002_min_by_同花顺exe(cfgset='同花顺分时图截图_上证领先')
