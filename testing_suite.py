import os 
import algo_playground as ap
import argparse


# If no file argument given, default to below symb and day
symb = 'SHOP'
folder = symb + '/'
directory = '../secdata/'
files = [f"{symb}-2020-07-13-secdata.txt"]
excluded_files = [f'{symb}-2020-07-10-secdata.txt']

#models
results = []
lines= [] # --delete

# Grab arguments
# -f (file), -a (all), none (default_files), -s (symbol)
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help = "")
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-s', '--symb', action='store_true')
parser.add_argument('-p', '--plot', action='store_true' )
parser.add_argument('-d', '--date' )

args = parser.parse_args()  

if args.symb:
    symb = args.symb
    folder = symb + '/'
    files = [f'{symb}-2020-03-24-secdata.txt']
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

    pg.main_loop()
    transactions = pg.get_transactions()
    output = pg.get_results()
    profit = pg.get_results()
    results.append(output)
    print(output['date'])
    print("Num Transactions: ", str(output['num_transactions']))

    #Get % of transactions that win
    num_win = 0
    for t in output['transactions']: 
        if t[2]-t[0] > 0:
            num_win += 1
    print("Pct win: " + str(num_win/output['num_transactions']))
    
    print("Profit: ", str(output['profit']))
    print("----------------")
    # print(output)
    if args.plot :
        pg.show_plot()

# Get total return across X days
total_sum = 0
for r in results:
    total_sum += r['profit']
print(f"Total profit across {len(results)} days: {total_sum}")

#------------------------------
# Code Library

# #Get % of transactions that win
# num_win = 0
# for t in output['transactions']: 
#     if t[2]-t[0] > 0:
#         num_win += 1
# print("Pct win: " + str(num_win/output['num_transactions']))

