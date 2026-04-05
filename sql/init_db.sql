
CREATE DATABASE IF NOT EXISTS information_manager_db;
USE information_manager_db;

CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL,
    data_key_user_encrypt TEXT,
    role VARCHAR(20) NOT NULL
);

CREATE TABLE personal_information (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT NOT NULL UNIQUE,
    fullname VARCHAR(100) NOT NULL,
    gender VARCHAR(10),
    email_encrypt TEXT,
    cccd_encrypt TEXT,
    phone_encrypt TEXT,
    
    CONSTRAINT fk_information_account
        FOREIGN KEY (account_id) REFERENCES accounts(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
