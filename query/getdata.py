#import tushare as ts
import akshare as ak
import pandas as pd
def get_data(code):

    #pro = ts.pro_api()
    
    dict_return = {} # 存放需要的数据

    # try:#每个小时调用一次，好坑
    #     passss_codes = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name')#上市代码
    #     ss_codes.to_csv("codes.csv")
    # except Exception as e:
    #     ss_codes = pd.read_csv("codes.csv")
        
    ss_codes = ak.stock_zh_a_spot_em()
    #print(ss_codes)
    
    

    #code 格式检查
    if('.' in code):
        strs=code.split(".")
        if(len(strs)>2):#格式有问题
            return dict_return
        if(len(strs)==2):#格式正确，但是前后缀，需要检查一下
            if(strs[1].upper()!="SH" and  strs[1].upper()!="SZ"):#转为大写,后缀不对
                return dict_return
            if(strs[0] not in list(ss_codes["代码"])): #代码不对
                return dict_return  
        
        else:#<2  检查6位代码对不对
            if(strs[0] not in list(ss_codes["代码"])): #代码不对
                return dict_return  
        code=strs[0]+strs[1].upper()
    else:#检查6位代码对不对
        if(code not in list(ss_codes["代码"])): #代码不对
            return dict_return  
        #print(ss_codes[code == ss_codes["代码"]].index )  #print(df['name'].str.contains('li'))
        #code=code+""
        else:#code是对的
            pass
    #代码检查完毕正确    
    
    #data = pro.daily(ts_code='000001.SZ')#start_date='20231101', end_date='20231118'  取所有数据  tushare太坑这个接口

    data = ak.stock_zh_a_hist(symbol=code, period="daily",  adjust="qfq")#start_date="20170301", end_date='20210907'
    #print(data)
    #return
    data_30 = data[-30:] #data[:30].iloc[::-1] # 取最新30个数据，按照按照日期正序排列数据
    data_30['rise'] = data_30['涨跌额'] > 0 # 涨
    data_30['fall'] = data_30['涨跌额'] < 0 # 跌
    close = data_30['收盘'] #最近30个交易日的收盘价
    close_index = list(close.index) # 收盘价x轴数据
    #print(close_index)
    close_value = close.values.tolist() # 收盘价y轴数据

    df_diff = data_30[['rise','fall']].sum() # 统计近30交易日的涨跌次数
    #print(df_diff)
    df_diff_index = list(df_diff.index) # 将数据转为列表格式
    #print(df_diff)
    df_diff_value = df_diff.values.tolist() # 将数据转为列表格式
    
    dict_return['diff'] = [{"name":item[0],"value":item[1]} for item in list(zip(df_diff_index,df_diff_value))] # 将数据制作成饼图需要的数据格式
    price_change = data_30['涨跌额'].values.tolist() # 统计近30交易日的价格变化
    volume = data_30['成交额'].values.tolist() # 统计近30交易日的成交量
    # 以下为将处理好的数据加入字典
    dict_return['close_index'] = close_index 
    dict_return['close_value'] = close_value
    dict_return['price_change'] = price_change
    dict_return['volume'] = volume
    dict_return['df_diff_index'] = df_diff_index
    #print(dict_return)
    return dict_return
if __name__ == '__main__':
    print(get_data('601318'))