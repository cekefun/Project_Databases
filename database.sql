create table User(
	ID int auto_increment primary key,
	FirstName varchar(30),
	LastName varchar(30),
	Email varchar(255),
	UserName varchar(255),
	Password varchar(30),
	unique (Email),
	unique (UserName)
);
create table Friends(
	UserID1 int references User(ID),
	UserID2 int references User(ID),
	primary key(UserID1, UserID2),
	constraint differentusers CHECK (UserID1 <> UserID2)
);

create table Admin(
	ID int references User(ID),
	primary key (ID)
);

create table Wall(
	Name varchar(50) primary key
);

create table SubWallOf(
	WallName1 varchar(50) references Wall(Name),
	WallName2 varchar(50) references Wall(Name), 
	primary key (WallName1, WallName2)
);

create table Moderates(
	AdminID int references Admin(ID),
	WallName varchar(50) references Wall(Name),
	primary key(AdminID, WallName)
);

create table Message(
	ID int auto_increment primary key,
	Content varchar(255),
	CreationTimestamp datetime not null,
	PostedBy int references User(ID),
	PostedOn varchar(50) references Wall(Name),
	Graph MEDIUMBLOB
);

create table Address(
	ID int auto_increment primary key,
	StreetName varchar(50) not null,
	StreetNumber int not null,
	City varchar(50) not null,
	Country varchar(50) not null,
	PostalCode int not null
);

create table House(
	ID int auto_increment primary key,
	AddressID int references Address(ID),
	PricePerUnit float DEFAULT '0',
	OwnedBy int references User(ID)
);

create table Sensor(
	ID int auto_increment primary key,
	Apparature varchar(50) DEFAULT '',
	InstalledOn int not null references House(ID),
	Active bool not null DEFAULT TRUE,
	Title varchar(50) not null,
	Description varchar(255) DEFAULT '',
	Unit varchar(10) DEFAULT 'Wh',
	CONSTRAINT UniqueName UNIQUE(Title,InstalledOn)
);

create table Comment(
	ID int auto_increment primary key,
	Message varchar(255),
	SensorID int not null references Sensor(ID),
	foreign key (SensorID) references Sensor(ID) ON DELETE CASCADE
);

create table MinuteData(
	CreationTimestamp datetime not null,
	SensorID int,
	foreign key (SensorID) references Sensor(ID) ON DELETE CASCADE,
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table HourData(
	CreationTimestamp datetime not null,
	SensorID int,
	foreign key (SensorID) references Sensor(ID) ON DELETE CASCADE,
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table DayData(
	CreationTimestamp datetime not null,
	SensorID int,
	foreign key (SensorID) references Sensor(ID) ON DELETE CASCADE,
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table MonthData(
	CreationTimestamp datetime not null,
	SensorID int,
	foreign key (SensorID) references Sensor(ID) ON DELETE CASCADE,
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table YearData(
	CreationTimestamp datetime not null,
	SensorID int,
	foreign key (SensorID) references Sensor(ID) ON DELETE CASCADE,
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create view WeekData as select CreationTimestamp, SensorID, Value 
from DayData
where CreationTimestamp between
timestamp( date_sub(makedate(year(now()), dayofyear(now())), interval 7 day), maketime(0,0,0)) and
timestamp( makedate(year(now()), dayofyear(now())), maketime(0,0,0));


INSERT INTO User(FirstName,LastName,Email,UserName,Password) VALUES ('FOO','BAR','foo@bar.com','FooBar','password');
INSERT INTO Admin VALUES (1);
INSERT INTO Address(StreetName,StreetNumber,City,Country,PostalCode) VALUES ('Foolane',0,'Bartown','Antarctica',0);








