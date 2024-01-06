import sys,os
import pywencai
import json

class 股票代码映射类():
	"""docstring for 股票代码映射类"""
	def __init__(self):	
		pass

	def get_股票代码映射(self):
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\股票代码映射.json')
		result={}
		with open(data_file_path, 'r',encoding='utf-8') as json_file:
			result=json.load(json_file)
		return result

	def get_股票代码映射_flag(self,flag):
		result=self.get_股票代码映射()
		return result[flag]

	
	def update_股票代码映射(self):
		#数据保存文件路径
		script_file_path=os.path.abspath(os.path.dirname(__file__))#当下这个代码文件路径
		data_file_path=os.path.join(script_file_path,'data\\股票代码映射.json')
		#print(data_file_path)


		searchtxt='个股涨跌幅'
		try:
			res = pywencai.get(query=searchtxt,loop=True,query_type='stock')#测试'
		except Exception as e:
			print(e,"__get_day_每日下跌数_wencai_1   is error ") 
			return None
		if(res is None or len(res)==0):
			print(e,"__get_day_每日下跌数_wencai_1   is  none ") 
			return  None
		
		#print(res)

		a = {i: [j, k] for i, j, k in zip(res['股票代码'], res['股票简称'], res['code'])}
		b = {j: [i, k] for i, j, k in zip(res['股票代码'], res['股票简称'], res['code'])}
		c = {k: [i, j] for i, j, k in zip(res['股票代码'], res['股票简称'], res['code'])}

		a.update(b)
		a.update(c)

		with open(data_file_path, 'w',encoding='utf-8') as json_file:
			json.dump(a, json_file)

		return a


	def update_股票代码映射_flag(self,flag):
 		result=self.update_股票代码映射()
 		return result[flag]


if __name__ == '__main__':
	股票代码映射类().get_票代码映射()

