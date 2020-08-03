import talib as ta
import numpy as np
import tensorflow as tf


def init():
    global model1
    global down_model
    model1=tf.keras.models.load_model("models/model1")
    down_model=tf.keras.models.load_model("models/down_model")

def transform(high,low,close):
    new=np.zeros(7)
    new[0]=ta.NATR(high,low,close)[-1]*1000
    new[1]=ta.CCI(high,low,close)[-1]
    new[2]=ta.CMO(close)[-1]
    new[3]=ta.PLUS_DI(high,low,close)[-1]-ta.MINUS_DI(high,low,close)[-1]
    new[4]=ta.MOM(close,timeperiod=14)[-1]
    new[5]=ta.PLUS_DM(high,low)[-1]-ta.MINUS_DM(high,low)[-1]
    new[6]=ta.RSI(close)[-1]
    #new[8]=ta.WILLR(high,low,close)[-1]
    #new[9]=ta.ROC(close,timeperiod=14)[-1]*100
    return new/100



def get_pred(high,low,close):
    new=transform(high,low,close)
    val1=model1(new)
    val2=down_model(new)
    #=model2.predict(new)
    #print(val1,val2)

    return (val1>.5) , (val2>.5)

def batch_pred(high,low,close):
    batch=np.zeros((0,7))
    for i in range(900,len(close)):
        highmins = high[np.arange(i-900,i,60)]
        lowmins = low[np.arange(i-900,i,60)]
        closemins = close[np.arange(i-900,i,60)]
        new=transform(highmins,lowmins,closemins)
        batch=np.vstack((batch,new))
    preds=model1.predict(batch)
    preds_down=down_model.predict(batch)

    return(preds),(preds_down)
