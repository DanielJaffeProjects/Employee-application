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
values('Daniel','Jaffe','e','e','employee');
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','is thn','m','m','manager');
insert into employee(firstName, lastName, userName, password, role)
values('Daniel','Yes I am the ','o','o','owner');

# Test accounts with specific credentials
insert into employee(employee_id, firstName, lastName, userName, password, role)
values(99, 'Himmy', 'Butler', 'o', '123', 'owner');

insert into employee(employee_id, firstName, lastName, userName, password, role)
values(100, 'Himmy', 'Butler', 'e', '123', 'employee');

insert into employee(employee_id, firstName, lastName, userName, password, role)
values(101, 'Himmy', 'Butler', 'm', '123', 'manager');

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
    firstName Varchar (15),
    lastName varchar (15),
    clock_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    clock_in varchar(23),
    clock_out varchar(23),
    reg_in DECIMAL(10,2),
    reg_out DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);


# table for invoices
CREATE TABLE if not exists Invoice (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_company VARCHAR(255) NOT NULL,
    invoice_amount DECIMAL(10, 2) NOT NULL,
    date_received VARCHAR(20) NOT NULL,
    date_due Varchar(20) NOT NULL,
    invoice_paid ENUM('paid', 'unpaid') NOT NULL
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

CREATE TABLE IF NOT EXISTS Payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    store_id INT,
    pay_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);
CREATE TABLE IF NOT EXISTS Expense (
    expense_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    store_id INT,
    expense_date DATE,
    expense_type VARCHAR(100),
    amount DECIMAL(10,2),
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);
