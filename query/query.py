# 1.导入Flask扩展
from flask import Flask, request, render_template
from getdata import get_data#自己写的代码被导入

from 情绪指标 import  连板股_连板数统计
import json

# 2.创建Flask应用程序实列
# 需要传入__name___，作用是为了确定资源所在路径
app = Flask(__name__)
# 3.定义路由及其视图
# Flask中定义路由时通过装饰器实现的
@app.route('/', methods=['GET', 'POST'])  #为啥要先这样，在如下才能启动？为啥？
@app.route('/query/', methods=['GET', 'POST'])
#名字不对，自己文件夹不是html中是/query/,这里源代码也是这个但是自己改了文件夹名字，但是如果html中改成showweb不对的， 不清楚怎么匹配 这样问题是无法网页查询
#把工程文件夹名字改为query，然后这里改为@app.route('/query/'），html中<form id="form" name="form" method='POST' action='/query/'> 匹配地址，这样能在线查询
#
# def query():
#     if request.method == 'POST':
#         code = request.form.get('name')
#         dict_return = get_data(code)   # https://www.cnblogs.com/zpf666/p/10438423.html
#         lb=连板股_连板数统计(连板数=3,start='2023-11-11',end='')#时间先不从网页获取
#         dict_return.update(lb)#合并, #似乎只能传一个参数，所以组合起来看看，且元素不能是数字，要str
#         return render_template('query.html', dict_return = dict_return,dict2=lb)   

#     else:
#         dict_return = get_data('601318')
#         lb=连板股_连板数统计(连板数=3,start='2023-11-11',end='')#时间先不从网页获取
#         dict_return.update(lb)
#         print(dict_return)
#         return render_template('query.html', dict_return = dict_return,dict2=lb)  # json.dumps()

def query():
    if request.method == 'POST':
        code = request.form.get('name')
        dict_return = get_data(code)   # https://www.cnblogs.com/zpf666/p/10438423.html
       
        lb=连板股_连板数统计(连板数=3,start='2023-11-11',end='')#时间先不从网页获取

        return render_template('query.html', dict_return = dict_return,dict2=lb)   
         
    else:
        dict_return = get_data('601318')
        
        lb=连板股_连板数统计(连板数=3,start='2023-11-11',end='')#时间先不从网页获取
        result=dict()
        for i in range(len(lb['data']['曲线'])):
            tt=lb['data']['曲线'][i]
            tt=[str(i) for i in tt]
            temp={str(i+2):tt}
            
            result.update(temp)
        #print(result)
        df_lb={'0':lb['date'],'1':list(lb['data']['名称'])}#日期横坐标，名称是图例，result是纵坐标
        result.update(df_lb)
        print(result)
         
         
        return render_template('query.html', dict_return = dict_return,dict2=result)   





if __name__ == '__main__':
   #app.run(host='0.0.0.0', port=5000,debug = True)
   app.run(debug = True)