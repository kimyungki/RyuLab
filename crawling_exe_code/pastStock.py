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
time=[]
stock=[]
trade=[]
while int(endDate) >= 20190118:
    str(endDate)
    # SetInputValue
    instStockChart.SetInputValue(0, "A000660")
    # instStockChart.SetInputValue(1, ord('2'))  # 개수로
    # instStockChart.SetInputValue(4, '6000') #개수
    instStockChart.SetInputValue(1, ord('1'))  # 날짜로
    instStockChart.SetInputValue(2, endDate)  # 종료일
    instStockChart.SetInputValue(3, '20190101')  # 시작일
    instStockChart.SetInputValue(5, (0, 1, 5, 8))
    instStockChart.SetInputValue(6, ord('m'))
    # 날짜 시간 종가 거래량

    # BlockRequest
    instStockChart.BlockRequest()

    # GetHeaderValue
    numData = instStockChart.GetHeaderValue(3)
    # numField = instStockChart.GetHeaderValue(1)
    endDate = instStockChart.GetDataValue(0, 4998) - 1
# GetDataValue
    for i in range(numData):
        date.append(instStockChart.GetDataValue(0, i))
        time.append(instStockChart.GetDataValue(1, i))
        trade.append(instStockChart.GetDataValue(3, i))
        stock.append(instStockChart.GetDataValue(2, i))

df = pd.DataFrame(columns= ['date', 'time', 'tradevolume', 'stock'])
df["date"] = date
df["time"] = time
df["stock"] = stock
df["tradevolume"] = trade
df = df.iloc[::-1]
df = df.reset_index(drop=True)

df.to_csv("C:/stock/A000660_past.csv", mode='w', header=True, index=False)

