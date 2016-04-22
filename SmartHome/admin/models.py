from __future__ import unicode_literals

from django.db import models, connection

import json

# Create your models here.
class ValidLogin:
    def __init__(self):
        self.cursor = connection.cursor()
        self.username = ""

    def isValid(self, username, password):
        """ Return true if the username and the password match """

        self.username = str(username)
        self.cursor.execute("select * from User where UserName = %s and Password = %s and ID in (SELECT ID FROM Admin)",[self.username, password])
        results = self.cursor.fetchone()
        if (results == None):
            return False
        
        return True

    def getUserID(self):
        self.cursor.execute("select User.ID from User where UserName = %s", [self.username])
        result = self.cursor.fetchone()
        return int(result[0])

    def hasHouse(self):
        userID = self.getUserID()
        self.cursor.execute("select House.ID from House where OwnedBy=%s", [str(userID)])
        result = self.cursor.fetchone()

        if (result != None):
            return True
        else:
            return False


    def getFirstHouseID(self):
        userID = self.getUserID()
        self.cursor.execute("select House.ID from House where House.OwnedBy=%s", [str(userID)])
        result = self.cursor.fetchone()

        return int(result[0])


class AdminAgg:
    def __init__(self):
        self.cursor = connection.cursor()
        self.results = []

    def search(self,Table,Startmoment,EndMoment,Adress,Adrname):
        self.cursor.execute('''SELECT CreationTimestamp, SUM(Value)
                               FROM %s
                               WHERE CreationTimeStamp > %s AND CreationTimeStamp < %s AND SensorID IN (
	                               SELECT ID
	                               FROM Sensor
	                               WHERE InstalledOn IN (
			                           SELECT ID
			                           FROM House
			                           WHERE AddressID IN (
				                           SELECT ID
				                           FROM Address
				                           WHERE %s = %s
				                       )
		                           )
	                           )
                               GROUP BY CreationTimestamp''',[Table,StartMoment,EndMoment,Adress,Adrname])
        rows = self.cursor.fetchall()
        for i in rows:
			self.results.append(MinuteDataSample(i))
        


    def searchStreet(self,Table,Startmoment,EndMoment,strName,Town):
        self.cursor.execute('''SELECT CreationTimestamp, SUM(Value)
                               FROM %s
                               WHERE SensorID IN (
	                               SELECT ID
	                               FROM Sensor
	                               WHERE CreationTimeStamp > %s AND CreationTimeStamp < %s AND InstalledOn IN (
			                           SELECT ID
			                           FROM House
			                           WHERE AddressID IN (
				                           SELECT ID
				                           FROM Address
				                           WHERE StreetName = %s AND City = %s
				                       )
		                           )
	                           )
                               GROUP BY CreationTimestamp;''',[Table,StartMoment,EndMoment,strNname,Town])
        rows = self.cursor.fetchall()
        for i in rows:
			self.results.append(MinuteDataSample(i))


#    def searchMoment(self,Table,Moment):
#        self.cursor.execute('''SELECT House.ID,SUM(Value) AS HouseUse
#                               FROM House,Sensor,%s AS ThisTable
#                               WHERE House.ID=Sensor.InstalledOn AND ThisTable.InstalledOn=Sensor.ID AND ThisTable.CreationTimeStamp=%s
#                               ORDER BY HouseUse ASC''',[Table,Moment])
#        rows = self.cursor.fetchall()
#        for i in rows:
#			self.results.append(MinuteDataSample(i))

#    def searchMomentPlace(self,Table,Moment,KindOfPlace,Place):
#        self.cursor.execute('''SELECT House.ID,SUM(Value) AS HouseUse
#                               FROM House,Sensor,%s AS ThisTable
#                               WHERE House.ID=Sensor.InstalledOn AND ThisTable.InstalledOn=Sensor.ID AND ThisTable.CreationTimeStamp=%s AND House.AddressID IN (
#                                   SELECT ID FROM Address WHERE %s = %s
#                               )
#                               ORDER BY HouseUse ASC''',[Table,Moment,KindOfPlace,Place])
#        rows = self.cursor.fetchall()
#        for i in rows:
#			self.results.append(MinuteDataSample(i))

#    def searchMomentStreet(self,Table,Moment,KindOfPlace,Place,Street):
#        self.cursor.execute('''SELECT House.ID,SUM(Value) AS HouseUse
#                               FROM House,Sensor,%s AS ThisTable
#                               WHERE House.ID=Sensor.InstalledOn AND ThisTable.InstalledOn=Sensor.ID AND ThisTable.CreationTimeStamp=%s AND House.AddressID IN (
#                                   SELECT ID FROM Address WHERE %s = %s AND StreetName = %s
#                               )
#                               ORDER BY HouseUse ASC''',[Table,Moment,KindOfPlace,Place,Street])
#        rows = self.cursor.fetchall()
#        for i in rows:
#			self.results.append(MinuteDataSample(i))

    def toJson(self):
        result = {}
        result["datasamples"] = []
        for i in self.results:
            result["datasamples"].append(dict(i))
        return json.dumps(result)

