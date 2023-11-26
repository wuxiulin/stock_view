#2023年11月16日阶段涨停统计

#stock_zt_pool_em() 接口只有最近10多天 数据，算了，，通过问财获取更多
import pywencai  #https://github.com/zsrl/pywencai


def get_同花顺概念指数():#爬取概念：看新增：标注时间：完成，直接用，如果对时间不要求，其实自己用时候爬取就是了！时间不多的！
	search_txt="概念指数"
	res = pywencai.get(query=search_txt, loop=True, query_type='zhishu')#sort_key='退市@退市日期',sort_order='asc'
	#print(res)
	#res.to_csv("概念指数.csv")
	return res


#涨停类似别，不要请轻易删除，都是加分了，不是单个，多个概念才加分，
#做个涨停理由统计，在名称后面标注，今天涨停的有多少个这个理由的，


#还是要手动晒一下的，要么先代码，


def get_阶段涨停统计(day="20231122",):
	#同花顺概念指数
	search_txt="概念指数"
	concepts_indexs = pywencai.get(query=search_txt, loop=True, query_type='zhishu')#sort_key='退市@退市日期',sort_order='asc'
	names_cnps=list(concepts_indexs["指数简称"])
	

	search_txt=day+"阶段涨停统计，按照连续涨停天数排序，去掉ST股，去掉北交所"
	res = pywencai.get(query=search_txt, loop=True, query_type='stock')#sort_key='退市@退市日期',sort_order='asc'
	print(res)
	res["核心涨停原因"]=[[]]*len(res['股票代码'])
	#交叉所属概念和涨停原因！如果同花顺更新不及时，可能交叉有误，这没办法！
	#先用着，出问题再说
	columns=res.columns
	zt_res_col=([ i  for i in columns  if('涨停原因类别' in i)  ])[0]
	#print(zt_res_col)
	for i in range(len(res['股票代码'])):
		#print(res.loc[i,zt_res_col])
		zt_reasons=(res.loc[i,zt_res_col]).split('+')
		temp_reasons=[]
		for reason in zt_reasons:
			if( reason in names_cnps ):
				temp_reasons.append(reason)
			# else:
			# 	temp=[ i for i in names_cnps if (reason in i )]
			# 	#有时候导致太多，类似华为，涨停原因，但是不是概念，但是能in很多概念里，导致很多输出，
			# 	temp_reasons=temp_reasons+temp
			else:
				temp=[ i for i in names_cnps if (reason in i )]
				if(len(temp)==1):
					temp_reasons=temp_reasons+temp
				#有时候导致太多，类似华为，涨停原因，但是不是概念，但是能in很多概念里，导致很多输出，
				
		if(len(temp_reasons)==0):
			for reason in zt_reasons:
				temp=[ i for i in names_cnps if (reason in i )]
				temp_reasons=temp_reasons+temp

		#print(temp_reasons)
		#res["核心涨停原因"][i]=temp_reasons    
		#res.loc[i,"核心涨停原因"]=temp_reasons   
		res.at[i,"核心涨停原因"]=temp_reasons  

	print(res["核心涨停原因"])
 





if __name__ == '__main__':
	get_阶段涨停统计()
	#get_同花顺概念指数()