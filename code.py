#XSHG 上海证券交易所 XSHE 深圳证券交易所
# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import talib
import numpy as np
import math
import pandas

# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
   
    context.s1 = "002230.XSHE"
    #obsevation相当于缓冲数据,只要大于SMA(简单移动平均线)即可
    context.OBSERVATION = 40
    context.SMA = 27

    
# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

   
    high = history(context.OBSERVATION,'1d','high')[context.s1].values
    low = history(context.OBSERVATION,'1d','low')[context.s1].values
    close = history(context.OBSERVATION,'1d','close')[context.s1].values
    MIX = (high+low+close)/3  

    SMA = talib.SMA(MIX,context.SMA)    
    
    currentPrice = bar_dict[context.s1].close
   
     # 计算现在portfolio中股票的仓位
    curPosition = context.portfolio.positions[context.s1].quantity
    # 计算现在portfolio中的现金可以购买多少股票
    shares = context.portfolio.cash/bar_dict[context.s1].close
    

    plot('currentPrice',currentPrice)
    plot('SMA', SMA[-1])
    
    if currentPrice > SMA[-1] and curPosition == 0:
        order_target_percent(context.s1,1)     
    
    if currentPrice < SMA[-1] and curPosition !=0:
        order_target_percent(context.s1,0)
