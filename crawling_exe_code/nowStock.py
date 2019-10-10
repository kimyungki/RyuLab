import win32com.client
import time
import csv
import datetime
import pandas as pd

# 연결 여부 체크
objCpCybos = win32com.client.Dispatch("CpUtil.CpCybos")
bConnect = objCpCybos.IsConnect
if (bConnect == 0):
    print("PLUS가 정상적으로 연결되지 않음. ")
    exit()

# 현재가 객체 구하기
objStockMst2 = win32com.client.Dispatch("DsCbo1.StockMst2")
objStockMst2.SetInputValue(0, 'A000660')
objStockMst2.BlockRequest()
# 현재가 통신 및 통신 에러 처리
rqStatus2 = objStockMst2.GetDibStatus()

one_minute_later = ((datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%H%M'))

time=[]
trade=[]
stock=[]
pastTrade=[]
# 현재가 정보 조회
if (objStockMst2.GetDataValue(2, 0) >= int('0800')
        and rqStatus2 == 0):
    print("장이 열렸습니다")
    print("현재가 통신 OK")
    while True:
        nowTime = datetime.datetime.now().strftime('%H%M')
        if (nowTime == one_minute_later):
            for i in range(0, objStockMst2.GetHeaderValue(0)):
                pastTrade.append(objStockMst2.GetDataValue(11, i))
            objStockMst2.SetInputValue(0, 'A000660')
            objStockMst2.BlockRequest()
            print("데이터 받아온 시간 : ", nowTime)
            print(" 시간 , 거래량 , 현재가 ")
            time.append(nowTime)
            for i in range(0, objStockMst2.GetHeaderValue(0)):
                trade.append(objStockMst2.GetDataValue(11, i)- pastTrade[-1])  # 거래량
                stock.append(objStockMst2.GetDataValue(3, i))  # 현재가
                print(time, trade, stock)
                print()
                df = pd.DataFrame(columns=['time', 'tradevolume', 'stock'])
                df["time"] = time
                df["tradevolume"] = trade
                df["stock"] = stock
                df.to_csv("C:/stock/A000660_now.csv", mode='w', header=True, index=False)
            one_minute_later = (datetime.datetime.now() + datetime.timedelta(minutes=1)).strftime('%H%M')
else:
    print("장이 닫혔습니다")
    print(rqStatus2)
    exit()