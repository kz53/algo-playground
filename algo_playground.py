import timeit 
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
import nn_model

class Playground:
    def __init__(self,name):
        #open file
        f = open(name,"r")
        lines = f.readlines()
        #intialize config
        self.qty_stocks = 0
        self.time_interval = 15 
        self.time_total = self.get_valid_len(lines)
        self.time_start = 0
        #models
        self.entry = 0
        self.profit = 0
        self.buys = [] 
        self.exits = [] 
        self.buy_prices = []
        self.buy_times = []
        self.sell_prices = []
        self.sell_times = []
        self.saved_exits = []
        self.transactions = [] 
        self.arr_xs = np.arange(self.time_total)
        self.arr_ys = np.full(self.time_total,-1.)
        
        #populate models
        for i in range(self.time_total):
            self.arr_ys[i] = float(lines[i])
        
        nn_model.init()


    # def load_data(self, name):

    #     #open file
    #     f = open("secdata/"+name,"r")
    #     lines = f.readlines()

    #     # clear values
    #     self.buys = [] 
    #     self.exits = [] 
    #     self.buy_prices = []
    #     self.buy_times = []
    #     self.sell_prices = []
    #     self.sell_times = []
    #     self.qty_stocks = 0
    #     self.entry = 0
    #     self.profit = 0
    #     self.saved_exits = []
    #     self.time_interval = 15 
    #     self.time_total = self.get_valid_len(lines)
    #     self.time_start = 0
        
    #     #models
    #     self.transactions = [] 
    #     self.arr_xs = np.arange(self.time_total)
    #     self.arr_ys = np.full(self.time_total,-1.)
    #     self.data_buffer = np.full(1800,-1.)
    #     #populate models
    #     for i in range(self.time_total):
    #         self.arr_ys[i] = float(lines[i])

    def buy(self, price, i):
        self.entry = price
        self.qty_stocks += 1
        self.transactions.append((price, i, -1, -1))
        self.buy_prices.append(price)
        self.buy_times.append(i)

    def sell(self, price, i):    
        last = self.transactions[-1]
        if last[2] == -1 and last[3] == -1:
            self.transactions[-1] = (last[0], last[1], price, i) 
            self.sell_prices.append(price)
            self.sell_times.append(i)

        else: 
            raise Exception("Tried to sell something that wasn't there.")
        self.qty_stocks -= 1

    def get_valid_len(self, mylist):
        counter = 0
        for i in mylist:
            if i == -1:
                break
            counter += 1
        return counter 

    def do_algo(self, data, t=15): 
        # wrong - points = self.arr_ys[i-(t+2):i+1]
        #divide into 15 pieces
        minutes = []
        for i in range(15):
            minutes.append(data[i*60:(i+1)*60])

        highs = []
        lows = []
        closes = []
        for minute in minutes:
            highs.append(max(minute))
            lows.append(min(minute))
            closes.append(minute[-1])
        nn_result = nn_model.get_pred(np.array(highs), np.array(lows), np.array(closes))
        return nn_result[0][0]

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
        for i in range(900, self.time_total):
            if i % 60 == 0:
                direction_up = self.do_algo(self.arr_ys[i-900:i])
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
                if ta.MA(self.arr_ys[i-9:i+1],10)[-1] < self.entry  and self.qty_stocks != 0:
                    self.sell(self.arr_ys[i], i)
                if self.arr_ys[i] >= self.entry + .20 and self.qty_stocks != 0: 
                    self.sell(self.arr_ys[i], i)
        if self.qty_stocks != 0:
            self.sell(self.arr_ys[self.time_total-1], self.time_total-1)

    def get_transactions(self):
        print("Num transactions: ", str(len(self.transactions))) 
        # print("Transactions: ", str(self.transactions)) 
        return self.transactions

    def show_plot(self):
        #
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
        plt.plot(self.arr_xs, self.arr_ys)
        plt.plot(self.arr_xs, self.arr_ys, 'b.')
        plt.plot(sell_xs, sell_ys, 'ro')
        plt.plot(buy_xs, buy_ys, 'g^') 
        print("Profit: ", str(self.profit))
        print("----------------")
        return self.profit

# m = MyClass()
# m.load_data("MSFT-2020-03-27-secdata.txt")
# m.main_loop()
# m.get_transactions()
# m.show_results()