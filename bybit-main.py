import pandas as pd
import datetime as dt
import plotly.graph_objects as go
import calendar
import requests

symbol = 'BTCUSD' #symbol to be traded
tick_interval = '1' #candle in minutes

now = dt.datetime.utcnow()
unixtime = calendar.timegm(now.utctimetuple())
since = unixtime
start = str(since - 60 * 60 * int(tick_interval))    
url = 'https://api.bybit.com/v2/public/kline/list?symbol='+symbol+'&interval='+tick_interval+'&from='+str(start)
data = requests.get(url).json()
D = pd.DataFrame(data['result'])

HAdf = pd.DataFrame()
HAdf = D[['open', 'close', 'high', 'low']]
HAdf['close'] = round(((D['open'].astype(float) + D['high'].astype(float) + D['low'].astype(float) + D['close'].astype(float))/4),2)

for i in range(len(D)):
    if i == 0:
        HAdf.iloc[0,0] = round(((D['open'].astype(float).iloc[0] + D['close'].astype(float).iloc[0])/2),2)
    else:
        HAdf.iat[i,0] = round(((HAdf.astype(float).iat[i-1,0] + HAdf.astype(float).iat[i-1,3])/2),2)

HAdf['high'] = HAdf.loc[:,['open', 'close']].join(D['high']).astype(float).max(axis=1)
HAdf['low']  = HAdf.loc[:,['open', 'close']].join(D['low']).astype(float).min(axis=1)

# Heikin Ashi bars chart 
fig2 = go.Figure(data = [go.Candlestick(x = HAdf.index,
                open  = HAdf.open,
                high  = HAdf.high,
                low   = HAdf.low,
                close = HAdf.close)])

fig2.update_layout(
          title = 'Heikin Ashi Chart', 
          xaxis_title = 'Date', 
          yaxis_title = 'Price')

fig2.show()
