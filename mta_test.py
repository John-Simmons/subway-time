import requests;
from google.transit import gtfs_realtime_pb2
from datetime import datetime
import warnings

def convert_time(posix_time):
    return datetime.utcfromtimestamp(posix_time).strftime('%Y-%m-%dT%H:%M:%SZ');

mta_feed = gtfs_realtime_pb2.FeedMessage();

mta_uri = "http://datamine.mta.info/mta_esi.php?key=91176d7a2718a1a8ea9f0f0ebf547425&feed_id=36";

mta_response = requests.get(mta_uri);

mta_feed.ParseFromString(mta_response.content);

mta_trains = {};

for entity in mta_feed.entity:
    #if entity.HasField('vehicle'):
        #if entity.vehicle.stop_id in ["M18", "M18S", "M18N"]:
            #mta_trains[entity.vehicle.trip.trip_id] = entity.vehicle;
            #print(convert_time(entity.vehicle.timestamp));
            #print(entity.vehicle);
    if entity.HasField('trip_update'):
        for stop in entity.trip_update.stop_time_update:
            if stop.stop_id in ["M18S", "M18N", "M18"]:
                print(stop);
    #else:
    #    print("Other");

    #print(mta_trains);
