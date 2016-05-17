from __future__ import unicode_literals

from django.db import models, connection

import json


def dictfetchall(cursor):
    "function that returns the results from an SQL query in dictionary format"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]

class DataSample:
	def __init__(self):
		self.CreationTimestamp = ""
		self.Value = 0

	def __init__(self, databasetuple):
		self.CreationTimestamp = str(databasetuple[0])
		self.Value = str(databasetuple[1])

	def __iter__(self):
		yield('CreationTimestamp', self.CreationTimestamp)
		yield('Value', self.Value)

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

    def search(self,Table,StartMoment,EndMoment,Adress,Adrname):
	Query = '''SELECT CreationTimestamp, SUM(Value) FROM %s WHERE CreationTimestamp >= %%s AND CreationTimestamp <= %%s AND SensorID IN (SELECT ID FROM Sensor WHERE InstalledOn IN (SELECT ID FROM House WHERE AddressID IN (SELECT ID FROM Address WHERE %s = %%s))) GROUP BY CreationTimestamp''' % (Table,Adress)
        self.cursor.execute(Query,[StartMoment,EndMoment,Adrname])
        rows = self.cursor.fetchall()
        for i in rows:
			self.results.append(DataSample(i))
        


    def searchStreet(self,Table,StartMoment,EndMoment,strName,Town):
        Query = '''SELECT CreationTimestamp, SUM(Value) FROM %s WHERE CreationTimestamp >= %%s AND CreationTimestamp <= %%s AND SensorID IN (SELECT ID FROM Sensor WHERE InstalledOn IN (SELECT ID FROM House WHERE AddressID IN ( SELECT ID FROM Address WHERE StreetName = %%s AND City = %%s) )) GROUP BY CreationTimestamp;''' % (Table)
        self.cursor.execute(Query,[StartMoment,EndMoment,strName,Town])
        rows = self.cursor.fetchall()
        for i in rows:
			self.results.append(DataSample(i))


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

class AdminSearch:
    def __init__(self):
        self.cursor = connection.cursor()
        self.results = []
    
    def isAdmin(self,ID):
        self.cursor.execute('''SELECT ID FROM Admin WHERE ID = %s''',[ID])
        row = self.cursor.fetchone()
        if row == None:
            return False
        return True

    def users(self):
        self.cursor.execute('''SELECT ID,FirstName,LastName,UserName,Email FROM User''')
        rows = self.cursor.fetchall()
        for i in rows:
            _dict = {}
            _dict['FirstName'] = i[1]
            _dict['LastName'] = i[2]
            _dict['UserName'] = i[3]
            _dict['Email'] = i[4]
            _dict['Admin'] = self.isAdmin(i[0])
            self.results.append(_dict)

    def getResults(self):
        return self.results
    
    def makeAdmin(self,UserName):
        self.cursor.execute('''INSERT INTO Admin SELECT ID FROM User WHERE UserName = %s''',[UserName])



class HistoryOutages:
    def __init__(self, data):
        self.cursor = connection.cursor()
        self.form = data

    def returnWrong(self):
        return json.dumps({})

    def toJSON(self):
        resultingJSON = {}
        startDate = self.form.cleaned_data['start']
        toDate = self.form.cleaned_data['to']

        if (toDate < startDate):
            return self.returnWrong()

        selectOutage = self.form.cleaned_data['selectOutage']
        if (selectOutage == "house"):
            pass
        elif (selectOutage == "neighbourhood"):
            pass
        else:
            return self.returnWrong()


        return json.dumps(resultingJSON)