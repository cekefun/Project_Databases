from __future__ import unicode_literals

from django.db import models, connection



class Sensor:
	def __init__(self):
		self.ID = 0
		self.Apparature = ""
		self.InstalledOn = 0
		self.Active = "False"

	def __init__(self, databasetuple):
		self.ID = str(databasetuple[0])
		self.Apparature = str(databasetuple[1])
		self.InstalledOn = str(databasetuple[2])
		self.Active = "True"
		if (str(databasetuple[3]) == "0"):
			self.Active = "False"

	def __repr__(self): #used for testing
		returnstring = "ID: "
		returnstring += self.ID
		returnstring += " Apparature: "
		returnstring += self.Apparature
		returnstring += " InstalledOn: "
		returnstring += self.InstalledOn
		returnstring += " Active: "
		returnstring += self.Active
		return returnstring


class SensorDataSample:
	def __init__(self):
		self.CreationTimestamp = ""
		self.SensorID = 0
		self.Value = 0

	def __init__(self, databasetuple):
		self.CreationTimestamp = str(databasetuple[0])
		self.SensorID = str(databasetuple[1])
		self.Value = str(databasetuple[2])

class MinuteDataSample(SensorDataSample):
	pass
class HourDataSample(SensorDataSample):
	pass
class DayDataSample(SensorDataSample):
	pass
class MonthDataSample(SensorDataSample):
	pass
class YearDataSample(SensorDataSample):
	pass


class SensorData:
	''' Class which is used to perform querries on the sensors and store the results'''

	def __init__(self):
		self.results = []
		self.cursor = connection.cursor()

	def clean(self):
		self.results = []

	def getTuples(self):
		return self.results

	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from Sensor order by ID;")
		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(Sensor(i))

		return self.getTuples()

	def selectByHouseHoldID(self, householdid):
		self.clean()
		self.cursor.execute("select * from Sensor where InstalledOn = " + str(householdid) + " order by ID;")
		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(Sensor(i))

		return self.getTuples()


class MinuteData:
	''' Class which is used to display minute data from sensors'''

	def __init__(self):
		self.results = []
		self.cursor = connection.cursor()

	def clean(self):
		self.results = []

	def getTuples(self):
		return self.results

	def selectAll(self):
		self.clean()

		self.cursor.execute("select * from MinuteData order by CreationTimestamp;")
		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(MinuteDataSample(i))

		return self.getTuples()

	def selectBySensorID(self, sensorID):
		self.clean()

		self.cursor.execute("select * from MinuteData where SensorID = " + str(sensorID) + " order by CreationTimestamp;")
		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(MinuteDataSample(i))

		return self.getTuples()