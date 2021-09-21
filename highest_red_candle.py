import pandas as pd
import yfinance as yf
import datetime as dt



# Likelyhood of being profitable buying PUTS after a new 20D High is a red candle
# Gap Ups:Next day is gaps up 
# Gap Down:Next day is gaps down
# Next Day Red:Next day is a red candle
# D1 Low LT Low:Next days Low is lower than signal day low
# D1 High GT Close:Next days high is greater than close


dfdic={}
report=pd.DataFrame(columns=['Symbol','Gap_Ups','Gap_Down','Next_Day_Red','d1Low_LT_Low','d1High_GT_Close'])
 
#symbols
tickers=['AAPL','FB']

# #download data
downloads=yf.download(tickers,interval='1d')
data=downloads.stack().reset_index().rename(index=str, columns={"level_1": "Symbol"}).sort_values(['Symbol','Date'])


for ticker in tickers:
    df=data.loc[data['Symbol'] == ticker]
    
    df=df.copy()    
    
    #check if candle is red or green
    df['body']=df['Close']-df['Open'] 
    
    #next day gaps
    df['d1Gap']=df['Open'].shift(-1)-df['Close']
    
    #next day OHLC
    df['d1Open']=df['Open'].shift(-1)
    df['d1High']=df['High'].shift(-1)
    df['d1Low']=df['Low'].shift(-1)
    df['d1Close']=df['Close'].shift(-1)
    df['d1Body']=df['body'].shift(-1)
    
    #remove green candles
    df=df.loc[df['body'] < 0]
        
    #adding rolling high information
    df['rolling_high_20d']=df['High'].rolling(20).max()
    
    #scan criteria
    criteria=df.loc[df['rolling_high_20d']==df['High']]
    
    #next day gap up
    gapups=len(criteria.loc[criteria['d1Gap'] > 0])/len(criteria)
    gapdowns=len(criteria.loc[criteria['d1Gap'] < 0])/len(criteria)
    d1red=len(criteria.loc[criteria['d1Body'] < 0])/len(criteria)
    d1low_low=len(criteria.loc[criteria['d1Low'] < criteria['Low']])/len(criteria)
    d1high_close=len(criteria.loc[criteria['d1High'] > criteria['Close']])/len(criteria)
    
    
    row=[ticker,gapups,gapdowns,d1red,d1low_low,d1high_close]
    report.loc[len(report)] = row 
    
    
report=report.round(2)

#results:
# It's better to buy PUTS at open the next day as likelyhood of next day's
# high being greater than signal day close is > 80%

