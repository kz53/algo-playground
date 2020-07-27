import tensorflow as tf
from tensorflow import keras
import numpy as np
import os

rng = np.random.default_rng()

raw=np.array([]).reshape((0,9))
np.set_printoptions(suppress=True, precision=3)
for filename in os.listdir("learning-data/MSFT"):
    arr=np.load('./learning-data/MSFT/'+filename)
    raw=np.concatenate((raw,arr))
    print(filename)

uniques=unique_rows = np.unique(raw, axis=0)
rng.shuffle(uniques,axis=0)
#labeled=uniques
labeled=np.delete(uniques,(7),1)


data=labeled[:,:-1]/100
cat=labeled[:,-1]
print(data[1,:])
print(np.sum(cat)/len(cat))
cat=cat.astype(int).reshape((-1,1))
test_num=-len(cat)//10
test_data=data[test_num:,:]
train_data=data[:test_num,:]
test_cat=cat[test_num:,:]
train_cat=cat[:test_num,:]

model=keras.Sequential([keras.layers.Dense(data.shape[1],input_shape=(data.shape[1],),activation='tanh'),
                        keras.layers.Dense(6, activation='elu'),
                        keras.layers.Dense(6, activation='elu'),
                        keras.layers.Dense(1,activation='sigmoid')])
opt=tf.keras.optimizers.Adam(learning_rate=.001)
model.compile(opt,loss=keras.losses.BinaryCrossentropy(),metrics=['accuracy'])
model.fit(train_data,train_cat, epochs=100, class_weight={0:1, 1:1})
model.evaluate(test_data,test_cat)

print("Finished L1")
# pred=model.predict(train_data)
# #test_loss,test_acc=model.evaluate(test_data,test_cat)
#
#
# #
# l2_data=np.array([]).reshape((0,10))
# l2_cat=np.array([]).reshape((0,1))
#
# for i in range(0,len(pred)):
#     if  pred[i]>.5:
#         l2_data=np.vstack((l2_data,train_data[i,:]))
#         l2_cat=np.vstack((l2_cat,train_cat[i,:]))
#
# model2=keras.Sequential([keras.layers.Dense(10, input_shape=(10,)),
#                         keras.layers.Dense(10,activation='selu'),
#                         keras.layers.Dense(10,activation='tanh'),
#                         keras.layers.Dense(1, activation='tanh')])
# opt2=tf.keras.optimizers.Adam(learning_rate=.0005)
# model2.compile(optimizer=opt2,loss=keras.losses.BinaryCrossentropy(),metrics=['accuracy'])
# model2.fit(l2_data,l2_cat,epochs=175,class_weight={0:1, 1:2})
#
# test_pred1=model.predict(test_data)
# test_pred2=model2.predict(test_data)
#
# print(np.sum(l2_cat)/len(l2_cat))

final_pred=np.rint(model.predict(test_data))

# for i in range(0,len(test_pred1)):
#     if(test_pred1[i]>=.5 and test_pred2[i]>=.5):
#         final_pred[i]=1
# #print(np.hstack((test_pred1,test_pred2,final_pred,test_cat)))
# # #
print("Positives:{:d}".format(np.sum(test_cat)))
print("Negatives:{:d}".format(len(final_pred)-np.sum(test_cat)))
print("Absolute Error: {:g}".format(np.sum(np.abs(final_pred-test_cat))))
print("Correct Positives: {:g}".format(np.sum(test_cat[(final_pred).nonzero()])))
print("Correct Negatives: {:g}".format(np.sum(1-test_cat[(final_pred==0).nonzero()])))
#
model.save("models/model1")
#model2.save("models/model2")
