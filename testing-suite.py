import os 
results = []

files = os.listdir('./raw-outputs')
lines= []



# print(files)

for filename in files:
    f = open('./raw-outputs/'+filename, 'r')
    data  = []
    counter = 0
    end_time = len(f.readlines())

    for i in f.readlines():
        if(float(i)!=-1):  
            data.append(float(i))
        else:
            end_time = counter
            break
        counter+=1

#     run mainloop on file
    output = {}
    output['date'] = filename
    output['total_time'] = end_time
    # # output['profit'] = 
    # # output['transactions'] = 
    results.append(output)

print(str(results))
#{
# Date:
# Output:
# Length of time: 
# Transactions: (price, i, price2, j)
#
#
#}  