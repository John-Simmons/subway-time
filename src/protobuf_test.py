import requests;
from google.transit import gtfs_realtime_pb2
from google.protobuf import text_format
from protobuf_to_dict import protobuf_to_dict
import nyct_subway_pb2 as nyct

apiURI = "http://datamine.mta.info/mta_esi.php?key="+"91176d7a2718a1a8ea9f0f0ebf547425"+"&feed_id=";

def station_time_lookup(train_data, station):
    """Takes MTA data as a dict and removes the trains not arriving at station
    Code found and adapted from https://github.com/neoterix/nyc-mta-arrival-notify

    Parameters:
    train_data (dict): MTA train data converted from GTFS real-time to a dict.
    station (list): A list of station codes.

    Returns:
    upcoming_trains (list): Each list item contains trip_id, route_id, and arrival_time(epoch)"""

    upcoming_trains = [];

    for trains in train_data: # trains are dictionaries
        if trains.get('trip_update', False) != False:

            unique_train_schedule = trains['trip_update']; # train_schedule is a dictionary with trip and stop_time_update

            if unique_train_schedule.get('stop_time_update', False) != False:
                unique_arrival_times = unique_train_schedule['stop_time_update']; # arrival_times is a list of arrivals

                for scheduled_arrivals in unique_arrival_times: #arrivals are dictionaries with time data and stop_ids
                    if scheduled_arrivals.get('stop_id', False) in station:

                        time_data = scheduled_arrivals['arrival'];
                        unique_time = time_data['time'];

                        if unique_time != None:
                            print(unique_train_schedule['trip']['___X']['1001']['train_id'][1])
                            upcoming_trains.append([unique_train_schedule['trip']['trip_id'],unique_train_schedule['trip']['route_id'], unique_time]);

    return upcoming_trains;

feed = gtfs_realtime_pb2.FeedMessage();
response = requests.get(apiURI+"36");
feed.ParseFromString(response.content);

#Convert MTA data to a dict
subway_feed = protobuf_to_dict(feed);
realtime_data = subway_feed['entity']

upcoming_trains = station_time_lookup(realtime_data, ["M18", "M18S", "M18N"]);

#print(upcoming_trains);
