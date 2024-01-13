import sys
import os
import configparser
from datetime import datetime ,timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)) )


from  数据保存.数据保存 import 数据保存类
from  数据爬取 import 同花顺领先指数1c0002    

class test( ):
	def __init__(self, GlobalCfg =None):

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
		self.conf_local.read(self.cfgpath_local, encoding='utf-8')


	def test(self):
		temp类=同花顺领先指数1c0002.同花顺领先指数1c0002类()
		data=temp类.crawl_同花顺领先指数1c0002_min()
		print(data)
		file_dir=self.conf_local.get('同花顺分时图截图_上证领先', '数据保存路径')
		#print(type(file_dir))
		file_path=os.path.join(file_dir,'{}.json'.format(list(data.keys())[0]))
		#print(file_path)
		数据保存类().save_to_json(data=data,file_path=file_path)
		








if __name__ == '__main__':
	test().test()
	pass






