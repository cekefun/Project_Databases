from __future__ import unicode_literals

from django.db import models , connection

import datetime

import os.path

import csv
# Create your models here.

def save_uploaded_file(f):
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
                    self.cursor.execute("SELECT ID FROM Sensor WHERE InstalledOn = %s AND Apparature = %s",[HouseID,header[column]])
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
