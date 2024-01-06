

#pip install Jinja2
#四个js文件，是highechart的
#生成template ，创建一个 Jinja2 模板文件（比如 template.html） 




#创建一个 Python 脚本，使用 Jinja2 渲染模板并将动态数据传递给模板：
import webbrowser
from jinja2 import Template
from datetime import datetime
import sys
import os
# 准备数据，这里使用一个简单的列表作为示例
#dynamic_data = [1, 2, 3, 4, 5]
class HC可视化( ):
	"""docstring for ClassName"""
	def __init__(self ):
		pass
	

	def get_chart(self,dynamic_data,name,isopenweb=0):#默认股票，带时间那种图形

		# # 使用模板渲染 HTML，传递动态数据
		# #在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
		# #模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
		# #html_output = template.render(data=dynamic_data)
		# html_output = template.render(data=dynamic_data )

		#运行这个 Python 脚本，它将生成一个 HTML 文件（比如 output.html），其中包含动态数据的 JavaScript 代码。打开这个 HTML 文件，
		#你应该能够看到 Highcharts 图表，其中的曲线数据是你在 Python 中指定的动态数据。


	# 读取模板文件
		with open('template.html', 'r', encoding='utf-8') as template_file:
		    template_content = template_file.read()

		# 创建 Jinja2 模板对象
		template = Template(template_content)

		# 使用模板渲染 HTML，传递动态数据
		#在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
		#模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
		#html_output = template.render(data=dynamic_data)
		html_output = template.render(data=dynamic_data )
		# 将生成的 HTML 写入文件
		output_file_path='index.html'
		with open(output_file_path, 'w', encoding='utf-8') as output_file:
		    output_file.write(html_output)



		# 用默认浏览器打开生成的 HTML 文件
		if(isopenweb==1):
			webbrowser.open(output_file_path)

	def get_标注曲线(self,dynamic_data,labelxy天地板,labelxy地天板,name,isopen=0):#默认股票，带时间那种图形
		print(os.path.abspath(__file__))
		# # 使用模板渲染 HTML，传递动态数据
		# #在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
		# #模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
		# #html_output = template.render(data=dynamic_data)
		# html_output = template.render(data=dynamic_data )

		#运行这个 Python 脚本，它将生成一个 HTML 文件（比如 output.html），其中包含动态数据的 JavaScript 代码。打开这个 HTML 文件，
		#你应该能够看到 Highcharts 图表，其中的曲线数据是你在 Python 中指定的动态数据。


	# 读取模板文件
		with open(   os.path.join( os.path.dirname(os.path.abspath(__file__)),'模板_标注.html'), 
				'r', encoding='utf-8') as template_file:
		    template_content = template_file.read()

		# 创建 Jinja2 模板对象
		template = Template(template_content)


		# 使用模板渲染 HTML，传递动态数据
		#在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
		#模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
		#html_output = template.render(data=dynamic_data)
		html_output = template.render(data=dynamic_data ,labelxy天地板=labelxy天地板,labelxy地天板=labelxy地天板)
		# 将生成的 HTML 写入文件
		output_file_path= os.path.join( os.path.dirname(os.path.abspath(__file__)),'index.html')
		with open(output_file_path, 'w', encoding='utf-8') as output_file:
		    output_file.write(html_output)



		# 用默认浏览器打开生成的 HTML 文件
		if(isopen==1):
			webbrowser.open(output_file_path)


if __name__ == '__main__':


	# dydata={
	# 		'0板': 
	# 			[ 
	# 				[1672675200000.0, 0], [1672761600000.0, 0], [1672848000000.0, 1], [1672934400000.0, 0], 
	# 				[1673193600000.0, 0], [1673280000000.0, 0], [1673366400000.0, 0], [1673452800000.0, 0], 
	# 				[1673539200000.0, 1], [1673798400000.0, 2], [1673884800000.0, 2], [1673971200000.0, 1], 
	# 				[1674057600000.0, 2], [1674144000000.0, 0], [1675008000000.0, 0], [1675094400000.0, 0]
	# 			],
	# 		'1板': 
	# 			[
	# 				[1672675200000.0, 0], [1672761600000.0, 0], [1672848000000.0, 1], [1672934400000.0, 0], 
	# 				[1673193600000.0, 0], [1673280000000.0, 0], [1673366400000.0, 0], [1673452800000.0, 0], 
	# 				[1673539200000.0, 1], [1673798400000.0, 1], [1673884800000.0, 1], [1673971200000.0, 0], 
	# 				[1674057600000.0, 1], [1674144000000.0, 0], [1675008000000.0, 0], [1675094400000.0, 0],
	# 			]
	# 	}

 # 	#timestamp =(datetime.strptime(day, "%Y-%m-%d")).timestamp()*1000#转为linux时间
 	
	# print(dydata)

	#HC可视化().get_chart(dydata,"证券",1)


 

	dynamic_data = [
            [int(datetime(2023, 1, 1).timestamp())*1000, 2], 
            [int(datetime(2023, 1, 3).timestamp())*1000, 3],
            [int(datetime(2023, 1, 4).timestamp())*1000, 4],
            [int(datetime(2023, 1, 5).timestamp())*1000, 5],
            [int(datetime(2023, 1, 6).timestamp())*1000, 6],
            [int(datetime(2023, 1, 7).timestamp())*1000, 7],
            [int(datetime(2023, 1, 9).timestamp())*1000, 7],
            [int(datetime(2023, 1, 10).timestamp())*1000, 2],
            [int(datetime(2023, 1, 11).timestamp())*1000, 3],
            [int(datetime(2023, 1, 12).timestamp())*1000, 1],
            [int(datetime(2023, 1, 13).timestamp())*1000,2],
            [int(datetime(2023, 1, 14).timestamp())*1000,3],
            [int(datetime(2023, 1, 15).timestamp())*1000, 4],
            [int(datetime(2023, 1, 18).timestamp())*1000,5],
            [int(datetime(2023, 1, 19).timestamp())*1000, 5],

        ];
	print(dynamic_data)
	
 

	labelCoordinates = [
			{ 'date':int(datetime(2023, 1, 7).timestamp())*1000, 'yValue': 3, 'labelText': 'Montrond' },
			{ 'date': int(datetime(2023, 1, 15).timestamp())*1000, 'yValue': 5, 'labelText': 'Saint-Claude' },
		]

	HC可视化().get_标注曲线(dynamic_data=dynamic_data,labelxy=labelCoordinates,name="证券",isopen=1)

	#print(a)

	 