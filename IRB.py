#//inventory retracement candle detection//#
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import config
import time
import sys



ohlc = 'TEST.csv' #filename

def Analysis(file_name):
    c = 45/100
    riskratio = 1.5
    print('Analyzing...')
    df = pd.read_csv(file_name)
    print(df)
    df['a'] = abs(df.apply(lambda row: row.High - row.Low, axis=1))
    df['b'] = abs(df.apply(lambda row: row.Close - row.Open, axis=1))
    df['ca'] = df.apply(lambda row: row.a * c, axis = 1)
    df['rv'] = np.where(df['b'].values < df['ca'].values,1,0)
    df['x'] = df.apply(lambda row: row.Low + row.ca, axis = 1)
    df['y'] = df.apply(lambda row: row.High - row.ca, axis = 1)
    df['sl'] = np.where((df['High'].values>df['y'].values) & (df['Close'].values<df['y'].values) & (df['Open'].values<df['y'].values),1,0)
    df['ss'] = np.where((df['Low'].values<df['x'].values) & (df['Close'].values>df['x'].values) & (df['Open'].values>df['x'].values),1,0)
    # df['longlimit'] = np.where((df['sl'] > 0), df['High'].values,np.NaN)
    # df['longlimit'] = df['longlimit'].ffill()
    # df['longlimit'] = np.array(df['longlimit']).tolist()
    # df['shortlimit'] = np.where((df['ss'] > 0), df['Low'].values,np.NaN)
    # df['shortlimit'] = df['shortlimit'].ffill()
    # df['shortlimit'] = np.array(df['shortlimit']).tolist()
    # df['longstop'] = np.where((df['sl'] > 0), df['Low'].values,np.NaN)
    # df['longstop'] = df['longstop'].ffill()
    # df['longstop'] = np.array(df['longstop']).tolist()
    # df['shortstop'] = np.where((df['ss'] > 0), df['High'].values,np.NaN)
    # df['shortstop'] = df['shortstop'].ffill()
    # df['shortstop'] = np.array(df['shortstop']).tolist()
    # df['longtarget'] = df.apply(lambda row: abs((row.longstop / row.longlimit) - 1)*riskratio, axis=1)
    # df['longtarget'] = df.apply(lambda row: (row.longlimit * (row.longtarget + 1)), axis=1)
    # df['shorttarget'] = df.apply(lambda row: abs((row.shortstop / row.shortlimit) - 1)*riskratio, axis=1)
    # df['shorttarget'] = df.apply(lambda row: (row.shortlimit * (1 - row.shorttarget)), axis=1)
    # df['long'] = np.where((df['High'].values>df['longlimit'].values),'yes','no')
    # df['short'] = np.where((df['Low'].values<df['shortlimit'].values),'yes','no')
    return df

print(Analysis(ohlc))

def getSignals(df):
    Longs = []
    ExitLongs = []
    Shorts = []
    ExitShorts = []
    max_length = 11
    for i in range(len(df)):
        if 'yes' in df['long'].iloc[i] and 'no' in df['long'].iloc[i-1]:
            Longs.append(df.iloc[i].name)
            for j in range(1,max_length):
                if (df['High'].iloc[i+j] > df['longtarget'].iloc[i+j]) and (df['High'].iloc[i+j-1] < df['longtarget'].iloc[i+j-1])\
                 or (df['Low'].iloc[i+j] < df['longstop'].iloc[i+j]) and (df['Low'].iloc[i+j-1] < df['longstop'].iloc[i+j-1]):
                    ExitLongs.append(df.iloc[i].name)
                    break
                elif j == (max_length-1):
                    ExitLongs.append(df.iloc[i].name)
    for i in range(len(df)):
        if 'yes' in df['short'].iloc[i] and 'no' in df['short'].iloc[i-1]:
            Shorts.append(df.iloc[i].name)
            for j in range(1,max_length):
                if (df['Low'].iloc[i+j] < df['shorttarget'].iloc[i+j]) and (df['Low'].iloc[i+j-1] > df['shorttarget'].iloc[i+j-1])\
                 or (df['High'].iloc[i+j] > df['shortstop'].iloc[i+j]) and (df['High'].iloc[i+j-1] < df['shortstop'].iloc[i+j-1]):
                    ExitShorts.append(df.iloc[i].name)
                    break
                elif j == (max_length-1):
                    ExitShorts.append(df.iloc[i].name)
    return Longs,ExitLongs,Shorts,ExitShorts
# frame = analysis(ohlcv)
#longs,longexits,shorts,shortexits = getSignals(frame)
# print(longexits)

def profitCalc(frame):
    longs,longexits,shorts,shortexits = getSignals(frame)
    Profits = ((frame.loc[longexits].Open.values - frame.loc[longs].Open.values)/frame.loc[longs].Open.values)\
    + abs((frame.loc[shortexits].Open.values - frame.loc[shorts].Open.values)/frame.loc[shorts].Open.values)
    return Profits
