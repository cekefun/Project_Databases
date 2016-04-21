'''
COMPLETE SQL QUERY FOR DAY AGGREGATION TO MONTHDATA

insert into MonthData
select timestamp( date_sub( date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 month), maketime(0,0,0)) as CreationTimestamp,
 DayData.SensorID as SensorID,
 SUM(DayData.Value) as Value
from DayData
where CreationTimestamp between
 timestamp(date_sub( date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 month), maketime(0,0,0))
 and
 timestamp(last_day( date_sub(makedate(year(now()), dayofyear(now())), interval 1 month)), maketime(0,0,0))
group by SensorID;

'''

'''
COMPLETE SQL QUERY FOR DAY DELETION AFTER 1 YEAR

delete from DayData
where CreationTimestamp < timestamp( date_sub(date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 year), maketime(0,0,0) );

'''

import MySQLdb as mysql


class MonthlyAggregation:
	def __init__(self):
		self.database = mysql.connect("localhost", "root", "", "smarthome")
		self.database.autocommit(True)
		self.cursor = self.database.cursor()

	def execute(self):
		self.insertMonthlyTuples()
		self.deleteOutdatedTuples()

	def insertMonthlyTuples(self):

		command = """insert into MonthData
select timestamp( date_sub( date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 month), maketime(0,0,0)) as CreationTimestamp,
DayData.SensorID as SensorID,
SUM(DayData.Value) as Value
from DayData
where CreationTimestamp between
timestamp(date_sub( date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 month), maketime(0,0,0))
and
timestamp(last_day( date_sub(makedate(year(now()), dayofyear(now())), interval 1 month)), maketime(0,0,0))
group by SensorID;"""
		self.cursor.execute(command)


	def deleteOutdatedTuples(self):
		command = """delete from DayData where CreationTimestamp < timestamp( date_sub(date_sub(makedate(year(now()), dayofyear(now())), interval dayofmonth(now())-1 day), interval 1 year), maketime(0,0,0) );"""

		self.cursor.execute(command)




MonthlyAggregation().execute()