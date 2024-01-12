import sys
import os
import configparser



from 数据爬取.同花顺领先指数1c0002 import 同花顺领先指数1c0002类

from  数据保存.数据保存 import 数据保存类


class test( ):
	def __init__(self,  ):
		self.current_dir = os.path.dirname(os.path.abspath(__file__)) 
		#配置文件init
		self.cfgpath= os.path.join(self.current_dir,'配置文件.cfg')#当前文件配置文件
        # 读取配置文件，最新更新日期，不要重复爬取
		self.conf = configparser.ConfigParser()
		os.makedirs(self.current_dir, exist_ok=True)  # 创建文件夹，如果存在则不报错
		if not os.path.exists(self.cfgpath):
			# 如果配置文件不存在，创建一个空的配置文件
			with open(self.cfgpath, 'w'):
				pass
		self.conf.read(self.cfgpath, encoding='utf-8')

	def test(self):
		data=同花顺领先指数1c0002类().crawl_同花顺领先指数1c0002_min()
		file_dir=self.conf.get('保存路径', '1c0002_min')
		#print(type(file_dir))
		file_path=os.path.join(file_dir,'{}.json'.format(list(data.keys())[0]))
		#print(file_path)
		数据保存类().save_to_json(data=data,file_path=file_path)
		





if __name__ == '__main__':
	test().test()






