# generic naive
def do_algo(i): 
    if (arr_ys[i]>entry): 
        return True
    else:
        return False

# linreg of [t-15:t]
def do_algo(i): 
    points = arr_ys[i-14:i+1]
    slope = ta.LINEARREG_SLOPE(points)  
    if (slope > 0): 
        return True
    else:
        return False

# if 15-sec slope and 5-sec slope both positives       
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