import os 
import algo_playground as ap
import argparse

# grab args
# -f (file), -a (all), none (default_files)
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "")
parser.add_argument('-a', '--all', action='store_true')
args = parser.parse_args()  

#config
files = ["MSFT-2020-03-24-secdata.txt"]
folder = 'MSFT/'

#models
results = []
lines= []

m = ap.Playground()

if args.all:
    files = os.listdir('./secdata/'+folder)
elif args.file:
    files = []
    files.append(args.file)
else:
    pass

for filename in files:
    f = open('./secdata/'+folder+filename, 'r')
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

    # run mainloop on file
    # print(filename[0:10])
    m.load_data(folder+filename)
    m.main_loop()
    transactions = m.get_transactions()
    profit = m.get_results()
    output = {}
    output['date'] = filename[5:15]
    output['total_time'] = end_time
    output['profit'] = profit
    # output['transactions'] = transactions
    results.append(output)

print(str(results))

# trans_list = m.get_transactions()
# for item in trans_list:
#     subprofit = item[2] - item[0]
#     if subprofit < 0:
#         print(str(item) + ", " + str(subprofit))


# m.show_plot()


#{
# Date:
# Output:
# Length of time: 
# Transactions: (price, i, price2, j)
#
#
#}  