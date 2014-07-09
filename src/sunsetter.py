from .geocoder import FileGeocoder
from .enums import ALL_CITY_NAMES
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

	def find_sunset_at_time(self, time=None):
		"""
		get the name of a major city where the sun is setting at a given time

		:param time: time of the sunset

		:return str: city name or None
		"""
		if not time:
			time = datetime.now(pytz.UTC)

		short_time = None 	# 24 hour starting time
		short_cities = []
		for city, data in self.cities.iteritems():
			delt = data['sunset']-time
			if short_time == None:
				short_time = delt

			if delt < short_time:
				short_time = delt
				short_cities = [city]
			elif delt == short_time:
				short_cities.append(city)

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

					city_dict = {
						"sunset": s['sunset'],
						"sunrise": s['sunrise']
					}

					self.cities[city] = city_dict

				except KeyError:
					print "NO - %s" % city
