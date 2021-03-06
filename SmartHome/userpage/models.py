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

	command = ("""insert into Sensor(ID, Active, InstalledOn, Title, Apparature, Description, Unit) values (0, 1, %i, "%s", "%s", "%s", "%s");""" % (InstalledOn, Title, Apparature, Description, Unit))
	return command

def SQL_DeleteSensor(SensorID):
	command = ("""delete from Sensor where Sensor.ID='%s' """ % (SensorID))
	return command


def SQL_SelectHouseHoldPrice(UserID):
	command = ("""select Address.StreetName as Streetname, Address.StreetNumber as Streetnumber, Address.City as City, Address.PostalCode as Postalcode, Address.Country as Country, House.PricePerUnit as Price, House.ID as ID from Address, House where House.AddressID = Address.ID and House.OwnedBy=%i; """ % (UserID))
	return command


def SQL_SelectCurrentMinuteData(houseID):
	command = (""" select MinuteData.CreationTimestamp as CreationTimestamp, MinuteData.SensorID as SensorID, MinuteData.Value as Value from MinuteData, Sensor where Sensor.InstalledOn=%i and Sensor.ID = MinuteData.SensorID and (MinuteData.CreationTimestamp between timestamp(makedate(year(now()), dayofyear(now())), maketime(hour(now()), minute(now()), 0)) and timestamp(makedate(year(now()), dayofyear(now())), maketime(hour(now()), minute(now()), 59)) ); """ % (houseID))
	return command

def SQL_SelectCurrentHourData(houseID):
	command = (""" select HourData.CreationTimestamp as CreationTimestamp, HourData.SensorID as SensorID, HourData.Value as Value from HourData, Sensor where Sensor.InstalledOn=%i and Sensor.ID = HourData.SensorID and (HourData.CreationTimestamp = date_sub(timestamp(makedate(year(now()), dayofyear(now())), maketime(hour(now()), 0,0)), interval 1 hour)) order by SensorID;   """ % (houseID))
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


def DeleteSensor(SensorID):
	dbCursor = connection.cursor()
	dbCursor.execute(SQL_DeleteSensor(SensorID))
	return True

def updatePriceByHouseholdID(HouseID, Price):
	dbCursor = connection.cursor()
	dbCursor.execute(("""update House set PricePerUnit=%f where ID=%i """ % (Price, HouseID)))


def getFirstHouseID(UserID):
	dbCursor = connection.cursor()
	dbCursor.execute("select House.ID from House where OwnedBy=%i" % (int(UserID)))
	result = dbCursor.fetchone()

	return int(result[0])


def addComment(SensorID, Message):
	dbCursor = connection.cursor()
	dbCursor.execute("""insert into Comment values (0,"%s",%i);""" % (str(Message), int(SensorID)))


def getAddressObj(householdID):
	dbCursor = connection.cursor()
	dbCursor.execute(""" select Address.StreetName as StreetName, Address.StreetNumber as StreetNumber, Address.City as City, Address.Country as Country from Address inner join House on House.AddressID = Address.ID where House.ID = %i; """ % householdID)
	result = dictfetchall(dbCursor)
	return Address(result[0])

class Address:
	def __init__(self, dictObj):
		self.StreetName = dictObj["StreetName"]
		self.StreetNumber = dictObj["StreetNumber"]
		self.City = dictObj["City"]
		self.Country = dictObj["Country"]



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

		if (Attribute == "Title"):
			self.cursor.execute("""select * from Sensor where Title='%s' and InstalledOn=(select InstalledOn from Sensor where ID=%s); """ % (newValue, sensorID))
			result = self.cursor.fetchone()
			if (result != None): #this means that there is already an entry with the same title in the same household
				return False


		self.cursor.execute(SQL_SensorChangeAttribute(sensorID, Attribute, newValue))
		return True

	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from Sensor order by Active DESC, Title;")

		self.results = dictfetchall(self.cursor)
		return self.getTuples()


	def selectByHouseHoldID(self, householdid):
		self.clean()
		self.cursor.execute("select * from Sensor where InstalledOn = " + str(householdid) + " order by Active DESC, Title;")
		# rows = self.cursor.fetchall()
		# for i in rows:
		# 	self.results.append(Sensor(i))
		self.results = dictfetchall(self.cursor)
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

		command = """ select distinct MinuteData.CreationTimestamp, MinuteData.SensorID, MinuteData.Value from MinuteData inner join Sensor on MinuteData.SensorID=Sensor.ID where (MinuteData.CreationTimestamp between date_sub(now(), interval 2 hour) and now()) and Sensor.InstalledOn = %i order by MinuteData.SensorID, MinuteData.CreationTimestamp; """ % (householdID)

		self.cursor.execute(command)
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

	def toJSON(self, householdID):
		result = {}
		result["datasamples"] = []

		for i in self.results:
			result["datasamples"].append(dict(i))

		result["firstTimestamp"] =  str(currentTimeStamp().timestampFirstMinute()["firstTimestamp"])
		result["pricePerUnit"] = str(houseHold(householdID).getPrice())

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
		command = """ select distinct HourData.CreationTimestamp, HourData.SensorID, HourData.Value from HourData inner join Sensor on HourData.SensorID = Sensor.ID where HourData.CreationTimestamp between date_sub(now(), interval 2 day) and now() and Sensor.InstalledOn=%i order by HourData.SensorID, HourData.CreationTimestamp; """ % (householdID)
		self.cursor.execute(command)
		self.results = dictfetchall(self.cursor)

		return self.getTuples()


	def selectAll(self):
		self.clean()
		self.cursor.execute("select * from HourData order by CreationTimestamp;")

		self.results = dictfetchall(self.cursor)
		return self.getTuples()	

	def toJSON(self, householdID):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			datasample = {}
			datasample["CreationTimestamp"] = str(i["CreationTimestamp"])
			datasample["SensorID"] = i["SensorID"]
			datasample["Value"] = i["Value"]

			result["datasamples"].append(datasample)

		if (len(self.results) != 0):
			result["firstTimestamp"] =  str(currentTimeStamp().timestampFirstHour()["firstTimestamp"])
		result["pricePerUnit"] = str(houseHold(householdID).getPrice())
		
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
		command = """ select distinct DayData.CreationTimestamp as CreationTimestamp, DayData.SensorID as SensorID, DayData.Value as Value from DayData inner join Sensor on Sensor.ID = DayData.SensorID where Sensor.InstalledOn = %i order by SensorID, CreationTimestamp;""" % householdID
		self.cursor.execute(command)

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(DayDataSample(i))
		return self.getTuples()

	def toJSON(self, householdID):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))
		result["firstTimestamp"] = str(currentTimeStamp().timestampFirstDay()["firstTimestamp"])
		result["pricePerUnit"] = str(houseHold(householdID).getPrice())
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
		command = """ select distinct MonthData.CreationTimestamp as CreationTimestamp, MonthData.SensorID as SensorID, MonthData.Value as Value from MonthData inner join Sensor on Sensor.ID = MonthData.SensorID where Sensor.InstalledOn = %i order by SensorID, CreationTimestamp;""" % householdID
		self.cursor.execute(command)

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(MonthDataSample(i))

		return self.getTuples()

	def toJSON(self, householdID):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))
		result["firstTimestamp"] = str(currentTimeStamp().timestampFirstMonth()["firstTimestamp"])
		result["pricePerUnit"] = str(houseHold(householdID).getPrice())
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
		command = """ select distinct YearData.CreationTimestamp as CreationTimestamp, YearData.SensorID as SensorID, YearData.Value as Value from YearData inner join Sensor on Sensor.ID = YearData.SensorID where Sensor.InstalledOn = %i order by SensorID, CreationTimestamp;""" % householdID
		self.cursor.execute(command)

		rows = self.cursor.fetchall()
		for i in rows:
			self.results.append(YearDataSample(i))

		return self.getTuples()

	def toJSON(self, householdID):
		result = {}
		result['datasamples'] = []

		for i in self.results:
			result["datasamples"].append(dict(i))
		result["firstTimestamp"] = str(currentTimeStamp().timestampFirstYear()["firstTimestamp"])
		result["pricePerUnit"] = str(houseHold(householdID).getPrice())
		return json.dumps(result)

class WeekData:
	def __init__(self):
		self.cursor = connection.cursor()
		self.results = []

	def selectByHouseholdIDTotal(self, householdid):
		command = """ select WeekData.CreationTimestamp as CreationTimestamp, Sum(WeekData.Value) as Total from WeekData inner join Sensor on Sensor.ID = WeekData.SensorID and Sensor.InstalledOn=%i and WeekData.CreationTimestamp != timestamp(makedate(year(now()), dayofyear(now())), maketime(0,0,0)) group by WeekData.CreationTimestamp order by WeekData.CreationTimestamp; """ % householdid
		self.cursor.execute(command)
		self.results = dictfetchall(self.cursor)

	def toJSON(self):
		resultingJSON = {}

		resultingJSON["datasamples"] = []

		for i in self.results:
			datasample = {}
			datasample["CreationTimestamp"] = str(i["CreationTimestamp"])
			datasample["Total"] = i["Total"]
			resultingJSON["datasamples"].append(datasample)

		return json.dumps(resultingJSON)


class SensorTitle:
	def __init__(self, houseID):
		self.houseID = int(houseID)
		self.cursor = connection.cursor()
		self.results = []

	def getTuples(self):
		return self.results

	def toJSON(self):
		result = {}
		result["sensors"] = []
		for i in self.results:
			result["sensors"].append(dict(i))
		return json.dumps(result)

	def selectByHousehold(self):
		self.cursor.execute("""select Sensor.ID as SensorID, Sensor.Title as Title from Sensor where InstalledOn=%i order by Sensor.ID""" % (self.houseID))
		self.results = dictfetchall(self.cursor)


	def getCurrentSensorTitlesJSON(self):
		self.selectByHousehold()
		return self.toJSON()


class NewHouse:
	def __init__(self, form, UserID):
		self.Streetname = form.cleaned_data['Streetname']
		self.Streetnumber = form.cleaned_data['Streetnumber']
		self.City = form.cleaned_data['City']
		self.Postalcode = form.cleaned_data['Postalcode']
		self.Country = form.cleaned_data['Country']
		self.Price = form.cleaned_data['Price']
		self.cursor = connection.cursor()
		self.UserID = UserID

	def isFirst(self):
		self.cursor.execute("select * from House where OwnedBy=%i" % (self.UserID))
		results = self.cursor.fetchone()
		if (results == None):
			return True
		return False


	def addToDatabase(self):
		newAddressID = self.addAddress()
		self.addHouse(newAddressID)

	def addAddress(self):
		'''this method will not add a new address if it is already added in the database'''

		if (self.alreadyExists() == False):
			self.cursor.execute(("""insert into Address values (0, "%s", %i, "%s","%s",%i);""" % (self.Streetname, self.Streetnumber, self.City, self.Country, self.Postalcode)))
	
		self.cursor.execute((""" select ID from Address where StreetName="%s" and StreetNumber=%i and City="%s" and Country="%s" and PostalCode=%i;""" % (self.Streetname, self.Streetnumber, self.City, self.Country, self.Postalcode)))
		result = self.cursor.fetchone()
		return int(result[0])

	def addHouse(self,AddressID):
		self.cursor.execute(("""insert into House values (0,%i, %f, %i); """ % (AddressID, self.Price, self.UserID)))

	def alreadyExists(self):
		self.cursor.execute((""" select * from Address where StreetName="%s" and StreetNumber=%i and City="%s" and Country="%s" and PostalCode=%i;""" % (self.Streetname, self.Streetnumber, self.City, self.Country, self.Postalcode)))
		if (self.cursor.fetchone() != None):
			return True
		return False



class HouseHoldsPrice:
	def __init__(self, UserID, currentHouseID):
		self.UserID = UserID
		self.cursor = connection.cursor()
		self.results = []
		self.currentHouseID = int(currentHouseID)

	def selectUserHouses(self):
		self.cursor.execute(SQL_SelectHouseHoldPrice(self.UserID))
		self.results = dictfetchall(self.cursor)

	def toJSON(self):
		result = {}
		result["houses"] = []
		for i in self.results:
			dataToAdd = dict(i)
			if (dataToAdd["ID"] == self.currentHouseID):
				dataToAdd["CurrentlyActive"] = 1
			else:
				dataToAdd["CurrentlyActive"] = 0
			result["houses"].append(dataToAdd)
		return json.dumps(result)

	def getHousesJSON(self):
		self.selectUserHouses()
		return self.toJSON()


class CommentsFromSensor:
	def __init__(self, sensorID):
		self.SensorID = int(sensorID)
		self.cursor = connection.cursor()
		self.results = []

	def selectComments(self):
		self.cursor.execute("select Comment.Message from Comment where SensorID=%i" % (self.SensorID))
		self.results = dictfetchall(self.cursor)

	def toJSON(self):
		result = {}
		result["comments"] = []
		for i in self.results:
			result["comments"].append(dict(i))
		return json.dumps(result)

	def getCommentsJSON(self):
		self.selectComments()
		return self.toJSON()



class currentTimeStamp:
	def __init__(self):
		self.cursor = connection.cursor()

	def timestampFirstMinute(self):
		self.cursor.execute("select timestamp(date_sub(makedate(year(now()), dayofyear(now())), interval 2 hour), date_add(maketime(hour(now()), minute(now()), 0), interval 1 minute)) as firstTimestamp;")
		resultTime = dictfetchall(self.cursor)
		return resultTime[0]

	def timestampFirstHour(self):
		self.cursor.execute("select timestamp(date_sub(makedate(year(now()), dayofyear(now())), interval 2 day), date_add(maketime(hour(now()), 0, 0), interval 1 hour)) as firstTimestamp;")
		resultTime = dictfetchall(self.cursor)
		return resultTime[0]

	def timestampFirstDay(self):
		self.cursor.execute("select timestamp(date_sub(date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 year), maketime(0, 0, 0)) as firstTimestamp;")
		resultTime = dictfetchall(self.cursor)
		return resultTime[0]

	def timestampFirstMonth(self):
		self.cursor.execute("select timestamp(date_sub(makedate(year(now()), 1), interval 10 year), maketime(0, 0, 0)) as firstTimestamp;")
		resultTime = dictfetchall(self.cursor)
		return resultTime[0]

	def timestampFirstYear(self):
		self.cursor.execute("select timestamp(date_sub(makedate(year(now()), 1), interval 100 year), maketime(0, 0, 0)) as firstTimestamp;")
		resultTime = dictfetchall(self.cursor)
		return resultTime[0]



class houseHold:
	def __init__(self, householdID):
		self.ID = householdID
		self.cursor = connection.cursor()

	def getPrice(self):
		self.cursor.execute("select PricePerUnit from House where ID=%i" % (self.ID))
		resultPrice = dictfetchall(self.cursor)
		return resultPrice[0]["PricePerUnit"]



class currentMinuteUsage:
	def __init__(self, householdID):
		self.householdID = householdID
		self.cursor = connection.cursor()


	def getSamples(self):
		self.cursor.execute(SQL_SelectCurrentMinuteData(self.householdID))
		results = dictfetchall(self.cursor)

		total = 0
		resultingJSON = {}
		resultingJSON["datasamples"] = []
		for i in results:
			datasample = {}
			datasample["CreationTimestamp"] = i["CreationTimestamp"].isoformat()
			datasample["SensorID"] = i["SensorID"]
			datasample["Value"] = i["Value"]
			resultingJSON["datasamples"].append(datasample)
			total += float(i["Value"])

		resultingJSON["Total"] = total

		self.cursor.execute(""" SELECT PeakValue FROM PeakCrashes INNER JOIN Crashes ON PeakCrashes.CrashID = Crashes.ID WHERE Crashes.HouseID = %i ORDER BY CrashDate DESC LIMIT 1;  """ % self.householdID)
		result = dictfetchall(self.cursor)
		if (len(result) == 0):
			resultingJSON["Dangerzone"] = 0
		else:
			resultingJSON["Dangerzone"] = result[0]["PeakValue"]


		self.cursor.execute(""" select CrashData.Mean as Mean, CrashData.Deviation as Deviation from CrashData where HouseID=%i; """ % self.householdID)
		result = dictfetchall(self.cursor)
		if (len(result) == 0):
			resultingJSON["Mean"] = 0
			resultingJSON["Deviation"] = 0
		else:
			resultingJSON["Mean"] = result[0]["Mean"]
			resultingJSON["Deviation"] = result[0]["Deviation"]


		return json.dumps(resultingJSON)


class lastHourUsage:
	def __init__(self, householdID):
		self.householdID = householdID
		self.cursor = connection.cursor()


	def getSamples(self):
		self.cursor.execute(SQL_SelectCurrentHourData(self.householdID))
		results = dictfetchall(self.cursor)

		total = 0
		resultingJSON = {}
		resultingJSON["datasamples"] = []
		for i in results:
			datasample = {}
			datasample["CreationTimestamp"] = i["CreationTimestamp"].isoformat()
			datasample["SensorID"] = i["SensorID"]
			datasample["Value"] = i["Value"]
			resultingJSON["datasamples"].append(datasample)
			total += float(i["Value"])

		resultingJSON["Total"] = total
		return json.dumps(resultingJSON)


class partialHour:
	def __init__(self, householdID):
		self.householdID = householdID
		self.cursor = connection.cursor()

	def getSamples(self):
		command = """ select * from currentHourData order by SensorID; """
		self.cursor.execute(command)

		results = dictfetchall(self.cursor)

		resultingJSON = {}
		if (results == None):
			return resultingJSON
		
		total = 0
		resultingJSON["Timestamp"] = str(results[0]["CreationTimestamp"])
		resultingJSON["datasamples"] = []
		for i in results:
			datasample = {}
			datasample["SensorID"] = i["SensorID"]
			datasample["Value"] = i["Value"]
			total += float(i["Value"])
			resultingJSON["datasamples"].append(datasample)

		resultingJSON["Total"] = total
		return json.dumps(resultingJSON)


class HighMinuteUsage:
	def __init__(self, householdid):
		self.cursor = connection.cursor()
		self.highUsageSensors = []
		self.lowUsageSensors = []
		self.Total = 0
		self.HouseholdID = householdid

	def getData(self):
		self.cursor.execute(""" select Sensor.Title as Title, MinuteData.Value as Value from Sensor inner join MinuteData on Sensor.ID = MinuteData.SensorID where Sensor.InstalledOn = %i and MinuteData.CreationTimestamp = date_sub(now(), interval second(now()) second) order by MinuteData.Value DESC; """ % self.HouseholdID)
		return dictfetchall(self.cursor)

	def getJSON(self):
		allData = self.getData()
		
		for i in allData:
			self.Total += float(i["Value"])


		#sensors get classified as high or low here, could be changed to be more complex
		tempValue = 0
		for i in allData:
			if (tempValue >= self.Total / 3):
				self.lowUsageSensors.append(i)
			else:
				self.highUsageSensors.append(i)
				tempValue += float(i["Value"])

		return self.toJSON()


	def toJSON(self):
		resultingJSON = {}
		resultingJSON["highSensors"] = self.highUsageSensors
		resultingJSON["lowSensors"] = self.lowUsageSensors
		resultingJSON["Total"] = self.Total

		return json.dumps(resultingJSON)



class Status:
	def __init__(self, householdid):
		self.cursor = connection.cursor()
		self.HouseholdID = householdid


	def getJSON(self):
		resultingJSON = {}

		self.cursor.execute(""" SELECT StreetName,StreetNumber,City,Country FROM Address INNER JOIN House ON Address.ID = House.AddressID WHERE StreetName IN (SELECT StreetName FROM Address INNER JOIN House ON Address.ID = House.AddressID WHERE House.ID = %i) AND House.ID NOT IN (SELECT ID FROM House WHERE 0 != (SELECT SUM(Value) FROM MinuteData INNER JOIN Sensor ON MinuteData.SensorID = Sensor.ID WHERE MinuteData.CreationTimestamp = date_sub(NOW(), interval second(now()) second) AND House.ID = Sensor.InstalledOn)); """ % self.HouseholdID)
		resultNeighbour = dictfetchall(self.cursor)

		self.cursor.execute(""" select Sum(MinuteData.Value) from MinuteData inner join Sensor on Sensor.ID = MinuteData.SensorID where CreationTimestamp = date_sub(now(), interval second(now()) second) and Sensor.InstalledOn=%i group by MinuteData.CreationTimestamp; """ % self.HouseholdID)
		resultTemp = self.cursor.fetchone()
		resultCurrentSum = 0.0
		if (resultTemp != None):
			resultCurrentSum = float(resultTemp[0])

		self.cursor.execute(""" SELECT PeakValue FROM PeakCrashes INNER JOIN Crashes ON PeakCrashes.CrashID = Crashes.ID WHERE Crashes.HouseID = %i ORDER BY CrashDate DESC LIMIT 1; """ % self.HouseholdID)
		resultTemp = self.cursor.fetchone()
		resultPeakValue = (resultCurrentSum * 2) + 1
		if (resultTemp != None):
			resultPeakValue = float(resultTemp[0])


		
		
		if (len(resultNeighbour) >= 3):
			resultingJSON["status"] = "OutageNeighbourhood"
			resultingJSON["houses"] = []
			for i in resultNeighbour:
				house = {}
				house["StreetName"] = i["StreetName"]
				house["StreetNumber"] = i["StreetNumber"]
				house["City"] = i["City"]
				house["Country"] = i["Country"]
				resultingJSON.append(house)

		elif (resultPeakValue * 9 / 10 <= resultCurrentSum):
			resultingJSON["status"] = "HighUsage"
		else:
			resultingJSON["status"] = "Normal"
		
		return json.dumps(resultingJSON)


class HistoricCrashes:
	def __init__(self, householdID):
		self.cursor = connection.cursor()
		self.resultsPeakValues = []
		self.resultsNeighbourhoodValues = []
		self.HouseholdID = householdID

	def getPeakValues(self):
		command = """ SELECT PeakCrashes.PeakValue as PeakValue, PeakCrashes.FirstValue as SensorValue1, PeakCrashes.SecondValue as SensorValue2, PeakCrashes.ThirdValue as SensorValue3,Sensor1.Title as SensorTitle1,Sensor2.Title as SensorTitle2,Sensor3.Title as SensorTitle3,Crashes.CrashDate as Timestamp FROM PeakCrashes INNER JOIN Crashes ON PeakCrashes.CrashID = Crashes.ID INNER JOIN Sensor AS Sensor1 ON PeakCrashes.FirstSensor = Sensor1.ID INNER JOIN Sensor AS Sensor2 ON PeakCrashes.SecondSensor = Sensor2.ID INNER JOIN Sensor AS Sensor3 ON PeakCrashes.ThirdSensor = Sensor3.ID WHERE Crashes.HouseID = %i ORDER BY Crashes.CrashDate DESC LIMIT 10; """ % self.HouseholdID
		self.cursor.execute(command)
		self.resultsPeakValues = dictfetchall(self.cursor)

	def getNeighbourhoodValues(self):
		command = """ SELECT Address.StreetName as StreetName,Address.City as City,Address.Country as Country,Crashes.CrashDate as Timestamp FROM StreetCrashes JOIN Crashes ON StreetCrashes.CrashID = Crashes.ID JOIN House ON Crashes.HouseID = House.ID JOIN Address ON House.AddressID = Address.ID WHERE House.ID = %i ORDER BY Crashes.CrashDate DESC LIMIT 10; """ % self.HouseholdID
		self.cursor.execute(command)
		self.resultsNeighbourhoodValues = dictfetchall(self.cursor)


	def getNeighbourhoodObjects(self):
		class NeighbourhoodObject:
			def __init__(self, dictObject):
				self.StreetName = dictObject["StreetName"]
				self.City = dictObject["City"]
				self.Country = dictObject["Country"]
				self.Timestamp = dictObject["Timestamp"]

		results = []
		for i in self.resultsNeighbourhoodValues:
			results.append(NeighbourhoodObject(i))
		return results



	def getPeakValueObjects(self):
		class PeakValueObject:
			def __init__(self, dictObject):
				self.PeakValue = dictObject["PeakValue"]
				self.SensorTitle1 = dictObject["SensorTitle1"]
				self.SensorTitle2 = dictObject["SensorTitle2"]
				self.SensorTitle3 = dictObject["SensorTitle3"]
				self.SensorValue1 = dictObject["SensorValue1"]
				self.SensorValue2 = dictObject["SensorValue2"]
				self.SensorValue3 = dictObject["SensorValue3"]
				self.Timestamp = dictObject["Timestamp"]

		result = []
		for i in self.resultsPeakValues:
			result.append(PeakValueObject(i))
		return result

	def getData(self):
		self.getPeakValues()
		self.getNeighbourhoodValues()
