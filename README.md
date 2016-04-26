# Project_Databases
This is a project for databases
We use django and mySQL

To set up this server, you have to:

1. install python 2.7
2. install MYSQL
3. install MYSQL-python
4. install django (we worked and tested with 1.9)
5. create a database in mysql with the name smarthome
6. create a user in mysql with the name django and give it full authority on that database
5-6b. it is also possible to call it something else, but you would have to change settings.py in Smarthome/Smarthome
7. use the database.sql script on the new database
8. register all the scripts in Aggregations in cron
9. go to Smarthome
10. use the command python manage.py runserver

To set up a simulator, you have to:
1. copy ElecSim to where you want to simulate the house
2. change the SITE to the server/upload/
3. change the JSON to the configure file with all the families
4. change the FAMILY to the wanted family in the configure file
5. register this to cron to upload 2 minutes every time
