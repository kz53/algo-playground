import timeit 
import numpy as np
import matplotlib.pyplot as plt
import talib as ta

#intialize config
buys = [] 
qty_stocks = 0
entry = 0
exits = [] 
profit = 0
saved_exits = []
time_interval = 15 
time_total = 23500
time_start = 0

transactions = []
#load data
f = open("raw-outputs/raw-output-3-24-20.txt","r")
lines = f.readlines()

#create models
arr_xs = np.arange(23500)
arr_ys = np.full(23500,-1.)
for i in range(time_total):
     arr_ys[i] = float(lines[i])


def buy(price, i):
    global stocks
    global profits
    global transactions
    global entry
    global qty_stocks
    entry = price
    # profits -= x
    qty_stocks += 1
    transactions.append((price, i, -1, -1))

def sell(price, i):    
    global stocks
    global profits 
    global transactions
    global entry
    global qty_stocks
    last = transactions[-1]
    if last[2] == -1 and last[3] == -1:
        transactions[-1] = (last[0], last[1], price, i) 
    else: 
        raise Exception("Tried to sell something that wasn't there.")
    # profits += x
    qty_stocks -= 1

def sma(a, b):
    global nums
    return sum(nums[a:b+1])/(b-a)

def do_algo(i, t=15): 
    points = arr_ys[i-(t+2):i+1]
    slope = ta.LINEARREG_SLOPE(points,t)[-1]  
    slope_5 = ta.LINEARREG_SLOPE(points,5)[-1]
    # slope_prev = ta.LINEARREG_SLOPE(points,t)[-2]  
    # slope_prev_2 = ta.LINEARREG_SLOPE(points,t)[-3]  
    # print(str(slope_prev_2))
    if slope > 0 and slope_5 > 0: 
        return True
    else:
        return False

def cross_entry(i, t=15):
    points = arr_ys[i-(t+2):i+1]
    slope = ta.LINEARREG_SLOPE(points,t)[-1]  
    # slope_prev = ta.LINEARREG_SLOPE(points,t)[-2]  
    # slope_prev_2 = ta.LINEARREG_SLOPE(points,t)[-3]  
    # print(str(slope_prev_2))
    if slope > 0: 
        return True
    else:
        return False

# main loop starts here
for i in range(20, time_total):
    
    if i % 15 == 14:
        direction_up = do_algo(i)
        if qty_stocks ==   0:
            if direction_up: 
                buy(arr_ys[i], i)
            else:
                #HOLD
                pass
        elif qty_stocks == 1:
            if direction_up: 
                #HOLD 
                pass
            else:
                sell(arr_ys[i], i)
        else:
            raise Exception("You can't have something either than 1 or 0 stocks")
    else:
        if arr_ys[i] < entry and qty_stocks != 0:
            direction_up = cross_entry(i)
            if not direction_up:
                sell(arr_ys[i], i)
        if arr_ys[i] > entry + .15: 
            entry = arr_ys[i]

    # if i % time_interval == 0:
    #     if stocks == 1:        
    #         sell(nums[i])
    #     entry = nums[i]
    #     buy(nums[i]) 
    # elif:

    # elif i % 1  == 0 and nums[i] < entry and stocks == 1:
    #     sell(entry)
    #     saved = False
    #     for y in nums[i:i+45]:
    #         if y > entry:
    #             saved = True
    #         if saved:
    #             saved_exits.append(entry)
    #     saved = False 
        # exits.append([entry, nums[i], nums[i+1], nums[i+2],nums[i+3]])
        #sell(nums[i])

buy_xs = []
buy_ys = []
sell_xs = []
sell_ys = []

for t in transactions: 
    gain = t[2] - t[0]
    profit += gain
    buy_xs.append(t[1])
    buy_ys.append(t[0])
    sell_xs.append(t[3])
    sell_ys.append(t[2])

plt.plot(arr_xs, arr_ys)
plt.plot(arr_xs, arr_ys, 'b.')

plt.plot(sell_xs, sell_ys, 'ro')
plt.plot(buy_xs, buy_ys, 'g^') 

print("Transactions: ", str(transactions))
print("Profit: ", str(profit))
print("Num transactions: ", str(len(transactions)))
# print(exits)
# print(str(len(exits)))
# print(str(len(saved_exits)))
# print("Profit: " + str(profits))
plt.show()
print("finished")

