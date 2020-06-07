import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
import talib as ta
import numpy as np

def abline(slope, intercept, a, b):
    """Plot a line from slope and intercept"""
    # axes = plt.gca()
    print(slope)
    print(intercept)
    x_vals = np.array(list_xs[ a: b])
    y_vals = intercept + slope * (x_vals-a)
    plt.plot(x_vals, y_vals, '--')
    # print(x_vals)




#load data
f = open("raw-outputs/raw-output-3-24-20.txt","r") 

#...initialize all values 
list_xs = []
list_ys = []
list_linreg_15 = []

start = 1199
end = start+15
time_total = 23000

# counter = 0 
# entry = 0
# stocks = 0


#1. pick start time
#2. pick end time
#3. load data from file into lines[]
#4. loop through data time_total times and add point to correct lists
#5. plot(xs, all_lists)
#6. 
#7. 
#
#


#...load data for entire time series
lines = f.readlines()
for i in range(time_total):
    list_xs.append(i)
    list_ys.append(float(lines[i])) 

list_linreg_15 = ta.LINEARREG_SLOPE(np.array(list_ys), 15)


#print(ta.LINEARREG_SLOPE(np.array(ys),300)[300])

myslope = ta.LINEARREG_SLOPE(np.array(list_ys[start:end]), (end-start) )[-1]
myint = ta.LINEARREG_INTERCEPT(np.array(list_ys[start:end]), (end-start) )[-1]


#--------------------
# plt.plot(list_xs, list_ys)
# plt.plot(list_xs, list_ys, 'b.')

plt.plot(list_xs, list_linreg_15)
plt.plot(list_xs, list_linreg_15, 'g^')
abline(0, 0, 0, time_total) 


# abline(myslope, myint, start, end)

plt.ylabel('price')
plt.xlabel('time')
plt.show() 