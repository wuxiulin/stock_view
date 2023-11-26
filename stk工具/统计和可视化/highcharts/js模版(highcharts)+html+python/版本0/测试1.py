#pip install Jinja2
#四个js文件，是highechart的
#生成template ，创建一个 Jinja2 模板文件（比如 template.html） 


#创建一个 Python 脚本，使用 Jinja2 渲染模板并将动态数据传递给模板：
import webbrowser
from jinja2 import Template

# 准备数据，这里使用一个简单的列表作为示例
dynamic_data = [1, 2, 3, 4, 5]

# 读取模板文件
with open('template.html', 'r', encoding='utf-8') as template_file:
    template_content = template_file.read()

# 创建 Jinja2 模板对象
template = Template(template_content)

# 使用模板渲染 HTML，传递动态数据
#在上面的代码中，dynamic_data 是一个包含你希望替换的动态数据的列表。
#模板中的 {{ data | tojson | safe }} 部分将 Python 中的数据转换为 JSON 格式，并嵌入到 JavaScript 代码中。
html_output = template.render(data=dynamic_data)

# 将生成的 HTML 写入文件
output_file_path='output.html'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write(html_output)



#运行这个 Python 脚本，它将生成一个 HTML 文件（比如 output.html），其中包含动态数据的 JavaScript 代码。打开这个 HTML 文件，
#你应该能够看到 Highcharts 图表，其中的曲线数据是你在 Python 中指定的动态数据。


# 用默认浏览器打开生成的 HTML 文件
webbrowser.open(output_file_path)