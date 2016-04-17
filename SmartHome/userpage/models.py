from __future__ import unicode_literals

from django.db import models, connection
import json


def SQL_SensorDataByHouseholdID(tablename, householdID):
	command = "select " + str(tablename) + ".CreationTimestamp, "
	command += str(tablename) + ".SensorID, "
	command += str(tablename) + ".Value "
	command += "from " + str(tablename) + ", Sensor "
	command += "where Sensor.ID = " + str(tablename) + (".SensorID ")
	command += "AND Sensor.InstalledOn = " + str(householdID)
	command += " order by SensorID, CreationTimestamp;"

	return command


def SQL_SensorChangeAttribute(sensorID, attributename, value):
	command = "update Sensor "
	command += "set " + str(attributename) + "='" + str(value) + "' "
	command += "where Sensor.ID = " + str(sensorID) + ";"

	return command


def SQL_AddSensor(InstalledOn, Title, Apparature, Description, Unit):
	command = "insert into Sensor(ID, Active, InstalledOn, Title, Apparature, Description, Unit) values (0, 1, "
	command += InstalledOn + ", "
	command += "'" + Title + "', "
	command += "'" + Apparature + "', "
	command += "'" + Description + "', "
	command += "'" + Unit + "');"

	return command


def dictfetchall(cursor):
	"function that returns the results from an SQL query in dictionary format"
	desc = cursor.description
	return [
		dict(zip([col[0] for col in desc], row))
		for row in cursor.fetchall()
	]





def AddNewSensor(InstalledOn, Title, Apparature, Description, Unit):
	dbCursor = connection.cursor()
	dbCursor.execute(SQL_AddSensor(InstalledOn, Title, Apparature, Description, Unit))
	return True

class Sensor:
	def __init__(self):
		self.ID = 0
		self.Apparature = ""
		self.InstalledOn = 0
		self.Active = 0

	def __init__(self, databasetuple):
		self.ID = str(databasetuple[0])
		self.Apparature = str(databasetuple[1])
		self.InstalledOn = str(databasetuple[2])
		self.Active = databasetuple[3]

	def __repr__(self): #used for testing
		returnstring = "ID: "
		returnstring += self.ID
		returnstring += " Apparature: "
		returnstring += self.Apparature
		returnstring += " InstalledOn: "
		returnstring += self.InstalledOn
		returnstring += " Active: "
		returnstring += str(self.Active)
		return returnstring

	#more random testing
	def __iter__(self):
		yield('ID',self.ID)
		yield('Apparature',self.Apparature)
		yield('InstalledOn',self.InstalledOn)
		yield('Active',self.Active)


class SensorDataSample:
	def __init__(self):
		self.CreationTimestamp = ""
		self.SensorID = 0
		self.Value = 0

	def __init__(self, databasetuple):
		self.CreationTimestamp = str(databasetuple[0])
		self.SensorID = str(databasetuple[1])
		self.Value = str(databasetuple[2])

	def __iter__(self):
		yield('CreationTimestamp', self.CreationTimestamp)
		yield('SensorID', self.SensorID)
		yield('Value', self.Value)

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

	def updateAttribute(self, sensorID, Attribute, newValue):

		# print SQL_SensorChangeAttribute(sensorID, Attribute, newValue)
		self.cursor.execute(SQL_SensorChangeAttribute(sensorID, Attribute, newValue))

	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from Sensor order by Active DESC, Title;")

		self.results = dictfetchall(self.cursor)
		return self.getTuples()


	def selectByHouseHoldID(self, householdid):
		self.clean()
		self.cursor.execute("select * from Sensor where InstalledOn = " + str(householdid) + " order by ID;")
		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(Sensor(i))

		return self.getTuples()

	def toJSON(self):
		result = {}
		result["sensors"] = []
		for i in self.results:
			result["sensors"].append(dict(i))
		return json.dumps(result)



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

		self.cursor.execute("select * from MinuteData order by SensorID, CreationTimestamp;")
		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(MinuteDataSample(i))

		return self.getTuples()

	def selectByHouseholdID(self, householdID):
		self.clean()

		self.cursor.execute(SQL_SensorDataByHouseholdID("MinuteData", householdID))
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

	def toJSON(self):
		result = {}
		result["datasamples"] = []

		for i in self.results:
			result["datasamples"].append(dict(i))

		return json.dumps(result)



class HourData:
	def __init__(self):
		self.results = []
		self.cursor = connection.cursor()

	def clean(self):
		self.results = []

	def getTuples(self):
		return self.results

	def selectByHouseholdID(self, householdID):
		self.clean()
		self.cursor.execute(SQL_SensorDataByHouseholdID("HourData", householdID))

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(HourDataSample(i))

		return self.getTuples()


	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from HourData order by CreationTimestamp;")

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(HourDataSample(i))
		return self.getTuples()	

	def toJSON(self):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))

		return json.dumps(result)


class DayData:
	def __init__(self):
		self.results = []
		self.cursor = connection.cursor()

	def clean(self):
		self.results = []

	def getTuples(self):
		return self.results

	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from DayData order by CreationTimestamp;")

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(DayDataSample(i))
		return self.getTuples()

	def selectByHouseholdID(self, householdID):
		self.clean()
		self.cursor.execute(SQL_SensorDataByHouseholdID("DayData", householdID))

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(DayDataSample(i))

		return self.getTuples()

	def toJSON(self):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))

		return json.dumps(result)


class MonthData:
	def __init__(self):
		self.results = []
		self.cursor = connection.cursor()

	def clean(self):
		self.results = []

	def getTuples(self):
		return self.results

	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from MonthData order by CreationTimestamp;")

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(MonthDataSample(i))
		return self.getTuples()	

	def selectByHouseholdID(self, householdID):
		self.clean()
		self.cursor.execute(SQL_SensorDataByHouseholdID("MonthData", householdID))

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(MonthDataSample(i))

		return self.getTuples()

	def toJSON(self):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))

		return json.dumps(result)


class YearData:
	def __init__(self):
		self.results = []
		self.cursor = connection.cursor()

	def clean(self):
		self.results = []

	def getTuples(self):
		return self.results

	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from YearData order by CreationTimestamp;")

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(YearDataSample(i))
		return self.getTuples()	

	def selectByHouseholdID(self, householdID):
		self.clean()
		self.cursor.execute(SQL_SensorDataByHouseholdID("YearData", householdID))

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(YearDataSample(i))

		return self.getTuples()

	def toJSON(self):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))

		return json.dumps(result)