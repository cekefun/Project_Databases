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
