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
f = open("../secdata/MSFT/MSFT-2020-03-25-secdata.txt","r") 

#...initialize all values 
list_xs = []
list_ys = []
list_linreg_15 = []

time_total = 23000

# counter = 0 
# entry = 0
# stocks = 0


#1. pick start time
#2. pick end time
#3. load data from file into lines[]
#4. loop through data time_total times and add point to correct lists
#5. plot(xs, all_lists)
#6. 11809 11823
#7. 12963 12989
#
#


#...load data for entire time series
lines = f.readlines()
for i in range(time_total):
    list_xs.append(i)
    list_ys.append(float(lines[i])) 



#print(ta.LINEARREG_SLOPE(np.array(ys),300)[300])


#--------------------
plt.plot(list_xs, list_ys)
plt.plot(list_xs, list_ys, 'b.')


plt.ylabel('price')
plt.xlabel('time')
plt.show() 