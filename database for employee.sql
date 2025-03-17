CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

CREATE TABLE IF NOT EXISTS employee_information (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100) Null,
    username VARCHAR(25) Null,
    password varchar(25) NUll ,
    role varchar(50) NUll
);

Create Table if not exists employee_close(
    employee_name Varchar (100) NUll,
    store_name VARCHAR(100) NULL,
    credit DECIMAL(10, 2) NULL,
    cash_in_envelope DECIMAL(10, 2) NULL,
    expense DECIMAL(10, 2) NULL,
    comments TEXT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)



