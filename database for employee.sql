CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

CREATE TABLE IF NOT EXISTS employee_financials (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_name VARCHAR(100),
    store_name VARCHAR(100),
    credit DECIMAL(10, 2),
    cash_in_envelope DECIMAL(10, 2),
    expense DECIMAL(10, 2),
    comments TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select *
from employee_financials;

