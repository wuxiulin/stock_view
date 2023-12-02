import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__)) 
#print(current_dir)
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)                           
#模块根目录要在运行中写入path，然后可以通过
#from  stk工具.common import DataStruct 等类似绝对路径来读取引入模块，但是测试单独模块式后可能还是有问题，
#所以单独在sys.path.append(parent_dir)   根目录就是了，后面在注销掉，影响不大！
 
from datetime import datetime
 
import stk工具.common
import stk工具.modules.noteplt as noteplt
from stk工具.modules.stkPV import sktPriceVol
from stk工具.modules.可视化stock.stocks可视化 import HC可视化


#这个文档好处是，纷杂的工作不用记忆，不用重复，不用切换，不用花很多时间精力，专注更重要东西
#例如，证券个股三连板重要信号，不太容易在同花顺比较方便的得到这个信号，花费心力每天盯着，但是有这个文件，就不用花费，
#而是需要关注新指标增删就好了，和直接利用结论文档复盘，
#很多指标自己都容易忘记，错过很多机会，或者说太多指标浪费太多心力去查看，导致自己每天忙在切换和查看上，浪费心力，不是每天都有信号，时间长了
#倦怠。所以需要工具来解决重复工作！更多时间精力在更重要信号思考上，而不是重复查看是否有信号上！
#
#
#不同工具配合使用，虽然想集成，但是很多不好在同花顺实现，不好在python代码中，能实现就实现，不要强求，集成一大部分就好了！
#
#
# ***需要监控的指标做好分类，可以先写，先用，积累一段时间后，后面在分类，毕竟太少不好精确分类！
#分类后方便修改查找！
#
#********添加一个指标，功能，都要做好记录备注使用方便后面用，和上传github，做好保存防止丢失
#每个指标标题后面加上链接，能链接到有道云笔记，看这个指标的notes注解，和跟踪注解，和指标经典
#
#
#输出信号分类别和级别的！
#可以交叉重复无所谓的！就是说信号即是个股信号也是板块信号，也是大盘信号，那么三个地方都输出就是，无所谓
#所以给出不同类型的数组？看看信号输出哪里就是了！

#a=common.DataStruct()
#print(a.data) 



#收集股票价量异动信息
a=sktPriceVol()
#out=a.stk_pv_monitor()#所有监控#a.data也行
#print(out)
#res=a.test_txt()#测试代码
#print(res.data)

#保存html文档notes
#noteplt.notes_stocks(data=out.data,page_type=20) #page_type，设置需要改那个页面内容



aa=sktPriceVol().多日天地板(start="20231120")
#print('**************')
#print(aa)
label天地板=[]
for day in aa['date']:
	if(aa['data'][day] ):#非空字典
		label天地板.append(aa['data'][day])
# print('**************')
# print(label天地板)
# print(type(label天地板[0]['labelText']))
# print('**************')
# bb=sktPriceVol().多日地天板(start="20231120")
# print(bb)



dynami000c_data=a.多日连板统计(start="20231115")
# print(dynami000c_data)
# # print(type(dynami000c_data[0][0]))
# dynamic_data = [
#             [int(datetime(2023, 1, 1).timestamp())*1000, 2], 
#             [int(datetime(2023, 1, 3).timestamp())*1000, 3],
#             [int(datetime(2023, 1, 4).timestamp())*1000, 4],
#             [int(datetime(2023, 1, 5).timestamp())*1000, 5],
#             [int(datetime(2023, 1, 6).timestamp())*1000, 6],
#             [int(datetime(2023, 1, 7).timestamp())*1000, 7],
#             [int(datetime(2023, 1, 9).timestamp())*1000, 7],
#             [int(datetime(2023, 1, 10).timestamp())*1000, 2],
#             [int(datetime(2023, 1, 11).timestamp())*1000, 3],
#             [int(datetime(2023, 1, 12).timestamp())*1000, 1],
#             [int(datetime(2023, 1, 13).timestamp())*1000,2],
#             [int(datetime(2023, 1, 14).timestamp())*1000,3],
#             [int(datetime(2023, 1, 15).timestamp())*1000, 4],
#             [int(datetime(2023, 1, 18).timestamp())*1000,5],
#             [int(datetime(2023, 1, 19).timestamp())*1000, 5],

#         ]

#print(dynami000c_data)

# #数据重新组织一下数据
# print(dynami000c_data['date'])
# print(dynami000c_data['date'].index("2023-11-06"))
# print(dynami000c_data['date'].index("2023-12-01")+1)
tradedays = dynami000c_data["date"][dynami000c_data['date'].index("2023-11-15"):dynami000c_data['date'].index("2023-12-01")+1]#g根据输入获得tradedays
dydata=[]
for day in tradedays:#按照时间顺序，读取，然后push
	dydata.append(dynami000c_data['data'][day])

# labelxy = [
# 		{ 'date':int(datetime(2023, 11, 16).timestamp())*1000, 'yValue': 3, 'labelText': 'Montrond' },
# 		{ 'date': int(datetime(2023, 11, 25).timestamp())*1000, 'yValue': 5, 'labelText': 'Saint-Claude' },
# 	]

print(label天地板)
print(dydata)
for idata in label天地板:
	date=idata['date']
	temp=[ i[1] for i in dydata if(i[0]==date)]
	idata['yValue']=temp[0]
print(label天地板)

HC可视化().get_标注曲线(dynamic_data=dydata,labelxy=label天地板,name="情绪连板",isopen=1)






