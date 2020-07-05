import os

files = os.listdir('./raw-outputs/')

for f in files:
    if f[-3:] == 'csv':
        print(f)
        f2 = 'SHOP-'+f
        os.rename('raw-outputs/'+f, './raw-outputs/'+f2)

