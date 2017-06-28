CREATE DATABASE IF NOT EXISTS musiciansfriend;
USE musiciansfriend;
CREATE TABLE IF NOT EXISTS musiciansfriend (id int AUTO_INCREMENT PRIMARY KEY, url text, name varchar(255), style varchar(255), brand varchar(255), price decimal(10,2), availability varchar(255));
