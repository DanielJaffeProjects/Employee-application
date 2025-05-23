drop database if exists employee_db;
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

# table for store
CREATE TABLE if not exists Store (
    store_id INT Auto_Increment primary key,
    store_name VARCHAR(255),
    location VARCHAR(255)
);

# employee close
Create Table if not exists employee_close(
    close_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT,
    firstName Varchar (15),
    lastName varchar (15),
    store_name VARCHAR(25),
    credit DECIMAL(10, 2),
    cash_in_envelope DECIMAL(10, 2),
    expense DECIMAL(10, 2),
    comments TEXT,
    employee_id INT,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id),
    FOREIGN KEY (store_id) REFERENCES store(store_id),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);



INSERT INTO Store (store_name, location)
VALUES ('Aloha', 'ClearWater');

# employee clock-in and clock to
Create table if not exists clockTable(
    firstName Varchar (15),
    lastName varchar (15),
    clock_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    clock_in DATETIME,
    clock_out DATETIME,
    reg_in DECIMAL(10,2),
    reg_out DECIMAL(10,2),
    duration TIME NULL,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

# test the for over a 30 days
INSERT INTO clockTable (firstName, lastName, employee_id, clock_in, clock_out, reg_in, reg_out)
VALUES ('Test', 'User', 2, '2024-10-01 08:00:00', '2024-10-01 16:00:00', 8.00, 16.00);


# table for invoices
CREATE TABLE if not exists Invoice (
    invoice_id INT AUTO_INCREMENT PRIMARY KEY,
    invoice_company VARCHAR(255) NOT NULL,
    invoice_amount DECIMAL(10, 2) NOT NULL,
    date_received VARCHAR(20) NOT NULL,
    date_due Varchar(20) NOT NULL,
    invoice_paid ENUM('paid', 'unpaid') NOT NULL
);

CREATE TABLE IF NOT EXISTS Payroll (
    payroll_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    store_id INT NOT NULL,
    timeofDate DATE NOT NULL,
    hourly_rate DECIMAL(10, 2) NOT NULL,
    hours DECIMAL(10, 2) NOT NULL,
    total_payment DECIMAL(10, 2) NOT NULL,
    payment_with_bonus DECIMAL(10, 2) NOT NULL,
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

CREATE TABLE IF NOT EXISTS Merchandise (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Merch_Type VARCHAR(255) NOT NULL,
    Merch_Value DECIMAL(10,2) NOT NULL,
    Purchase_Date DATE NOT NULL,
    StoreID INT,
    FOREIGN KEY (StoreID) REFERENCES Store(store_id)
);



Create Table if not exists withdraw(
    withdraw_id INT PRIMARY KEY AUTO_INCREMENT,
    store_id INT,
    withdraw_date DATE,
    amount DECIMAL(10,2),
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);


CREATE TABLE IF NOT EXISTS Employee_Rate (
    Rate_ID INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    Bonus_Rate DECIMAL(10, 2) NOT NULL,
    Rate_Per_Hour DECIMAL(10, 2) NOT NULL,
    day_of_year DATE NOT NULL,
    bonus_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
);

Create Table if not exists summary(
    summary_id INT AUTO_INCREMENT PRIMARY KEY,
    store_id INT,
    cash_and_credit DECIMAL(10,2),
    total_expenses DECIMAL(10,2),
    total_merchandise DECIMAL(10,2),
    total_withdraw DECIMAL(10,2),
    total_payroll DECIMAL(10,2),
    net_profit DECIMAL(10,2),
    current_balance DECIMAL(10,2),
    actual_cash DECIMAL(10,2),
    actual_credit DECIMAL(10,2),
    month int,
    year int,
    FOREIGN KEY (store_id) REFERENCES Store(store_id)
);

# triggers
DELIMITER $$

CREATE TRIGGER calculate_bonus_amount_before_insert
BEFORE INSERT ON Employee_Rate
FOR EACH ROW
BEGIN
    SET NEW.bonus_amount = NEW.Bonus_Rate * NEW.Rate_Per_Hour;
END$$

DELIMITER ;

DELIMITER //

CREATE TRIGGER calculate_duration_after_clockout
BEFORE UPDATE ON clockTable
FOR EACH ROW
BEGIN
    -- Only calculate duration if clock_out is being set and was previously NULL
    IF NEW.clock_out IS NOT NULL AND OLD.clock_out IS NULL THEN
        SET NEW.duration = TIMEDIFF(NEW.clock_out, NEW.clock_in);
    END IF;
END;
//

DELIMITER ;


# trigger to calculate the net profit before inserting or updating a summary
DELIMITER $$

CREATE TRIGGER calculate_net_profit_before_insert_or_update
BEFORE INSERT ON summary
FOR EACH ROW
BEGIN
    SET NEW.net_profit = NEW.cash_and_credit -
                         (NEW.total_expenses + NEW.total_merchandise+ NEW.total_payroll);
END$$

#trigger to calculate the net profit before updating a summary
DELIMITER $$

CREATE TRIGGER calculate_net_profit_before_update
BEFORE UPDATE ON summary
FOR EACH ROW
BEGIN
    SET NEW.net_profit = NEW.cash_and_credit -
                         (NEW.total_expenses + NEW.total_merchandise + NEW.total_payroll);
END$$

DELIMITER ;

# trigger to calculate the current balance before inserting or updating a summary
DELIMITER $$

CREATE TRIGGER calculate_current_balance_before_insert
BEFORE INSERT ON summary
FOR EACH ROW
BEGIN
    SET NEW.current_balance = NEW.net_profit - NEW.total_withdraw;
END$$

# trigger to calculate the current balance before updating a summary
DELIMITER $$

CREATE TRIGGER calculate_current_balance_before_update
BEFORE UPDATE ON summary
FOR EACH ROW
BEGIN
    SET NEW.current_balance = NEW.net_profit - NEW.total_withdraw;
END$$

DELIMITER ;
