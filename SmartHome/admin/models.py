from __future__ import unicode_literals

from django.db import models, connection

# Create your models here.

class AdminAgg:
    def __init__(self):
        self.cursor = connection.cursor()
    def search(self,Table,Startmoment,EndMoment,Adress,Adrname):
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
				                           WHERE %s = %s
				                       )
		                           )
	                           )
                               GROUP BY CreationTimestamp;''',[Table,StartMoment,EndMoment,Adress,Adrname])


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



