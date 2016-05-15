import MySQLdb as mysql
from math import sqrt

class CrashAggregation:
	def __init__(self):
		self.database = mysql.connect("localhost", "root", "", "smarthome")
		self.database.autocommit(True)
		self.cursor = self.database.cursor()
	def execute(self):
		self.getValues()
		for row in self.cursor:
			self.handleValue(row)

	def getValues(self):
		command = '''SELECT ID,AVG(SumValue),STDDEV_SAMP(SumValue)FROM (SELECT House.ID AS ID,SUM(VALUE) AS SumValue FROM House inner join Sensor on House.ID = Sensor.InstalledOn inner join MinuteData on Sensor.ID = MinuteData.SensorID WHERE CreationTimestamp between timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 1 day), maketime(0, 0, 0)) and timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 1 day), maketime(23, 59, 59)) GROUP BY House.ID,CreationTimeStamp) AS TEMP GROUP BY ID;'''
		self.cursor.execute(command)
		return
		
	def handleValue(self,row):
		ID = row[0]
		Mean = row[1]
		Deviation = row[2]
		tempcursor = self.database.cursor()
		command = '''SELECT * FROM CrashData WHERE HouseID = %s;'''
		tempcursor.execute(command,[ID])
		oldRow = tempcursor.fetchone()
		if(oldRow == None):
			command = '''INSERT INTO CrashData VALUES(%s,%s,%s);'''
			tempcursor.execute(command,[ID,Mean,Deviation])
		else:
			newMean = (Mean+oldRow[1])/2
			newDev = sqrt(Deviation**2 + oldRow[2]**2 / 4)
			command = '''UPDATE CrashData SET Mean = %s, Deviation = %s WHERE HouseID = %s'''
			tempcursor.execute(command,[newMean,newDev,ID])
		return

CrashAggregation().execute()
