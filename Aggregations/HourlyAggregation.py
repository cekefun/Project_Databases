'''
COMPLETE SQL QUERY FOR MINUTE AGGREGATION TO HOURDATA

insert into HourData 
select timestamp( makedate( year(now()), dayofyear(now()) ), maketime( hour(now()) - 1, 0, 0 ) ) as CreationTimestamp, 
 MinuteData.SensorID as SensorID,
 SUM(MinuteData.Value) as Value
from MinuteData
where CreationTimestamp between 
 timestamp( makedate( year(now()), dayofyear(now()) ), maketime( hour(now()) - 1, 0, 0 ) )
 and 
 timestamp( makedate( year(now()), dayofyear(now()) ), date_sub(maketime( hour(now()), 59, 59), interval 1 hour) ) 
group by SensorID;

'''

'''
COMPLETE SQL QUERY FOR MINUTE DELETION AFTER  DAYS

delete from MinuteData
where CreationTimestamp < timestamp( makedate( year(now()), dayofyear(now()) - 2), maketime( hour(now()), 0, 0))

'''

import MySQLdb as mysql


class HourlyAggregation:
	def __init__(self):
		self.database = mysql.connect("localhost", "root", "", "smarthome")
		self.database.autocommit(True)
		self.cursor = self.database.cursor()

	def execute(self):
		self.insertHourlyTuples()
		self.deleteOutdatedTuples()

	def insertHourlyTuples(self):

		command = """ insert into HourData select timestamp( makedate( year(now()), dayofyear(now()) ), maketime( hour(now()) - 1, 0, 0 ) ) as CreationTimestamp, MinuteData.SensorID as SensorID, SUM(MinuteData.Value) as Value from MinuteData where CreationTimestamp between timestamp( makedate( year(now()), dayofyear(now()) ), maketime( hour(now()) - 1, 0, 0 ) ) and timestamp( makedate( year(now()), dayofyear(now()) ), date_sub(maketime( hour(now()), 59, 59), interval 1 hour) ) group by SensorID;"""
		self.cursor.execute(command)


	def deleteOutdatedTuples(self):
		command = """ delete from MinuteData where CreationTimestamp < timestamp( makedate( year(now()), dayofyear(now()) - 2), maketime( hour(now()), 0, 0)) """

		self.cursor.execute(command)

		#TIMESTAMP('2016-04-01', '16:00:00')


		#sql command to retrieve timestamp with the start of the previous hour
		#for example:	Current timestamp = 2016-04-01 15:24:16
		#				Resulting timestamp = 2016-04-01 14:00:00
		#timestamp(makedate(year(now()), dayofyear(now())), maketime(hour(now()) - 1, 0, 0));




HourlyAggregation().execute()