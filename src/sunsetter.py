from astral import Astral
from .enums import CITY_NAMES
from datetime import date, datetime, timedelta
import pytz

class SunSetter(object):
	"""
	"""
	def __init__(self):
		super(SunSetter, self).__init__()

		self.a = Astral()
		self.cities = dict()
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

		for city, data in self.cities.iteritems():
			delt = time-data['sunset']

			print "%s: %s" % (city, delt.seconds)

	def _prime(self):
		"""
		read all the important data into memory
		"""
		self._get_cities()

	def _get_cities(self):
		for name, continent in CITY_NAMES.iteritems():	
			for city in continent:
				try:
					c = self.a[city]
					s = c.sun(date=self.date, local=False)

					city_dict = {
						# "city": c,
						# "sun": s,
						"sunset": s['sunset'],
						"sunrise": s['sunrise']
					}

					self.cities[city] = city_dict

				except KeyError:
					print "NO - %s" % city
