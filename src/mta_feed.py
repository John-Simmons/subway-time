import requests;
from google.transit import gtfs_realtime_pb2
from google.protobuf import text_format
from system_config.subway_info import SubwayInfo
from protobuf_to_dict import protobuf_to_dict
import src.nyct_subway_pb2 as nyct

class MtaFeed(object):
    """MtaFeed is an object meant to handle pulling subway data from the MTA GTFS real-time api"""

    def __init__(self, apiKey):
        self.apiURI = "http://datamine.mta.info/mta_esi.php?key="+apiKey+"&feed_id=";
        self.subwayInfo = SubwayInfo();

    def getArrivals(self, station, line):
        """Returns a list containing trains on a subway line approaching a station.
        Each list item contains a list of the Trip ID(String), the Subway Line(String), and the estimated Arrival Time(Epoch Time)

        Parameters:
        station (string): Name of the subway station.
        line (string): Name of the subway line"""

        #Retreive the station and line codes for the parameters given
        stationCodes = self.subwayInfo.getStationCodes(station);
        lineCode = self.subwayInfo.getLineCode(line);

        #Get raw data from the MTA API
        feed = gtfs_realtime_pb2.FeedMessage();
        response = requests.get(self.apiURI+lineCode);
        feed.ParseFromString(response.content);

        #Convert MTA data to a dict
        subway_feed = protobuf_to_dict(feed);
        realtime_data = subway_feed['entity']

        #Check MTA data for trains that will arrive at station
        upcoming_trains = self.__station_time_lookup(realtime_data, stationCodes);

        return upcoming_trains


    def __station_time_lookup(self, train_data, station):
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
                                upcoming_trains.append([unique_train_schedule['trip']['trip_id'],unique_train_schedule['trip']['___X']['1001']['train_id'][1], unique_time]);

        return upcoming_trains;
