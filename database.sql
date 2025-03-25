CREATE DATABASE IF NOT EXISTS employee_db;

USE employee_db;

# user information
CREATE TABLE IF NOT EXISTS employee(
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    firstName VARCHAR(15) Null,
    lastName varchar(15) Null,
    userName varchar(15),
    password varchar(25) null,
    role enum('employee','manager','owner')
    );
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','is the best','admin','admin','owner');
# todo get rid of when done for testing purposes only
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','Jaffe','e','e','owner');
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','is thn','m','m','owner');
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','Yes I am the ','o','o','owner');

# employee close
Create Table if not exists employee_close(
    firstName Varchar (15),
    lastName varchar (15),
    store_name VARCHAR(25),
    credit DECIMAL(10, 2),
    cash_in_envelope DECIMAL(10, 2),
    expense DECIMAL(10, 2),
    comments TEXT,
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

# table for store
CREATE TABLE if not exists Store (
    store_id INT Auto_Increment primary key,
    store_name VARCHAR(255),
    location VARCHAR(255)
);

# employee clock-in and clock to
Create table if not exists clockTable(
    clock_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    store_id INT,
    clock_in DATETIME,
    clock_out DATETIME,
    reg_in DECIMAL(10,2),
    reg_out DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);


# table for invoices
CREATE TABLE if not exists Invoice (
    invoice_id INT AUTO_INCREMENT primary key,
    company_name VARCHAR(255),
    amount_due DECIMAL(10,2),
    due_date DATE,
    paid_status ENUM('paid', 'unpaid'),
    payment_date DATE
);

# table for bonuses
CREATE TABLE if not exists Bonuses (
    bonus_id INT auto_increment PRIMARY KEY,
    employee_id INT,
    store_id INT,
    week_start DATE,
    week_end DATE,
    total_sales DECIMAL(10,2),
    bonus_percentage DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);