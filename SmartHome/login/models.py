from __future__ import unicode_literals

from django.db import models , connection

# Create your models here.

class Registerer:
    def __init__(self):
        self.cursor = connection.cursor()
    
    def Save(self,firstName,lastName,userName,email,passWord):
        self.cursor.execute("INSERT INTO User(FirstName,LastName,PassWord,UserName,Email) VALUES(%s,%s,%s,%s,%s)",[firstName,lastName,passWord,userName,email])
