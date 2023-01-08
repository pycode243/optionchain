import requests
import pandas as pd
import time
import datetime
import os.path

today = pd.to_datetime('today').strftime("%d%m%y")
file_exists = os.path.exists("oc_"+today+".csv")
date = pd.to_datetime('today').strftime("%d/%m/%y  %H:%M:%M")
#now = pd.to_datetime('today').strftime("%H:%M:%M")
#start = pd.to_datetime('today').strftime("15:50:00")
#end = pd.to_datetime('today').strftime("15:59:00")

sym = "NIFTY"

def oc(sym):
    url = 'https://www.nseindia.com/api/option-chain-indices?symbol='+sym
    headers = {
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
                'accept-encoding' : 'gzip, deflate, br',
                'accept-language' : 'en-US,en;q=0.9'
                }
    session = requests.Session()
    data = session.get(url, headers=headers).json()['records']['data']

    ocdata = []
    for i in data:
        for j,k in i.items():
            if j == "CE" or j == "PE":
                try:
                    info = k
                    info["instrumentType"] = j
                    ocdata.append(info)
                except:
                    print("fatching data")
                    
        df = pd.DataFrame(ocdata)
        df.drop(['underlying','pchangeinOpenInterest','change','pChange','totalBuyQuantity','totalSellQuantity','bidQty','bidprice','askQty','askPrice','underlyingValue'],axis=1,inplace = True)
        df.insert(loc = 0,column = 'Date',value = date)
    return df
        
while True:
    try:
        if file_exists is False:
            data = oc(sym)
            data.to_csv("oc_"+today+".csv",mode='a',index=False,header=True)
            #print("data with headers")
            time.sleep(180)
        elif file_exists is True:
            data = oc(sym)
            data.to_csv("oc_"+today+".csv",mode='a',index=False,header=False)
            #print("data without headers")
            time.sleep(180)                
    except:
        #print("Retring")
        time.sleep(5)
        
 

            

              