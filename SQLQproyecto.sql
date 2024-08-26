CREATE DATABASE Proyecto;

USE Proyecto;

drop table if exists CompanyProfiles;
drop table if exists Companies;

CREATE TABLE CompanyProfiles (
	symbol varchar(255),
	company varchar(255),
	sector varchar (255),
	headquarters varchar (255),
	fecha_fundada varchar(255)
);

CREATE TABLE Companies (
	symbol varchar(255),
	fecha date,
	valor_close float
);


ALTER TABLE CompanyProfiles
ALTER COLUMN symbol varchar(255) NOT NULL;

ALTER TABLE CompanyProfiles
ADD CONSTRAINT PK_CompanyProfiles PRIMARY KEY (symbol);

ALTER TABLE Companies
ALTER COLUMN symbol varchar(255) NOT NULL;

ALTER TABLE Companies
ALTER COLUMN fecha date NOT NULL;

ALTER TABLE Companies
ADD CONSTRAINT PK_Companies PRIMARY KEY (symbol, fecha);



