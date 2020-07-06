import os

files = os.listdir('./secdata/')

for f in files:
    if f[-3:] == 'txt':
        print(f)
        # f2 = 'MSFT-'+f
        f2 = f.replace('raw-output', 'secdata', 1)
        os.rename('secdata/'+f, 'secdata/'+f2)

