class SubwayInfo(object):
    """docstring for ."""

    def __init__(self):
        self.lines = {
            "BDFM": "21",
            "JZ": "36",
            "ACE": "26",
            "123456": "1",
            "NQRW": "16"
        };

        self.stations = {
            "Essex": ["M18", "M18S", "M18N"]
        }

        self.stationLines = {
            "Essex": ["JZ", "BDFM"]
        };

    def getLineCode(self, line):
        return self.lines[line];

    def getLines(self):
        return self.lines.values();

    def getStationCodes(self, station):
        return self.stations[station];

    def getStationLines(self, station):
        return self.stationLines[station];
