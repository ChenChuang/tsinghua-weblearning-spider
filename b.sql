drop database learnspiderdb;
create database learnspiderdb;
use learnspiderdb;
create table COURSES(
	CourseID varchar(20) not null,
	Name varchar(256) not null,
	primary key(CourseID)) CHARSET=utf8;
create table NOTICES(
	id int not null auto_increment,
	Heading varchar(256) not null,
	Url varchar(256) not null,
	Publisher varchar(40),
	Time date,
	IsRead int,
	primary key(id),
	CourseID varchar(20) references COURSES(CourseID)) CHARSET=utf8;
create table DOCUMENTS(
	id int not null auto_increment,
	Heading varchar(256) not null,
	Url varchar(256) not null,
	Explanation varchar(256),
	DocSize varchar(20), 
	Time date,
	IsRead int,
	primary key(id),
	CourseID varchar(20) references COURSES(CourseID)) CHARSET=utf8;
create table ASSIGNMENTS(
	id int not null auto_increment,
	Title varchar(256) not null,
	Url varchar(256) not null,
	StartDate date,
	DueDate date,
	Status varchar(40),
	AttSize varchar(20),
	IsRead int,
	primary key(id),
	CourseID varchar(20) not null references COURSES(CourseID)) CHARSET=utf8;
create table DISCUSSIONS(
	id int not null auto_increment,
	Subject varchar(256) not null,
	Url varchar(256) not null,
	Author varchar(40),
	ReplyNum varchar(20),
	Time datetime,
	IsRead int,
	primary key(id),
	CourseID varchar(20) not null references COURSES(CourseID)) CHARSET=utf8;
 
	 
