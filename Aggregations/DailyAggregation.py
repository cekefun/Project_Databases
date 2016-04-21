"""
COMPLETE SQL QUERY FOR HOUR AGGREGATION TO DAILYDATA

insert into DailyData
select timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 1 day ), maketime(0,0,0)) as CreationTimestamp, 
 HourData.SensorID as SensorID,
 SUM(HourData.Value) as Value
from HourData
where CreationTimestamp between
 timestamp( date_sub(
 				makedate(year(now()), dayofyear(now())),
 				interval 1 day),
 			maketime(0, 0, 0))
 and
 timestamp( date_sub(
 				makedate(year(now()), dayofyear(now())),
 				interval 1 day),
 			maketime(23, 59, 59))
group by SensorID;

"""

"""
COMPLETE SQL QUERY FOR HOUR DELETION AFTER 2 MONTHS

delete from HourData where CreationTimestamp < timestamp(date_sub(makedate(year(now()), dayofyear(now())), interval 2 month), maketime(0,0,0));

"""



import MySQLdb as mysql


class DailyAggregation:
	def __init__(self):
		self.database = mysql.connect("localhost", "root", "", "smarthome")
		self.database.autocommit(True)
		self.cursor = self.database.cursor()

	def execute(self):
		self.insertDailyTuples()
		self.deleteOutdatedTuples()

	def insertDailyTuples(self):

		command = """ insert into DayData
select timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 1 day ), maketime(0,0,0)) as CreationTimestamp, 
HourData.SensorID as SensorID,
SUM(HourData.Value) as Value
from HourData
where CreationTimestamp between
timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 1 day), maketime(0, 0, 0))
and
timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 1 day), maketime(23, 59, 59))
group by SensorID;"""
		self.cursor.execute(command)


	def deleteOutdatedTuples(self):
		command = """ delete from HourData where CreationTimestamp < timestamp(date_sub(makedate(year(now()), dayofyear(now())), interval 2 month), maketime(0,0,0));"""
		self.cursor.execute(command)


DailyAggregation().execute()