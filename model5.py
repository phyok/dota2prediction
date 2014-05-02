training_data = open("trainingdata.txt")
games = []
for line in training_data:
    l = line.strip()
    games.append(l)
training_data.close()

# calculcate win rates

winRates = {}
for n in range(len(games)):
    line = games[n].split(",")
    game = line[0:10]
    result = int(line[10])
    for i in range(0,5):
        for j in range(5,10):
            pair1 = (game[i].lower(), game[j].lower())
            pair2 = (game[j].lower(), game[i].lower())
            if not winRates.has_key(pair1):
                winRates[pair1] = result
            else:
                winRates[pair1] += result
            if not winRates.has_key(pair2):
                winRates[pair2] = -result
            else:
                winRates[pair2] += -result

# do the prediction
inputSize = int(raw_intput())
inputLines = []
lineCount = 0
while(lineCount < inputSize):
    line = raw_input().split(",")
    inputLines.append(line)
    lineCount += 1

for line in inputLines:
    total = 0
    for i in range(0,5):
        for j in range(5,10):
            pair = (line[i].lower(), line[j].lower())
            total += winRates[pair]
    if total <= 0:
        print 1
    else:
        print 2

