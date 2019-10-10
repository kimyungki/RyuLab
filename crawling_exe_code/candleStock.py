import win32com.client
from pandas import Series, DataFrame
import pandas as pd
import csv
from datetime import datetime

# Create object
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")
yesterdayStock = int(datetime.today().strftime("%Y%m%d")) -1

endDate = yesterdayStock
date=[]
start=[]
high=[]
low=[]
end=[]


# SetInputValue
instStockChart.SetInputValue(0, "A000660")
# instStockChart.SetInputValue(1, ord('2'))  # 개수로
# instStockChart.SetInputValue(4, '6000') #개수
instStockChart.SetInputValue(1, ord('1'))  # 날자로
instStockChart.SetInputValue(2, endDate)  # 종료일
instStockChart.SetInputValue(3, '20190101')  # 시작일
instStockChart.SetInputValue(5, (0, 2, 3, 4, 5)) # 날짜/시가/고가/저가/종가
instStockChart.SetInputValue(6, ord('D'))
# 날짜 시간 종가 거래량

# BlockRequest
instStockChart.BlockRequest()

# GetHeaderValue
numData = instStockChart.GetHeaderValue(3)
# numField = instStockChart.GetHeaderValue(1)
endDate = instStockChart.GetDataValue(0, 0) - 1
# GetDataValue
for i in range(numData):
    date.append(instStockChart.GetDataValue(0, i))
    start.append(instStockChart.GetDataValue(1, i))
    high.append(instStockChart.GetDataValue(2, i))
    low.append(instStockChart.GetDataValue(3, i))
    end.append(instStockChart.GetDataValue(4, i))

df = pd.DataFrame(columns= ['date', 'start', 'high', 'low', 'end'])
df["date"] = date
df["start"] = start
df["high"] = high
df["low"] = low
df["end"] = end
df = df.iloc[::-1]
df = df.reset_index(drop=True)

df.to_csv("C:/stock/A000660_candle.csv", mode='w', header=True)

