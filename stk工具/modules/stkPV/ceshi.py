#取000001的前复权行情
import tushare as ts
df = ts.pro_bar(ts_code='000001.SH', asset='I', start_date='20180101', end_date='20181011')