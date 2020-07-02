import talib as ta
import numpy as np
import tensorflow as tf
import time

def init():
    global model1
    global model2
    model1=tf.keras.models.load_model("models/model1")
    model2=tf.keras.models.load_model("models/model2")


def get_pred(high,low,close):
    #NOTE TAKES 15 minutes worth of highs, lows and closes.
    new=np.zeros(10)
    t0=time.clock()
    new[0]=ta.PLUS_DM(high,low)[-1]
    new[1]=ta.CCI(high,low,close)[-1]
    new[2]=ta.CMO(close)[-1]
    new[3]=ta.DX(high,low,close)[-1]
    new[4]=ta.MINUS_DI(high,low,close)[-1]
    new[5]=ta.MOM(close,timeperiod=14)[-1]
    new[6]=ta.PLUS_DI(high,low,close)[-1]
    new[7]=ta.RSI(close)[-1]
    new[8]=ta.WILLR(high,low,close)[-1]
    new[9]=ta.ROC(close,timeperiod=14)[-1]*100
    t1=time.clock()
    #print("Formating time {}".format(t1-t0))
    new=(new/100).reshape((1,10))
    t0=time.clock()
    val1=model1(new)
    t1=time.clock()

    #print("Predict Time: {}".format(t1-t0))
    #val2=model2.predict(new)
    #print(val1,val2)

    return (val1>.5)# and (val2>.5)
