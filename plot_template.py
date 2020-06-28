import matplotlib.pyplot as plt
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
f = open("raw-outputs/2020-03-24-raw-output.txt","r") 

#...initialize all values 
list_xs = []
list_ys = []
list_linreg_15 = []
time_total = 23000
#...load data for entire time series
lines = f.readlines()
for i in range(time_total):
    list_xs.append(i)
    list_ys.append(float(lines[i])) 

#put function to be tested here
list_linreg_15 = ta.LINEARREG_SLOPE(np.array(list_ys), 15)

#print(ta.LINEARREG_SLOPE(np.array(ys),300)[300])


#--------------------
print(type(list_ys))
plt.plot(list_xs, list_linreg_15)
plt.plot(list_xs, list_linreg_15, 'g^')


plt.ylabel('')
plt.xlabel('time')
plt.show() 