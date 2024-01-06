#pip install Jinja2
#四个js文件，是highechart的
#生成template ，创建一个 Jinja2 模板文件（比如 template.html） 


#创建一个 Python 脚本，使用 Jinja2 渲染模板并将动态数据传递给模板：
import webbrowser
from jinja2 import Template
from datetime import datetime
# 准备数据，这里使用一个简单的列表作为示例
#dynamic_data = [1, 2, 3, 4, 5]
import sys
import os
def get_chart(dynamic_data,name):

	#运行这个 Python 脚本，它将生成一个 HTML 文件（比如 output.html），其中包含动态数据的 JavaScript 代码。打开这个 HTML 文件，
	#你应该能够看到 Highcharts 图表，其中的曲线数据是你在 Python 中指定的动态数据。
	# 读取模板文件
	with open('../templates/template.html', 'r', encoding='utf-8') as template_file:
	    template_content = template_file.read()

	# 创建 Jinja2 模板对象
	template = Template(template_content)

	# 使用模板渲染 HTML，传递动态数据
	#在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
	#模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
	#html_output = template.render(data=dynamic_data)
	html_output = template.render(data=dynamic_data )
	# 将生成的 HTML 写入文件
	output_file_path='../index.html'
	with open(output_file_path, 'w', encoding='utf-8') as output_file:
	    output_file.write(html_output)

	# 用默认浏览器打开生成的 HTML 文件
	webbrowser.open(os.path.abspath( output_file_path))#用output_file_path  有问题



if __name__ == '__main__':


	current_dir = os.path.dirname(os.path.abspath(__file__))
	parent_dir = os.path.dirname(os.path.dirname(current_dir))
	print(current_dir)
	sys.path.append(parent_dir)


	#******************获取数据*****************************************************************************
	#******************获取数据***********************
	#******************获取数据***********************
	from 爬取数据有关证券涨停的.获取数据模版1 import get_days_wencai
	#数据保存在这个目录下，因为他用，不是库函数位置
	a=get_days_wencai(start='20230101',end='20231125',txt="涨停,证券板块",infile='../data/数据1.json')
	#输出结果格式如下
	# {
	#     'date': ['2020-07-03', '2020-07-06', '2020-07-07', '2020-07-08', '2020-07-09', '2020-07-10'],

	#     'line': {	0: [14, 23, 3, 8, 4, 3], 1: [5, 10, 0, 6, 1, 2], 2: [8, 5, 0, 0, 1, 1],
	# 		 	3: [1, 7, 1, 0, 0, 0], 4: [0, 1, 1, 1, 0, 0], 5: [0, 0, 1, 0, 1, 0], 6: [0, 0, 0, 1, 0, 0], 
	#  			7: [0, 0, 0, 0, 1, 0], 8: [0, 0, 0, 0, 0, 0]}, 

	#     'result': {'2020-07-03': {0: 14, 1: 5, 2: 8, 3: 1, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0},
	# 			 '2020-07-06': {0: 23, 1: 10, 2: 5, 3: 7, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0},
	# 			 '2020-07-07': {0: 3, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 0, 7: 0, 8: 0}, 
	# 			'2020-07-08': {0: 8, 1: 6, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 0}, 
	# 			'2020-07-09': {0: 4, 1: 1, 2: 1, 3: 0, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0},
	# 			 '2020-07-10': {0: 3, 1: 2, 2: 1, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
	# 			 }
	# }

	#*************************重构数据***********************
	#*************************重构数据***********************
	#*************************重构数据***********************

	#https://data.jianshukeji.com/stock/history/000001
	#   [时间戳         ,收盘价,xx价格，xx，xx x ,成交额  ]
	# [	[1416182400000,7.204,7.232,7.037,7.072,889594.5],
	# 	[1416268800000,7.058,7.107,6.933,6.968,930296.44],
	# ]
	dydata={}
	for key in range(9):
		out=[]
		for i in range(len(a['date'])):

			# print('****************************************')
			day=a['date'][i]
			# print(day,i)
			# print('****************************************')
			timestamp =(datetime.strptime(day, "%Y-%m-%d")).timestamp()*1000#转为linux时间
			try:
				out.append([timestamp,a['line'][str(key)][i]])
			except Exception as e:
				print(a['line'])
				print(a['line'][str(key)])
				print(e)
	
		dydata[str(key)+"板"]=out
	print(dydata)#依照模板重构的数据



	#*************************html可视化图表数据***********************
	#*************************html可视化图表数据***********************
	#*************************html可视化图表数据***********************

	get_chart(dydata,"证券")
	#print(a)

	 