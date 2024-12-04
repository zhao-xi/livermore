import datetime
import csv

reformatted_data = {}
class candle:
    def __init__(self, time, open, high, low, close, volume,index):
        self.time = time
        self.open = float(open)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)
        self.volume = float(volume)
        self.index = index
        self.reformatted_data = {}

    def get_rate(self):
        """
        :return: rate
        """
        return (self.close - self.open)/self.open

    def get_time_stamp(self):
        # convert self.time 2024-10-02T14:00:00+08:00 to unix timestamp
        dt = datetime.datetime.fromisoformat(self.time)
        return int(dt.timestamp())

    def is_hammer(self):
        low_range = self.high - (self.high - self.low)*0.2
        if self.open > low_range and self.close > low_range:
            return True
        return False


def get_data(path):
    """
    :param path: input file path
    :return: a list of dict, each dict is a row
    """
    data = []
    reformatted_data['Date'] = []
    reformatted_data['Open'] = []
    reformatted_data['High'] = []
    reformatted_data['Low'] = []
    reformatted_data['Close'] = []
    reformatted_data['Volume'] = []
    with open(path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        # skip the title row
        headers = next(csv_reader)
        i = 0
        for row in csv_reader:
            data.append(candle(*row, i))
            reformatted_data['Date'].append(datetime.datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
            reformatted_data['Open'].append(float(row[1]))
            reformatted_data['High'].append(float(row[2]))
            reformatted_data['Low'].append(float(row[3]))
            reformatted_data['Close'].append(float(row[4]))
            reformatted_data['Volume'].append(float(row[5]))
            i += 1
    return data
