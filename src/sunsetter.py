from .geocoder import FileGeocoder
from .enums import ALL_CITY_NAMES
from .suntime import SunTime
from datetime import date, datetime, timedelta
import pytz
from astral import AstralError
import random


class SunSetter(object):

    """
    """

    def __init__(self):
        super(SunSetter, self).__init__()

        self.geo = FileGeocoder()
        self.cities = dict()
        self.date = self.get_current_datetime()  # date to find sunrise/sunset for

        self._prime()

    def find_rise_or_set_at_time(self, interval, rise_or_set=None, time=None):
        """
        get the name of a major city where the sun is setting at a given time

        :param interval: maximum time difference in seconds from time.
        :param time: (SunTime) time of the sunset

        :return str: list of cities where sunset will happen in less than interval seconds from time
        """
        if not time:
            time = self.get_current_time()
        if not rise_or_set:
            raise Exception("need a rise_or_set")
        if rise_or_set != 'sunrise' and rise_or_set != 'sunset':
            raise Exception(
                "rise_or_set must be either 'sunrise' or 'sunset'")

        short_cities = []
        for city, data in self.cities.iteritems():
            diff = time.get_time_difference(data[rise_or_set])
            if diff <= interval and diff >= 0:
                short_cities.append(city)

        return short_cities


    def refresh_date(self, dt = None):
        """
        reset self.date to the current date and reprime

        :param dt: the new datetime (datetime.datetime). If None, use now.
        """
        if dt:
            self.date = dt
        else:
            self.date = self.get_current_datetime()
        self._prime()


    def get_all_times(self):
        """
        return all the sunset/sunrise times
        """
        return self.cities


    def get_all_city_names(self):
        """
        return a list of all cities
        """
        return self.cities.keys()


    @classmethod
    def get_current_time(cls):
        """
        return the current time, as seen by this class
        """
        return SunTime.get_suntime_from_time(cls.get_current_datetime())


    @classmethod
    def get_current_datetime(cls):
        """
        return the current datetime in UTC
        """
        return datetime.now(pytz.UTC)


    def _prime(self):
        """
        read all the important data into memory
        """
        self._get_cities()

    def _get_cities(self):
        for name, continent in ALL_CITY_NAMES.iteritems():
            for city in continent:
                try:
                    c = self.geo[city]
                    try:
                        s = c.sun(date=self.date, local=False)
                    except AstralError:
                        # sun doesn't rise or set in this location today. ignore.
                        continue

                    city_time_dict = {
                        'sunrise': SunTime.get_suntime_from_time(s['sunrise']),
                        'sunset': SunTime.get_suntime_from_time(s['sunset'])
                    }

                    self.cities[city] = city_time_dict

                except KeyError:
                    print "NO - %s" % city


    @classmethod
    def pick_one_city(cls, cities):
        """
        pick one city from the list or return None

        :param cities: list of cities to pick from

        :return: one city (string)
        """
        if cities:
            if 'Hagen' in cities:
                return 'Hagen'
            else:
                return random.choice(cities)
        else:
            return ''
