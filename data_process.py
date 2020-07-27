import csv
import os
import numpy as np
import talib as ta

for dirname in os.listdir("raw-outputs"):
    if os.path.isdir("raw-outputs/"+dirname):
        for filename in os.listdir("raw-outputs/"+dirname):
            if filename.endswith(".csv"):
                with open("./raw-outputs/"+dirname+'/'+filename, newline='') as csvfile:
                    reader=csv.DictReader(csvfile)
                    count=0
                    row_count=0
                    last_close=0
                    high=np.zeros(15)
                    low=np.zeros(15)
                    close=np.zeros(15)
                    cat=np.zeros(26)
                    new=np.zeros((26,10))
                    for row in reader:
                        try:
                            high[count]=float(row['marketHigh'])
                            low[count]=float(row['marketLow'])
                            close[count]=float(row['marketClose'])
                        except ValueError:
                            continue
                        if(count==0 and row_count>0 and high[count]>=last_close*1.0003):
                            cat[row_count-1]=1
                        count+=1
                        if count>=15:
                            new[row_count,0]=ta.NATR(high,low,close)[-1]
                            new[row_count,1]=ta.CCI(high,low,close)[-1]
                            new[row_count,2]=ta.CMO(close)[-1]
                            new[row_count,3]=ta.CORREL(high,low, timeperiod=14)[-1]*100
                            new[row_count,4]=ta.PLUS_DI(high,low,close)[-1]-ta.MINUS_DI(high,low,close)[-1]
                            new[row_count,5]=ta.MOM(close,timeperiod=14)[-1]
                            new[row_count,6]=ta.PLUS_DM(high,low)[-1]-ta.MINUS_DM(high,low)[-1]
                            new[row_count,7]=ta.RSI(close)[-1]
                            new[row_count,8]=ta.WILLR(high,low,close)[-1]
                            new[row_count,9]=ta.ROC(close,timeperiod=14)[-1]*100
                            count=0
                            last_close=close[-1]
                            high=np.zeros(15)
                            low=np.zeros(15)
                            close=np.zeros(15)
                            row_count+=1
                    cat=cat.reshape((len(cat),1))
                    final=np.hstack((new,cat))
                    print(filename)
                    if( not os.path.isdir('./learning-data/'+dirname)):
                        os.mkdir('./learning-data/'+dirname)
                    np.save('./learning-data/'+dirname+"/"+filename[:-4],final)
