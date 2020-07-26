import timeit 
import numpy as np
import matplotlib.pyplot as plt
import talib as ta
import nn_model

class Playground:
    def __init__(self,name):
        self.filename = name
        #open file
        f = open(self.filename,"r")
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
        self.buy_ys = []
        self.buy_xs = []
        self.sell_ys = []
        self.sell_xs = []
        self.pos_xs = []
        self.pos_ys = []
        self.neg_xs = []
        self.neg_ys = []
        self.goodentry_xs = []
        self.goodentry_ys = []
        self.saved_exits = []
        self.transactions = [] 
        self.arr_xs = np.arange(self.time_total)
        self.arr_ys = np.full(self.time_total,-1.)
        
        #populate models
        for i in range(self.time_total):
            self.arr_ys[i] = float(lines[i])
        
        nn_model.init()

    def buy(self, price, i):
        self.entry = price
        self.qty_stocks += 1
        self.transactions.append((price, i, -1, -1))
        if len(self.buy_xs) == len(self.sell_ys):
            self.buy_ys.append(price)
            self.buy_xs.append(i)
        else:
            raise Exception("Tried to buy when still have an open position.")
    

    def sell(self, price, i):    
        last = self.transactions[-1]
        if last[2] == -1 and last[3] == -1:
            self.transactions[-1] = (last[0], last[1], price, i) 
        else: 
            raise Exception("Tried to sell something that wasn't there.")

        if len(self.sell_xs) + 1 == len(self.buy_ys):
            self.sell_ys.append(price)
            self.sell_xs.append(i)
        else:
            raise Exception("Tried to buy when still have an open position.")
        self.profit += self.sell_ys[-1] - self.buy_ys[-1]
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
        # return nn_result[0][0]
        # return nn_result[0][0] >= .45 and ta.LINEARREG_SLOPE(data[-120:],120)[-1] > 0
        return nn_result[0][0] and ta.LINEARREG_SLOPE(data[-120:],120)[-1] > 0 

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

    # Main loop starts here
    def main_loop(self):
        counter = 0 
        # Start at 15 minutes
        for i in range(900, self.time_total):
            # Every 60 seconds
            if i % 5 == 0:
                direction_up = self.do_algo(self.arr_ys[i-900:i])
                if direction_up:
                    self.pos_xs.append(i)
                    self.pos_ys.append(self.arr_ys[i])
                    if ta.LINEARREG_SLOPE(self.arr_ys[i-5:i],5)[-1] > 0 :
                        self.goodentry_xs.append(i)
                        self.goodentry_ys.append(self.arr_ys[i])
                else:
                    self.neg_xs.append(i)
                    self.neg_ys.append(self.arr_ys[i])
                
            else:
                pass
            counter += 1



    # Get a List of tuples that have complete transaction data 
    # [(buy price, i , sell price, j)]
    def get_transactions(self):
        print("Num transactions: ", str(len(self.transactions))) 
        # print("Transactions: ", str(self.transactions)) 
        return self.transactions

    def show_plot(self):
        for t in self.transactions: 
            gain = t[2] - t[0]
            # self.profit += gain
            self.buy_xs.append(t[1])
            self.buy_ys.append(t[0])
            self.sell_xs.append(t[3])
            self.sell_ys.append(t[2])
        plt.plot(self.arr_xs, self.arr_ys)
        plt.plot(self.arr_xs, self.arr_ys, 'b.')
        plt.plot(self.neg_xs, self.neg_ys, 'ro')
        plt.plot(self.pos_xs, self.pos_ys, 'g^') 
        plt.plot(self.goodentry_xs, self.goodentry_ys, 'c^') 
        plt.show()

    # Get list of transaction tuples where price did increase by at least x in next 60 seconds
    def get_model_correct_preds(self):
        correct_preds = []
        for t in self.transactions: 
            x = t[1]
            y = t[0]
            rose20 = False
            for i in range(x,x+59):
                if  i < len(self.arr_ys) and self.arr_ys[i] >= y+.10:
                    rose20 = True
                    break
            if rose20:
                correct_preds.append(t)
        return correct_preds
            
    #return 
    def get_results(self):
        #tODO: return result dict here instead of testing suite
        parts = self.filename.split('-')
        output = {}
        output['symb'] = parts[0]
        output['date'] = parts[1]+'-'+parts[2]+'-'+parts[3]
        output['total_time'] = self.time_total
        output['profit'] = self.profit 
        output['transactions'] = self.transactions
        output['num_transactions'] = len(self.transactions)
        output['num_correct_preds'] = len(self.get_model_correct_preds())
        return output 

        return self.profit
