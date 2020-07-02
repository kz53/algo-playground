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
values_to_plot = []
vtp_xs = []
time_total = 23000
#...load data for entire time series
lines = f.readlines()
for i in range(time_total):
    list_xs.append(i)
    list_ys.append(float(lines[i])) 


#START ****************************************

#function to be tested here
#--------------------
hit20 = False
minute_start = list_ys[0]
for i in range(len(list_ys)):
    if i %60 == 23:
        if hit20:
            values_to_plot.append(list_ys[i])
            vtp_xs.append(i)
        hit20 = False
        minute_start = list_ys[i]
    else:
        if list_ys[i] >= minute_start +.20:
            hit20 = True

#--------------------


#graph data points here
#--------------------
plt.plot(list_xs, list_ys)

plt.plot(vtp_xs, values_to_plot, 'g^')
#--------------------

#print results here
#--------------------
print('# hit20\'s: '+str(len(values_to_plot)))
#--------------------

#END ****************************************


plt.ylabel('price')
plt.xlabel('time')
plt.show() 