#证监会审核发行日期1（文中还有一个日期更早），
#明确申购日期2的日期3， 
#招股发行/网上申购日期2- ---
#上市委员会审核-上市交易日期4
#风向标关键是允许发行数量，和上市数量

http://www.csrc.gov.cn/csrc/c101955/zfxxgk_zdgk.shtml
import akshare as ak

stock_xgsglb_em_df = ak.stock_xgsglb_em(symbol="全部股票")#{"全部股票", "沪市主板", "科创板", "深市主板", "创业板", "北交所"}
print(stock_xgsglb_em_df)