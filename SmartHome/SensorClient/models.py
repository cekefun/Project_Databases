from __future__ import unicode_literals

from django.db import models , connection

import datetime

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



class CSVDecoder:
    def __init__(self):
        self.cursor = connection.cursor()
        
    def Decode(self,filename,HouseID):
        ifile = open(filename,'r')
        reader = csv.reader(ifile,delimiter=str(';'))
        rownum = 0
        timeColumn = -1
        for row in reader:
            if rownum == 0:
                header = row
                headerNum = 0
                for col in header:
                    if col == "Timestamp":
                        timeColumn = headerNum
                        break
                if timeColumn < 0:
                    ifile.close()
                    return False
            
            else:
                column = 0
                for col in row: 
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
            self.cursor.execute("INSERT INTO Sensor (Title,InstalledOn,Active) VALUES (%s,%s,%s)",["Lights",Houseid,True])
            for Appl in i['appliances']:
                self.cursor.execute("INSERT INTO Sensor (Title,InstalledOn,Active) VALUES (%s,%s,%s)",[Appl,Houseid,True])
        json_data.close()
        return True
        
