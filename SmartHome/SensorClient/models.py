from __future__ import unicode_literals

from django.db import models , connection

import datetime
import threading
import os.path

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
    def __init__(self,date,value,HouseID,Mean,SD):
        self.House = HouseID
        self.Total = value
        self.Moment = date
        self.Mean = Mean
        self.SD = SD
        thread = threading.Thread(target=self.run,args=())
        thread.daemon = False
        thread.start()

    def normpdf(x, mean, sd):               #FUNCTION COPIED FROM http://stackoverflow.com/questions/12412895/calculate-probability-in-normal-distribution-given-mean-std-in-python
        var = float(sd)**2
        pi = math.pi
        denom = (2*pi*var)**.5
        num = math.exp(-(float(x)-float(mean))**2/(2*var))
        return num/denom
        
    def run(self):
        chance = normpdf(self.Total,self.Mean,self.SD)
        if(chance < 0.01):
            #do shit
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
                if timeColumn < 0 or totalColumn < 0:
                    ifile.close()
                    return False
            
            else:
                column = 0
                for col in row: 
                    if column == timeColumn:
                        continue
                    if column == totalColumn and info != None:
                        CrashThread(str(row[timeColumn]),col,HouseID,Mean,SD)
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
        
