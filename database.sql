
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
<<<<<<< HEAD
	CreationTimestamp timestamp not null,
=======
	CreationTimestamp datetime not null,
>>>>>>> origin/Django-Basic
	PostedBy int references User(ID),
	PostedOn varchar(50) references Wall(Name)
);

create table Comment(
	ID int auto_increment primary key,
	Message varchar(255),
	SensorID int not null references Sensor(ID)
);

<<<<<<< HEAD
create table House(
	ID int auto_increment primary key,
	Street varchar (155),
	Houseno int,
	Town varchar (155),
=======
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
>>>>>>> origin/Django-Basic
	OwnedBy int references User(ID)
);

create table Sensor(
	ID int auto_increment primary key,
	Apparature varchar(50) not null,
	InstalledOn int not null references House(ID),
	Active bool not null,
	Title varchar(50),
	Description varchar(255),
<<<<<<< HEAD
	Unit varchar(10)
	CONSTRAINT UniqueName UNIQUE(Apparature,InstalledOn)
);

create table MinuteData(
	CreationTimestamp timestamp not null,
=======
	Unit varchar(10),
	CONSTRAINT UniqueName UNIQUE(Title,InstalledOn)
);

create table MinuteData(
	CreationTimestamp datetime not null,
>>>>>>> origin/Django-Basic
	SensorID int references Sensor(ID),
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table HourData(
<<<<<<< HEAD
	CreationTimestamp timestamp not null,
=======
	CreationTimestamp datetime not null,
>>>>>>> origin/Django-Basic
	SensorID int references Sensor(ID),
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table DayData(
<<<<<<< HEAD
	CreationTimestamp timestamp not null,
=======
	CreationTimestamp datetime not null,
>>>>>>> origin/Django-Basic
	SensorID int references Sensor(ID),
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table MonthData(
<<<<<<< HEAD
	CreationTimestamp timestamp not null,
=======
	CreationTimestamp datetime not null,
>>>>>>> origin/Django-Basic
	SensorID int references Sensor(ID),
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);

create table YearData(
<<<<<<< HEAD
	CreationTimestamp timestamp not null,
=======
	CreationTimestamp datetime not null,
>>>>>>> origin/Django-Basic
	SensorID int references Sensor(ID),
	Value float not null,
	primary key(CreationTimestamp, SensorID)
);
<<<<<<< HEAD



=======
>>>>>>> origin/Django-Basic
