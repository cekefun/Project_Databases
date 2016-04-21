from __future__ import unicode_literals

from django.db import models , connection

# Create your models here.

class Registerer:
    def __init__(self):
        self.cursor = connection.cursor()
    
    def Save(self,firstName,lastName,userName,email,passWord):
        self.cursor.execute("INSERT INTO User(FirstName,LastName,PassWord,UserName,Email) VALUES(%s,%s,%s,%s,%s)",[firstName,lastName,passWord,userName,email])

    def SafeEmail(self,email):
        self.cursor.execute("SELECT * FROM User WHERE Email = %s",[email])
        App = self.cursor.fetchone()
        if App != None:
            return False
        return True

    def SafeUser(self,userName):
        self.cursor.execute("SELECT * FROM User WHERE UserName = %s",[userName])
        App = self.cursor.fetchone()
        if App != None:
            return False
        return True


class ValidLogin:
    def __init__(self):
        self.cursor = connection.cursor()
        self.username = ""

    def isValid(self, username, password):
        """ Return true if the username and the password match """

        self.username = str(username)
        self.cursor.execute("select * from User where UserName = %s and Password = %s",[self.username, password])
        results = self.cursor.fetchone()
        if (results == None):
            return False
        
        return True

    def getUserID(self):
        self.cursor.execute("select User.ID from User where UserName = %s", [self.username])
        result = self.cursor.fetchone()
        return int(result[0])

    def hasHouse(self):
        userID = self.getUserID()
        self.cursor.execute("select House.ID from House where OwnedBy=%s", [str(userID)])
        result = self.cursor.fetchone()

        if (result != None):
            return True
        else:
            return False


    def getFirstHouseID(self):
        userID = self.getUserID()
        self.cursor.execute("select House.ID from House where House.OwnedBy=%s", [str(userID)])
        result = self.cursor.fetchone()

        return int(result[0])