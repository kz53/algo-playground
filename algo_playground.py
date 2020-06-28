import timeit 
import numpy as np
import matplotlib.pyplot as plt
import talib as ta

class Playground:
    def __init__(self):
        #intialize config

        self.qty_stocks = 0


        self.time_interval = 15 
        self.time_total = 23500
        self.time_start = 0
        #models
        self.entry = 0
        self.profit = 0
        self.buys = [] 
        self.exits = [] 
        self.saved_exits = []
        self.transactions = [] 
        self.arr_xs = np.arange(23500)
        self.arr_ys = np.full(23500,-1.)


    def load_data(self, name):
        #open file
        f = open("raw-outputs/"+name,"r")
        lines = f.readlines()

        # clear values
        self.buys = [] 
        self.exits = [] 
        self.qty_stocks = 0
        self.entry = 0
        self.profit = 0
        self.saved_exits = []
        self.time_interval = 15 
        self.time_total = len(lines)
        self.time_start = 0
        
        #models
        self.transactions = [] 
        self.arr_xs = np.arange(self.time_total)
        self.arr_ys = np.full(self.time_total,-1.)

        #populate models
        for i in range(self.time_total):
            self.arr_ys[i] = float(lines[i])

    def buy(self, price, i):
        self.entry = price
        self.qty_stocks += 1
        self.transactions.append((price, i, -1, -1))

    def sell(self, price, i):    
        last = self.transactions[-1]
        if last[2] == -1 and last[3] == -1:
            self.transactions[-1] = (last[0], last[1], price, i) 
        else: 
            raise Exception("Tried to sell something that wasn't there.")
        self.qty_stocks -= 1

    # def sma(a, b):
    #     global nums
    #     return sum(nums[a:b+1])/(b-a)

    def do_algo(self, i, t=15): 
        points = self.arr_ys[i-(t+2):i+1]
        slope = ta.LINEARREG_SLOPE(points,t)[-1]  
        slope_5 = ta.LINEARREG_SLOPE(points,5)[-1]
        # slope_prev = ta.LINEARREG_SLOPE(points,t)[-2]  
        # slope_prev_2 = ta.LINEARREG_SLOPE(points,t)[-3]  
        # print(str(slope_prev_2))
        if slope > 0 and slope_5 > 0: 
            return True
        else:
            return False

    def cross_entry(self, i, t=15):
        points = self.arr_ys[i-(t+2):i+1]
        slope = ta.LINEARREG_SLOPE(points,t)[-1]  
        # slope_prev = ta.LINEARREG_SLOPE(points,t)[-2]  
        # slope_prev_2 = ta.LINEARREG_SLOPE(points,t)[-3]  
        # print(str(slope_prev_2))
        if slope > 0: 
            return True
        else:
            return False

    # main loop starts here
    def main_loop(self):
        for i in range(20, self.time_total):
            if i % 15 == 14:
                direction_up = self.do_algo(i)
                if self.qty_stocks == 0:
                    if direction_up: 
                        self.buy(self.arr_ys[i], i)
                    else:
                        #HOLD
                        pass
                elif self.qty_stocks == 1:
                    if direction_up: 
                        #HOLD 
                        pass
                    else:
                        self.sell(self.arr_ys[i], i)
                else:
                    raise Exception("You can't have something either than 1 or 0 stocks")
            else:
                if self.arr_ys[i] < self.entry and self.qty_stocks != 0:
                    direction_up = self.cross_entry(i)
                    if not direction_up:
                        self.sell(self.arr_ys[i], i)
                if self.arr_ys[i] > self.entry + .15: 
                    self.entry = self.arr_ys[i]

    def get_transactions(self):
        print("Num transactions: ", str(len(self.transactions))) 
        # print("Transactions: ", str(self.transactions)) 
        return self.transactions

    def show_plot(self):
        plt.plot(self.arr_xs, self.arr_ys)
        plt.plot(self.arr_xs, self.arr_ys, 'b.')
        plt.show()

    def get_results(self):
        buy_xs = []
        buy_ys = []
        sell_xs = []
        sell_ys = []

        for t in self.transactions: 
            gain = t[2] - t[0]
            self.profit += gain
            buy_xs.append(t[1])
            buy_ys.append(t[0])
            sell_xs.append(t[3])
            sell_ys.append(t[2])

        plt.plot(sell_xs, sell_ys, 'ro')
        plt.plot(buy_xs, buy_ys, 'g^') 
        print("Profit: ", str(self.profit))
        print("----------------")
        return self.profit

print("ok, starting\n")
# m = MyClass()
# m.load_data("2020-03-27-raw-output.txt")
# m.main_loop()
# m.get_transactions()
# m.show_results()

# m.load_data("2020-03-25-raw-output.txt")
# m.main_loop()
# m.get_transactions()
# m.show_results()
# m.show_plot()