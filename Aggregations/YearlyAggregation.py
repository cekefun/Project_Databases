'''
COMPLETE SQL QUERY FOR MONTH AGGREGATION TO YEARDATA

insert into YearData
select timestamp(makedate(year(now()) - 1, 1), maketime(0,0,0)) as CreationTimestamp,
 MonthData.SensorID as SensorID,
 SUM(MonthData.Value) as Value
from MonthData
where CreationTimestamp between
 timestamp(makedate(year(now()) - 1, 1), maketime(0,0,0))
 and
 timestamp(makedate(year(now()) - 1, 365), maketime(23,59,59))
group by SensorID;
'''

'''
COMPLETE SQL QUERY FOR MONTH DELETION AFTER 10 YEARS

delete from MonthData
where CreationTimestamp < timestamp(date_sub(date_sub(makedate(year(now()),dayofyear(now())), interval dayofmonth(now())-1 day), interval 10 year), maketime(0,0,0));



COMPLETE SQL QUERY FOR YEAR DELETION AFTER 100 YEARS

delete from YearData
where CreationTimestamp < timestamp(makedate(year(now())-100,1), maketime(0,0,0));

'''

import MySQLdb as mysql


class YearlyAggregation:
	def __init__(self):
		self.database = mysql.connect("localhost", "root", "", "smarthome")
		self.database.autocommit(True)
		self.cursor = self.database.cursor()

	def execute(self):
		self.insertYearlyTuples()
		self.deleteOutdatedTuples()

	def insertYearlyTuples(self):

		command = """insert into YearData
select timestamp(makedate(year(now()) - 1, 1), maketime(0,0,0)) as CreationTimestamp,
MonthData.SensorID as SensorID,
SUM(MonthData.Value) as Value
from MonthData
where CreationTimestamp between
timestamp(makedate(year(now()) - 1, 1), maketime(0,0,0))
and
timestamp(makedate(year(now()) - 1, 365), maketime(23,59,59))
group by SensorID;"""
		self.cursor.execute(command)


	def deleteOutdatedTuples(self):
		command = """delete from MonthData where CreationTimestamp < timestamp(date_sub(date_sub(makedate(year(now()),dayofyear(now())), interval dayofmonth(now())-1 day), interval 10 year), maketime(0,0,0));"""
		self.cursor.execute(command)

		command = """ delete from YearData where CreationTimestamp < timestamp(makedate(year(now())-100,1), maketime(0,0,0)); """
		self.cursor.execute(command)



YearlyAggregation().execute()