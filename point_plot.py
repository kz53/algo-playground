import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
from talib import LINEARREG_SLOPE

#load data
f = open("raw-outputs/raw-output-3-24-20.txt","r")

#initialize all values 
ys = []
time = 0
xs = []
minute_xs = []
minute_ys = []
exit_xs= []
exit_ys = []
unsaved_exit_xs = []
unsaved_exit_ys = []
counter = 0 
entry = 0
stocks = 0
exits = []
time_interval = 15

#main loop
lines = f.readlines()
for p in lines[0:23000]:
    ys.append(float(p))
    xs.append(time)

    #every time
    if counter % time_interval == 0:
    	minute_ys.append(float(p))
    	minute_xs.append(time)
    	entry = float(p)
    	stocks = 1

    #every second
    elif counter % 1  == 0 and stocks == 1:
        #dips below entry
        if float(p) < entry:
            
            exit_ys.append(float(p))
            exit_xs.append(time)
            a = counter
            can_be_saved = False
            while(a%time_interval != 0):
                if float(lines[a]) >= entry:
                    can_be_saved = True
                a += 1
            if not can_be_saved and stocks == 1:
                unsaved_exit_ys.append(float(p))
                unsaved_exit_xs.append(time)
            stocks = 0
    #end loop
    time += 1
    counter += 1


plt.plot(xs, ys)
plt.plot(minute_xs, minute_ys,'ro')
plt.plot(exit_xs, exit_ys,'g^')
plt.plot(unsaved_exit_xs, unsaved_exit_ys,'y^')
print(str(len(exit_xs)))
print(str(len(unsaved_exit_xs)))
plt.ylabel('price')
plt.xlabel('time')
plt.show() 