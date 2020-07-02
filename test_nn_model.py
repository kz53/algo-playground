import nn_model
import numpy as np

h = np.array([15.0,14,13,12,11,10,9,8,7,6,5,4,3,2,1]) 
l = np.array([14.0,13,12,11,10,9,8,7,6,5,4,3,2,1,0]) 
c = np.array([14.0,13,12,11,10,9,8,7,6,5,4,3,2,1,0]) 

nn_model.init()
result = nn_model.get_pred(h,l,c)
print(type(result[0][0]))
print(result[0][0])