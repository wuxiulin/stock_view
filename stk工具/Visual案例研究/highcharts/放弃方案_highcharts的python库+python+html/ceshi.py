# 1-导入库和实例化
from highcharts import Highchart
#安装后可能有问题调用，修改那几个有问题库名字就好！
chart = Highchart()
 
# 2-配置项设置
options = {
    'chart': {
        'inverted': True  # 翻转x轴和y轴
    },
    'title': {  # 主标题
        'text': 'Atmosphere Temperature by Altitude'
    },
    'subtitle': {  # 副标题
        'text': 'According to the Standard Atmosphere Model'
    },
    'xAxis': {  # x轴设置
        'reversed': False,
        'title': {
            'enabled': True,
            'text': 'Altitude'
        },
        'labels': {
            'formatter': 'function () {\
                return this.value + "km";\
            }'
        },
        'maxPadding': 0.05,
        'showLastLabel': True
    },
    'yAxis': {  # y轴设置
        'title': {
            'text': 'Temperature'
        },
        'labels': {
            'formatter': "function () {\
                return this.value + '°';\
            }"
        },
        'lineWidth': 2
    },
    'legend': {  # 图例设置
        'enabled': False
    },
    'tooltip': {  # 提示工具设置
        'headerFormat': '<b>{series.name}</b><br/>',
        'pointFormat': '{point.x} km: {point.y}°C'
    }
}
 
# 3-实例化对象中添加配置
chart.set_dict_options(options)
 
# 4-绘图所需的数据和添加数据
data =  [[0, 15], 
         [10, -50], 
         [20, -56.5], 
         [30, -46.5], 
         [40, -22.1], 
         [50, -2.5], 
         [60, -27.7], 
         [70, -55.7], 
         [80, -76.5]]
# 添加数据
chart.add_data_set(data, 'spline', 'Temperature', marker={'enabled': False}) 
 
# 5-在线绘图
# 保存图表为 HTML 文件
chart.save_file('highcharts_chart.html')