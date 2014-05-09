import numpy as np
import csv

# read in the lines
training_data = open('../../dota2_scrapers/datdota_matches.csv')
lines = []
for line in training_data:
    l = line.strip()
    lines.append(l)
training_data.close()
del lines[0]    #remove the csv title line


# create ids for players and heros
match_heros = []
match_players = []
results = []
hero_id_map = {}
player_id_map = {}
hero_id = 0
player_id = 0

for n in range(len(lines)):
    game = lines[n].split(",")
    heros = game[9:14]+game[19:24]
    players = game[4:9]+game[14:19]
    if heros[0] != '':
        match_players.append(players)
        match_heros.append(heros)
        results.append(int(game[3]))
    for h in heros:
        if not hero_id_map.has_key(h):
            if h != '':
                hero_id_map[h] = hero_id
                hero_id += 1

    for p in players:
        if not player_id_map.has_key(p):
            if p != '':
                player_id_map[p] = player_id
                player_id += 1
            
NUM_OF_HEROS = len(hero_id_map)
NUM_OF_PLAYERS = len(player_id_map)
FEATURE_SET_SIZE = 2 * (NUM_OF_HEROS + NUM_OF_PLAYERS)
DATA_SIZE = len(match_heros)

# save the mappings
w = csv.writer(open("../hero_map.csv", "w"))
for key, val in hero_id_map.items():
    w.writerow([key, val])

w2 = csv.writer(open("../player_map.csv", "w"))
for key, val in player_id_map.items():
    w2.writerow([key, val])

# preprocess the labels
y = np.array(results, dtype = np.int8)

# preprocess the data
X = np.zeros((DATA_SIZE, FEATURE_SET_SIZE), dtype = np.int8)

for row in range(DATA_SIZE):
    heros = match_heros[row]
    players = match_players[row]
    for i in range(10):
        hindex = hero_id_map[heros[i]]
        if i >= 5:
            hindex += NUM_OF_HEROS
        X[row,hindex] = 10
        
        if players[i] == '':
            continue
        pindex = 2*NUM_OF_HEROS+player_id_map[players[i]]
        if i >= 5:
            pindex += NUM_OF_PLAYERS
        X[row,pindex] = 1

outfile = open("../trainingdata.npz", 'w+')
np.savez(outfile, X=X, y=y)
outfile.close()
