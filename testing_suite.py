import os 
import algo_playground as ap
import argparse

# grab args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "")
# parser.add_argument("-o", "--Output", help = "Show Output")
parser.add_argument('-a', '--all', action='store_true')
args = parser.parse_args()  


results = []
default_files = ["2020-03-24-raw-output.txt"]
files = os.listdir('./raw-outputs')
lines= []

m = ap.MyClass()

if args.all:
    pass
elif args.file:
    files = []
    files.append(args.file)
else:
    files = default_files

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

    # run mainloop on file
    print(filename[0:10])
    m.load_data(filename)
    m.main_loop()
    transactions = m.get_transactions()
    profit = m.get_results()
    output = {}
    output['date'] = filename[0:10]
    output['total_time'] = end_time
    output['profit'] = profit
    # output['transactions'] = transactions
    results.append(output)

# print(str(results))
#{
# Date:
# Output:
# Length of time: 
# Transactions: (price, i, price2, j)
#
#
#}  