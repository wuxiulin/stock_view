from 买入 import 买入类
from 选股 import 选股类
from 卖出 import 卖出类
from 盈利 import 盈利类
from 数据AP import 数据AP类 
import akshare as ak
def test(choseday='20231213',flag_out=1):
		#如下是某一天，通过均线突破，选股，买入，卖出，计算盈利，得到个股盈利 散点图
	a=选股类()
	a.均线突破_wencai(period='D',choseday=choseday,ma='250',srhtxt='去掉北交所')
	if(flag_out==1):
		print("-------------------选出代码---------")
		print(a.get_选股代码())

	b=买入类()
	b.买入成本(T=1,Buytype=1,chose类=a)
	if(flag_out==1):
		print("-------------------买入价格和时间---------")
		print(b.get_买入价格())
		print(b.get_买入时间())

	c=卖出类()
	c.卖出价格(T=1,Selltype=1,buy类=b)	#这里是为了传递买入的成本和时间等信息
	if(flag_out==1):
		print("-------------------卖出价格和时间---------")
		print(c.get_卖出价格())
		print(c.get_卖出时间())
	
	d=盈利类()
	d.盈利计算(buy类= b ,sell类= c,profittype=1)

	dd=d.get_盈利涨幅()
	if(flag_out==1):
		print("-------------------盈利---------")
		print(dd)

	#组织数据，然后展示图表，这里是需要手动选择

	e=数据AP类()
	ee=e.数据重构(src_type=1,des_type=2,data=dd)
	if(flag_out==1):
		print("-------------------数据重构---------")
		print(ee)

	if 1:
		ee.sort()#散点图排序比不排序更能看出大多数区间平均值稳定性
		#平均值有意义，但是还是个例，所以考虑去掉最大最小值
		#print(ee)
	if 0:#去掉极大极小10%区间，不是点，而是10%最大，最小，
		delnum=int(len(ee)*0.1)
		ee=ee[delnum:-1*delnum]
	e.散点图(data=ee,init=0,templt_name='./tplt/散点折线图.html',desname='./测试tplt/'+(c.get_卖出时间())+'散点折线图.html')
	return ee


if __name__ == '__main__':
 

	#如下是某一天，通过均线突破，选股，买入，卖出，计算盈利，得到个股盈利 散点图
	#test()
	#通过观察散点图，看到一些结论，尝试进行test1
	#去掉极大值极小值 10%的是数据
	#

	#看了某一天，某一天，通过均线突破，选股，买入，卖出，计算盈利，得到个股盈利 散点图
	#个别相对极限，大多数都是类似涨幅，那么多日的 平均值看看规律配合离散程度
	#
	start='20231101'
	trade_df = ak.tool_trade_date_hist_sina()#正序列表，最新日期在最后
	trade_df=[d.strftime("%Y%m%d") for d in list(trade_df['trade_date'])]#时间类型不对，转换
	if start in trade_df:
		index = trade_df.index(start)
	else:
		print(start ,"  choseday 输入不是交易日，或者格式有误，这里输入类似  20231215 ")


	day_ave_zf=[]
	每日选股数量=[]
	for i in range(index,index+10):
		day=trade_df[i]#在这天买
		print(day)
		data=test(choseday=day,	flag_out=0)
		每日选股数量.append(len(data))
		day_ave_zf.append(round(sum(data)/len(data),2))

	e=数据AP类()
	e.散点图(data=day_ave_zf,init=0,templt_name='./tplt/散点折线图.html',desname='./测试tplt/'+'均值'+'散点折线图.html')
	e.散点图(data=每日选股数量,init=0,templt_name='./tplt/散点折线图.html',desname='./测试tplt/'+'_每日选股数量_'+'散点折线图.html')