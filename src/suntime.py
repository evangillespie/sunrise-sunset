from datetime import date, datetime, timedelta


class SunTime(object):

    """
    class to deal with times as strings instead of time object
    """

    def __init__(self, time, **kwargs):
        """
        :param time: datetime.time object to use as our time
        """
        self.time = time

    def __repr__(self):
        return str(self.time)

    def __str__(self):
        return self.__repr__()

    @classmethod
    def get_suntime_from_time(cls, orig_datetime):
        """
        turn a time into a SunTime object

        :param orig_datetime: datetime.datetime object to map

        :return SunTime: Suntime equivalent
        """
        suntime = cls(time=orig_datetime.time())
        return suntime

    def get_time_difference(self, other_time):
        """
        compare another SunTime object to self.

        :param other_time: Suntime Object to compare to this one

        :return int: seconds to other_time. negative return means that other_time is before self
        """
        # XXX: HACK! maybe do this properly
        diff_h = other_time.time.hour - self.time.hour
        diff_m = other_time.time.minute - self.time.minute
        diff_s = other_time.time.second - self.time.second
        seconds_to_other_time = diff_h*60*60 + diff_m*60 + diff_s

        return seconds_to_other_time


    def increment_time(self, increment):
        """
        increment the time in self by increment

        :param increment: the amount to increase time by in seconds
        """
        self.time = (datetime.combine(date(1, 1, 1), self.time) + timedelta(seconds=increment)).time()
