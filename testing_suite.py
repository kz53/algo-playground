import os 
import algo_playground as ap
import argparse



symb = 'TSLA'
folder = symb + '/'
directory = '../secdata/'
files = [f"{symb}-2020-03-24-secdata.txt"]
excluded_files = [f'{symb}-2020-07-10-secdata.txt']

#models
results = []
lines= []

# Grab arguments
# -f (file), -a (all), none (default_files), -s (symbol)
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "")
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-s', '--symb')
args = parser.parse_args()  


if args.symb:
    symb = args.symb
    folder = symb + '/'
    directory = '../secdata/'
    files = [f"{symb}-2020-03-24-secdata.txt"]
    excluded_files = [f'{symb}-2020-07-10-secdata.txt']

# Handle args
if args.all:
    files = os.listdir(directory+folder)
    for x in excluded_files:
        files.remove(x)
elif args.file:
    files = []
    files.append(args.file)
else:
    pass


for filename in files:
    pg = ap.Playground(directory+folder+filename)
    # run mainloop on file
    print(filename[0:15])
    pg.main_loop()
    transactions = pg.get_transactions()
    profit = pg.get_results()
    output = {}
    output['date'] = filename[5:15]
    output['total_time'] = pg.time_total
    output['profit'] = profit
    # output['transactions'] = transactions
    results.append(output)

# Get total return across X days
total_sum = 0
for r in results:
    total_sum += r['profit']
print(f"Total profit across {len(results)} days: {total_sum}")
# print(str(results))


# m.show_plot()

# Output format
#{
# Date:
# Output:
# Length of time: 
# Numtransactinos: 
# Transactions: (price, i, price2, j)
#
#
#}  