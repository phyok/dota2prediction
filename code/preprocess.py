import numpy as np

# read in the lines
trainingdata = open("../matchdata.txt")
lines = []
for line in trainingdata:
    l = line.strip()
    lines.append(l)
trainingdata.close()

# create ids for players and heros
results = []
for l in lines:
    results.append(int(l[0]))

