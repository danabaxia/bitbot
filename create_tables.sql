CREATE DATABASE bitbotdb;
CREATE user 'botuser'@'localhost' identified BY '123456';
GRANT all ON bitbotdb.* TO 'botuser'@'localhost';
USE bitbotdb;
CREATE TABLE Users (user_id int NOT NULL, user_name varchar(255) NOT NULL, user_password varchar(255) NOT NULL, user_email varchar(255), user_mobilenumber varchar(255), user_address varchar(255)), cash_balance float, bitcoin_value float, PRIMARY KEY (user_id));
CREATE TABLE Transactions (transaction_id int NOT NULL, transaction_type varchar(255), transaction_bitcoin_number int, bitcoin_date date, user_id int, bitcoin_price float, transaction_amount float, order_type varchar(255), PRIMARY KEY (transaction_id));
CREATE TABLE Products (product_id int NOT NULL, user_id int NOT NULL, subcription_type varchar(255), PRIMARY KEY (product_id));
CREATE TABLE Strategies (product_id int NOT NULL, strategy_name varchar(255), product_strategy_algorithm varchar(255), PRIMARY KEY (product_id));