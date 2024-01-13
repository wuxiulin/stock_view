import os
import json
import configparser

class 数据保存类():

	def __init__(self,GlobalCfg=None):

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
		
		

	def save_to_json(self,data,file_path):
		if(data is None):
			print('data is None ,donot save to {}'.format(file_path))
			return 
		folder_path = os.path.dirname(file_path)
		if(folder_path =='' or folder_path is None):
			folder_path=self.current_dir 
			file_path=os.path.join(folder_path,file_path)
		os.makedirs(folder_path, exist_ok=True) #确保路径存在

		#无论是否存在这里都是覆盖的。
		with open(file_path, 'w+',encoding='utf-8') as json_file:
			json.dump(data, json_file)


	def save_to_csv(self,data,file_path):
		pass

	def map_savepath(self):
		if map_type==1:#保存在默认文件夹，filename名字
			#设置默认保存路径
			if(file_path=='' or file_path is None ):
				file_path=os.path.join(self.current_dir,filename)
		elif map_type==2:
			pass
		else:
			pass

		return file_path

	
#测试在上一级，测试不用在这里