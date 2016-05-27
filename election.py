from stv import *
import csv
excel= []
with open('fruits.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        excel.append(row)

names = excel[0]
votes = excel[1:]
for i in range(len(votes)):
	votes[i] = [int(j) for j in votes[i]]

mt = election(len(names), len(votes), 3)
mt.load_votes(votes)
mt.load_candidates(names)
mt.run()
