from time import time;

class Trains(object):
    """Trains is an object meant to take in list of train data and manage/return it in a clean fashion"""

    def __init__(self, trainList = []):
        self.trains = trainList;

    def addTrains(self, trainList):
        """Takes a list of train data and updates repeated entries and adds new entries

        Parameters:
        trainList (list): Each list item should contain a Trip ID(string), a Route ID(string), and an Arrival Time(epoch)

        Returns:
        trains (list): An updated list containing a super set of trainList"""

        #update self.trains
        self.trains += (trainList);

        return self.trains

    def clearTrains(self):
        """Clears the train list"""

        self.trains = [];

    def getTrains(self, n):
        """Gets the closest n trains"""

        #ensure we dont select for more trains than we have
        if n > len(self.trains):
            n = len(self.trains);

        #sort trains by arrvial time
        sortedTrains = sorted(self.trains, key=lambda x: x[2]);
        trains = [];

        #pull the closest n trains with arrival times greater than 0 minutes
        i = 0;
        while len(trains) < n:
            if self.__getMinutes(int(sortedTrains[i][2])) > 0:
                trains.append([sortedTrains[i][0], sortedTrains[i][1], sortedTrains[i][0][-1], self.__getMinutes(int(sortedTrains[i][2]))]);

            i+=1;

        return trains;

    def __getMinutes(self, posix_time):
        """Returns the number of minutes between posix_time and the current time.

        Parameters:
        posix_time (int): Time in unix time."""
        minutes = round((posix_time - round(time()))/60);

        if minutes < 0:
            return 0;

        return minutes;
