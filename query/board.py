import vizro.plotly.express as px
from vizro import Vizro
import vizro.models as vm
import pandas as pd

from 情绪指标 import  连板股_连板数统计

lb=连板股_连板数统计(连板数=5,start='',end='')#时间先不从网页获取
print(lb['date'])
#print(lb)
arr=[  i  for i in lb['data']['曲线']]
#print(arr)
index_columns=lb['data']['名称']
df=pd.DataFrame(data = dict(zip(index_columns,arr)))
#print(df)

#print(help(px.line))

#index_x=[ i[:4]+i[5:7]+i[8:10]  for i in lb['date']]
index_x= lb['date']
#print(index_x)
#df = px.data.iris()
page = vm.Page(
    title="My first dashboard",
    components=[
                vm.Graph(id="line",figure=px.line(y=df.columns,data_frame=df,x=index_x)) ,
                #vm.Graph(id="scatter_chart", figure=px.scatter(df, x="sepal_length", y="petal_width", color="species")),
                # vm.Graph(id="hist_chart", figure=px.histogram(df, x="sepal_width", color="species")),            
                ],
    # controls=[
    #             vm.Filter(column="species"),
    #         ],
)

dashboard = vm.Dashboard(pages=[page])

Vizro().build(dashboard).run()
