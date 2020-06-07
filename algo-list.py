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