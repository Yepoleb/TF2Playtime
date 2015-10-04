import json
import os

INPUT = "stats/{}.json"
PLAYTIME_STAT = "{}.accum.iPlayTime"
CLASSES = ["Scout", "Soldier", "Pyro", "Demoman", "Heavy", "Engineer", "Medic", "Sniper", "Spy"]

classtime = {}
for tfclass in CLASSES:
    classtime[tfclass] = 0

players = 0
for filename in os.listdir("stats/"):
    print(filename)
    path = "stats/" + filename
    statsdata = json.load(open(path, "r"))
    if "playerstats" not in statsdata:
        print("No data in", filename)
        continue
    if "stats" not in statsdata["playerstats"]:
        print("Player does not play the game", filename)
        continue
    tfstats = statsdata["playerstats"]["stats"]
    players += 1
    prettystats = {}
    for item in tfstats:
        name = item["name"]
        value = item["value"]
        prettystats[name] = value
    for tfclass in CLASSES:
        statskey = PLAYTIME_STAT.format(tfclass)
        if statskey not in prettystats:
            print(filename, "did not play", tfclass)
            continue
        classtime[tfclass] += prettystats[statskey]

print()
for tfclass in CLASSES:
    print(tfclass, round(classtime[tfclass] / 3600 / players, 2))
