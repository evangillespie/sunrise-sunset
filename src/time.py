from datetime import date, datetime, timedelta
import pytz

class SunTime(object):
	"""
	class to deal with times as strings instead of time object
	"""

	def __init__(self, h, m, s):
		"""
		:param h: the hour in 24 hour format
		:param m: minutes past the hour
		:param s: seconds past the minute
		"""
		self.h = h
		self.m = m
		self.s = s

	@classmethod
	def get_suntime_from_time(cls, time):
		"""
		turn a time into a SunTime object

		:param time: time object to map

		:return SunTime: Suntime equivalent
		"""
		print "+++++++++++++++++"
		print time
		print time.__class__
		print "+++++++++++++++++"

	def get_time_difference(self, other_time):
		"""
		compare another SunTime object to self.

		:param other_time: Suntime Object to compare to this one

		:return int: seconds to other_time. negative return means that other_time is before self
		"""
		# TODO: create this method
		pass