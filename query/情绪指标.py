#上升周期的赚钱效应来自于，各种变着花样的涨：
#核心是涨。
#冲高回落，次日反包；烂板了，次日弱转强。
#下降周期的亏钱效应正好相反，各种变着花样的跌。核心是跌。
#冲高回落，次日低开低走，烂板了，次日核按钮。
#衡量情绪到底是好是坏，看一些关键性个股的走势就够了。



#各种变着花样的涨：最极致的涨的方式，统计观察。各种关键词，都是一种监控角度！反核，大长腿，都是特定阶段才更大概率有的的图形，
#例如大长腿，是情绪情绪恐慌到极致的疯狂的日内变化，导致的图形。日内分歧转一致，这种短时间的巨大的心态转变，为啥，什么导致恐慌，
#什么导致又转变到极致看多，为啥能极致看多这么极致其实很难理解。
#但是可以知道的是一定是一波极致赚钱效应之后，极致贪婪，才会突然诱发极恐慌-核按钮，至于为啥恐慌，可能是盘中或盘后消息。
#这个时候所谓的情绪周期一个转折点重要的时刻，在没有出现之前认为一直是涨就是不要怕，等核按钮出来再说，有了核按钮不一定马上跌，不一定的
#怕就是慢慢减仓，小仓位加仓尝试，这就是龙头连板妖股玩法没有转折信号不要怕
#等转折信号出现，进入下一个阶段，可能能是反核，可能是持续恐慌，都是可能演化，都是可能失败的，不要执迷固定的周期。！耐心等待或持有-出现信号--根据信号应对-不同应对方式
#
#卡位啊，接力啊，等，其实无所谓，主要是大资金态度大资金参与情况，卡位是资金离开之前妖股去了新的股票都去了么，如果没有去，这卡位质疑，去了才叫卡位！

#所以一看市场资金流动！！散户和大资金通过打板资金看流动！
#
#
#


#涨幅：连板是最极致的情绪贪婪体现，由于300是20%所以有了分化！
#单日涨幅
#连板涨幅
#连板个数


#连板数，统计，虽然300票三连板抵上其他票6个板，但是这里不计较这些！
#
#
#
##
#

#设置某日统计起点
#统计当天涨停股，然后回顾这些股历史涨停数据
#第一种方式是历史每天涨停codes然后比对
#第二种是每个个股回顾历史每一天

#在起点这天采用，第二种快速建立起起点这天情况，然后，之后每天是采用第一种比较合适！快速

#怎么爬取每天涨停个股？
#
import akshare as ak
import json

import datetime
from datetime import date
import pandas as pd


def dict_to_json(dic_data):
	#dict1 = {"小明":4,"张三":5,"李四":99}
	with open("股票池.json","w", encoding='utf-8') as f: ## 设置'utf-8'编码
	#为了让json文件更美观，可以设置indent进行缩进
	# 如果ensure_ascii=True则会输出中文的ascii码，这里设为False
	    f.write(    json.dumps(   dic_data  ,ensure_ascii=False , indent=4   )     )  

def json_to_dict(filename=""):
	with open(filename,"r", encoding='utf-8'  ) as f:
	    load_dict = json.load(f)

	print(load_dict)





def 连板股_连板数统计(连板数=3,start='',end=''):#连板数=3,小于连板数的个股不统计，start：统计开始时间
	#处理时间开始结束交易日
	
	#处理时间
	trade_date_df = ak.tool_trade_date_hist_sina()#获取交易日
	trade_date_list = trade_date_df["trade_date"].astype(str).tolist()
	#print(trade_date_list)
	if(start==''):
		print('start error')
		return
	if('-' not in start):
		print("start is like 2023-11-11")
		return 
	day=datetime.datetime.strptime(start,"%Y-%m-%d")
	while datetime.datetime.strftime(day,"%Y-%m-%d")  not in trade_date_list:  # 如果当前日期不在交易日期列表内，则当前日期天数减一
		day =  day+ datetime.timedelta(days=1)

	start=datetime.datetime.strftime(day,"%Y-%m-%d")#

	if(end==''):
		end = date.today()
		end = datetime.datetime.strftime(end,"%Y-%m-%d")
		while(end not in  trade_date_list):#今天是周末或假期
			end=datetime.datetime.strptime(end,"%Y-%m-%d")-datetime.timedelta(days=1)
			end=datetime.datetime.strftime(end,"%Y-%m-%d")
	else:
		day=datetime.datetime.strptime(end,"%Y-%m-%d")
		while datetime.datetime.strftime(day,"%Y-%m-%d")  not in trade_date_list:  # 如果当前日期不在交易日期列表内，则当前日期天数减一
			day =  day - datetime.timedelta(days=1)
		
		end=datetime.datetime.strftime(day,"%Y-%m-%d")

	#print(start,end)
	daylist=trade_date_list[trade_date_list.index(start):trade_date_list.index(end)+1]
	#print(daylist)
	#print(daylist)
	#
	out=[]
	#处理start这天快照 #接口数据有限，所以即使保存
	temp=start.split('-')
	start_shotcut = ak.stock_zt_pool_em(date=temp[0]+temp[1]+temp[2])#么有st和北交所，涨停股票池   涨停统计n/m，m天中n次涨停  连板数
	#print(start_shotcut)

	
	#处理看codes在start这天第几板情况
			#第一种方式是历史每天涨停codes然后比对
			#第二种是每个个股回顾历史每一天
		#但是数据中已经有了stock_zt_pool_em(),所以不用统计了
	#所以处理思路不用处理start之前的情况，直接有结果了！但是统计时间很长，这个接口可能没有数据，所以其他需要统计，以后补缺口！

	#有了起始状态，那么怎么添加处理？
	stitcs_df=start_shotcut[start_shotcut['连板数'] >=3]  ##要统计和显示的codes start是三板开始基础上增删，以后再改是从1板还是四五板
	stitcs_df=stitcs_df.reset_index(drop=True)

	stitcs_df['曲线']=[list([stitcs_df['连板数'][x]]) for x in range(len(stitcs_df.index))]
	#print(stitcs_df)

	dayls=daylist[1:]
	for dayi in range(len(dayls)):#去掉开始那天数据
		day=dayls[dayi]
		#print('****************************',day,'***********************************')
		#print('****************************',day,'***********************************')
		#print('****************************',day,'***********************************')
		#print('****************************',day,'***********************************')
		temp=day.split('-')
		data = ak.stock_zt_pool_em(date=temp[0]+temp[1]+temp[2])#么有st和北交所，涨停股票池   涨停统计n/m，m天中n次涨停  连板数
		data=data[data['连板数']>=3]
		data=data.reset_index(drop=True)
		data['曲线']=[list([data['连板数'][x]]) for x in range(len(data.index))]
		#print(data)
		data['曲线'] = data['曲线'].astype('object')#为了配合data.at，解决告警问题，.loc 和df[][]会大量问题
		#合并数据，连板的用最新的，新增的直接添加，断板的继续跟踪，修改涨停统计+1，不用这个数据就先不改
		for code in list(stitcs_df['代码']):
			if(code in list(data['代码'])):#使用最新的，
				#print(code+"   6666")
				# if(code =='001300'):
				#print(list(data[code==data['代码']]['曲线'])[0])
				#print(list(stitcs_df[code==stitcs_df['代码']]['曲线'])[0])
				#print(type(data[code==data['代码']]['曲线']),data[code==data['代码']]['曲线'])
				#print(data[code==data['代码']]['曲线'].index)
				index=(data[code==data['代码']]['曲线'].index)[0]
				#data.loc[index,'曲线']=list(stitcs_df[code==stitcs_df['代码']]['曲线'])[0] + list(data[code==data['代码']]['曲线'])[0]#错误.loc 不能直接存入列表
				#data['曲线'][index]=list(stitcs_df[code==stitcs_df['代码']]['曲线'])[0] + list(data[code==data['代码']]['曲线'])[0]#会告警
				data.at[index,'曲线'] = list(stitcs_df[code==stitcs_df['代码']]['曲线'])[0] + list(data[code==data['代码']]['曲线'])[0]
				#data[code==data['代码']]['曲线'] =  list(stitcs_df[code==stitcs_df['代码']]['曲线'])[0] + list(data[code==data['代码']]['曲线'])[0]
				
				#print(data,'33333')
				continue
			else:#旧code断板，处理方式是，继续跟踪一下
				#print(code+"   7777")
				#data.iloc[len(data)-1] = data[data["代码"]== code]
				data=pd.concat([data, stitcs_df[stitcs_df["代码"]== code]])
				#data['曲线']=[ i+[i[-1]] for i in data['曲线'] ]
				data=data.reset_index(drop=True)
				#print(data['曲线'])
				tem=data.loc[data.index[-1],'曲线']
				tem=tem+[tem[-1]]
				index=(data[code==data['代码']]['曲线'].index)[0]
				data.at[index,'曲线']=tem
				#data['曲线'][index]=tem#data.loc[data.index[-1],'曲线']+[tem[-1]]#告警问题
				data=data.reset_index(drop=True)
				#print(data,'4444')

		#print(data,'#####################################################')
		for code in list(data['代码']):#新增代码数据处理
			if(code not in list(stitcs_df['代码'])):
				index=(data[code==data['代码']]['曲线'].index)[0]
				tem=data['曲线'][index]
				tem=[0]*(dayi+1)+tem
				data.at[index,'曲线']= tem

		stitcs_df=data.copy(deep=True)#深度复制完全独立
		
		#print(stitcs_df)
		#data中有新进3板，有继续连板的，有短板持续跟踪一下
	#print(stitcs_df)
	#res=stitcs_df['曲线'][0]
	#res=[str(i) for i in res]
	#print(res)
	#out={"date":daylist,'data':res}

	#print(out,type(out))

	out={'data':stitcs_df,'date':daylist}

	# result={}
	# for i in range(len(out['data']['曲线'])):
	# 	temp={str(i+2):out['data']['曲线'][i]}
	# 	result.update(temp)
	# print(result)


	#print(json.dumps(list(out['data']['名称'])))
    
	# result=dict()
	# for i in range(len(out['data']['曲线'])):
	# 	tt=out['data']['曲线'][i]
	# 	tt=[str(i) for i in tt]
	# 	temp={str(i+2):tt}
	# 	result.update(temp)

	# df_lb={'0':out['date'],'1':list(out['data']['名称'])}#日期横坐标，名称是图例，result是纵坐标
	# result.update(df_lb)
	# #print(df_lb)
	# #print(result)
	# dict2=json.dumps(result)
	#print(out)

	return out






	#读取历史数据
	


		#通过问财来爬取！

	#start那天涨停情况codes
    



#建立字典，按照日期，取股票池，
#如果结果不行就换接口就是了！

	

	#回顾codes历史涨停数，作为start起点数据开始统计

	

	#开始start+1 +2 +3 等开始统计



	#保存数据
if __name__ == '__main__':
	连板股_连板数统计(连板数=3,start='2023-11-11',end='')