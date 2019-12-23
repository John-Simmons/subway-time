from src.mta_feed import MtaFeed
from src.trains import Trains

#Setup User Configurations
userConfig = open("userConfig.txt", "r").readlines()

for l in userConfig:
    if l.split(":")[0] == "API Key":
        apiKey = l.split(":")[1].strip();
    elif l.split(":")[0] == "Station":
        station = l.split(":")[1].strip();
    elif l.split(":")[0] == "Lines":
        ls = str(l.split(":")[1].strip());
        lines = [];
        for line in ls.split(","):
            lines.append(line.strip());

#Create new feed and trains
feed = MtaFeed(apiKey);
trains = Trains();

arrivals = [];

for line in lines:
    #get raw feed from MtaFeed object
    arrivals = feed.getArrivals(station, line);
    #update Trains object with feed from MTA
    trains.addTrains(arrivals);

print(station);

for train in trains.getTrains(6):
    if train[2] == 'N':
        print(train[1] + " North " + str(train[3]) + " min");
    elif train[2] == 'S':
        print(train[1] + " South " + str(train[3]) + " min");

## TODO:
## - Create a looping process
## - Add stations for direction??
