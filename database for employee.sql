CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

CREATE TABLE IF NOT EXISTS employee_information (
    id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(15) Null,
    lastName varchar(15) Null,
    userName varchar(15),
    password varchar(25) null,
    role enum('employee','manager','owner')
    );

Create Table if not exists employee_close(
    firstName Varchar (15),
    lastName varchar (15),
    store_name VARCHAR(25),
    credit DECIMAL(10, 2),
    cash_in_envelope DECIMAL(10, 2),
    expense DECIMAL(10, 2),
    comments TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)



