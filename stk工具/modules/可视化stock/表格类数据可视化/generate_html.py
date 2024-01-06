#这个代码和html模版放在一个文件夹，然后再文件夹路径中cmd
# cmd 中执行  python -m http.server
# http://localhost:8000/index.html      就能打开index.html  刷新能看到调试状态，一种调试方式

html_template = """
<tr>
    <td>{symbol}</td>
    <td>{company}</td>
    <td>{price}</td>
    <td>{change}</td>
</tr>
"""

stock_data = [
    {'symbol': 'AAPL', 'company': 'Apple Inc.', 'price': 150.25, 'change': '+2.5%'},
    {'symbol': 'GOOGL', 'company': 'Alphabet Inc.', 'price': 2700.50, 'change': '-1.2%'},
    # 其他股票数据
]

# 构建 tbody 部分
tbody_content = ""
for stock in stock_data:
    tbody_content += html_template.format(**stock)

# 将生成的 tbody 替换到原始 HTML 文件中
with open("index.html", "r",encoding="utf-8") as file:
    html_content = file.read()
    html_content = html_content.replace("<!-- Table rows will be dynamically inserted here using Python -->", tbody_content)

with open("index.html", "w",encoding="utf-8") as file:
    file.write(html_content)
