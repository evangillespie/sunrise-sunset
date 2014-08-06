from .geocoder import FileGeocoder
from .enums import ALL_CITY_NAMES
from .time import SunTime
from datetime import date, datetime, timedelta
import pytz

class SunSetter(object):
	"""
	"""
	def __init__(self):
		super(SunSetter, self).__init__()

		self.geo = FileGeocoder()
		self.cities = dict()
		self.date = datetime.now(pytz.UTC)	# date to find sunrise/sunset for
		
		self._prime()

	def find_sunsets_at_time(self, interval, time=None):
		"""
		get the name of a major city where the sun is setting at a given time

		:param interval: maximum time difference in seconds from time.
		:param time: (SunTime) time of the sunset

		:return str: list of cities where sunset will happen in less than interval seconds from time
		"""
		if not time:
			time = self.get_current_time()

		short_cities = []
		for city, data in self.cities.iteritems():
			# TODO: compare all cities and find the next sunset
			# TODO: time the comparison. Do we need to be more clever than brute force?
			pass

		return short_cities
			
	def get_all_times(self):
		"""
		return all the sunset/sunrise times
		"""
		return self.cities

	def get_current_time(self):
		"""
		return the current time, as seen by this class
		"""
		return SunTime.get_suntime_from_time(datetime.now(pytz.UTC))

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
					s = c.sun(date=self.date, local=False)

					city_time_dict = {
						'sunrise': SunTime.get_suntime_from_time(s['sunrise']),
						'sunset': SunTime.get_suntime_from_time(s['sunset'])
					}

					self.cities[city] = city_time_dict

				except KeyError:
					print "NO - %s" % city
