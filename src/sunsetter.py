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
		# TODO: make sure to calclulate the NEXT sunset
		self.date = datetime.now(pytz.UTC)	# date to find sunrise/sunset for
		
		self._prime()

	def find_sunset_at_time(self, time=None):
		"""
		get the name of a major city where the sun is setting at a given time

		:param time: time of the sunset

		:return str: city name or None
		"""
		if not time:
			time = datetime.now(pytz.UTC)

		short_time = None
		short_cities = []
		for city, data in self.cities.iteritems():
			pass

		print short_cities
		print "in %s" % short_time
			

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
