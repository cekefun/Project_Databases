from __future__ import unicode_literals

from django.db import models , connection

import datetime
import threading
import os.path

from scipy.stats import norm
import MySQLdb as mysql
import csv
import json

# Create your models here.

def save_uploaded_csvfile(f):
    filename = str(datetime.time())
    if os.path.isfile(filename+".csv"):
        succes = False
        i = 0
        while not succes:
            succes = not os.path.isfile(filename+str(i)+".csv")
            i += 1
        filename += str(i)
    filename += ".csv"
    with open(filename, 'w+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename

def save_uploaded_jsonfile(f):
    filename = str(datetime.time())
    if os.path.isfile(filename+".json"):
        succes = False
        i = 0
        while not succes:
            succes = not os.path.isfile(filename+str(i)+".json")
            i += 1
        filename += str(i)
    filename += ".json"
    with open(filename, 'w+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return filename


class CrashThread:
    def __init__(self,date,HouseID,Mean,SD):
        self.database = mysql.connect("localhost", "root", "", "smarthome")
        self.database.autocommit(True)
        self.cursor = self.database.cursor()
        self.House = HouseID
        self.Total = 0
        self.Moment = date
        self.Mean = Mean
        self.SD = SD
        thread = threading.Thread(target=self.run,args=())
        thread.daemon = False
        thread.start()

    def getPrevDate(self):
        command = '''SELECT CreationTimestamp,SUM(Value) FROM MinuteData WHERE CreationTimestamp < %s AND SensorID IN(SELECT ID from Sensor WHERE InstalledOn = %s) GROUP BY CreationTimestamp ORDER BY CreationTimestamp DESC LIMIT 1;''' 
        self.cursor.execute(command,[self.Moment,self.House])
        time = self.cursor.fetchone()
        self.Moment = time[0]
        self.Total = time[1]
    
    def run(self):
        self.getPrevDate()
        chance = 1 - norm.cdf(self.Total,self.Mean,self.SD)
        if(chance < 0.05):
            command = '''SELECT SensorID, Value FROM MinuteData WHERE CreationTimestamp = %s AND SensorID in (SELECT ID from Sensor WHERE InstalledOn = %s) ORDER BY Value DESC LIMIT 3;'''
            self.cursor.execute(command,[self.Moment,self.House])
            sensorData = [[0,0],[0,0],[0,0]]
            counter = 0
            for sensor in self.cursor:
                sensorData[counter][0]=sensor[0]
                sensorData[counter][1]=sensor[1]
                counter += 1
            
            command = '''INSERT INTO Crashes VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            self.cursor.execute(command,[self.House,self.Moment,self.Total,sensorData[0][0],sensorData[0][1],sensorData[1][0],sensorData[1][1],sensorData[2][0],sensorData[2][1]])
            return    
        else:
            return

        
        
        

class CSVDecoder:
    def __init__(self):
        self.cursor = connection.cursor()
        
    def Decode(self,filename,HouseID):
        ifile = open(filename,'r')
        reader = csv.reader(ifile,delimiter=str(';'))
        rownum = 0
        timeColumn = -1
        totalColumn = -1
        Mean = 0
        SD = 1
        self.cursor.execute("SELECT Mean, Deviation FROM CrashData WHERE HouseID = %s",[HouseID])
        info = self.cursor.fetchone()
        if info != None:
            Mean = info[0]
            SD = info[1]
        for row in reader:
            if rownum == 0:
                header = row
                headerNum = 0
                for col in header:
                    if col == "Timestamp":
                        timeColumn = headerNum
                    if col == "Total":
                        totalColumn = headerNum
                    headerNum += 1
                if timeColumn < 0 or totalColumn < 0:
                    ifile.close()
                    return False
            
            else:
                column = 0
                for col in row: 
                    if column == timeColumn:
                        column += 1
                        continue
                    if rownum == 1 and column == totalColumn and info != None:
                        column += 1
                        CrashThread(str(row[timeColumn]),HouseID,Mean,SD)
                        continue
                    elif column == totalColumn and info != None and int(float(col)) == 0:
                        column += 1
                        CrashThread(str(row[timeColumn]),HouseID,Mean,SD)
                        continue
                    self.cursor.execute("SELECT ID FROM Sensor WHERE InstalledOn = %s AND Title = %s",[HouseID,header[column]])
                    AppID = self.cursor.fetchone()
                    if AppID == None:
                        column += 1
                    else:
                        timestamp = str(row[timeColumn])
                        self.cursor.execute("INSERT INTO MinuteData (CreationTimestamp,SensorID,Value) VALUES (%s,%s,%s)",[timestamp,str(AppID[0]),col])
                        column +=1
            rownum += 1
    
        ifile.close()
        return True

class jsonDecoder:
    def __init__(self):
        self.cursor = connection.cursor()
    def Decode(self,filename):
        json_data = open(filename)
        data = json.load(json_data)
        for i in data:
            Houseid = i['id_household']
            self.cursor.execute("INSERT INTO House (ID,AddressID,OwnedBy) VALUES (%s,%s,%s)",[Houseid,1,1])
            self.cursor.execute("INSERT INTO Sensor (Title,InstalledOn) VALUES (%s,%s)",["Lights",Houseid])
            for Appl in i['appliances']:
                self.cursor.execute("INSERT INTO Sensor (Title,InstalledOn) VALUES (%s,%s)",[Appl,Houseid])
        json_data.close()
        return True
        
