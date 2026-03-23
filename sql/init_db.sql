CREATE DATABASE student_db;
USE student_db;
CREATE TABLE accounts (
	id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user'
);

CREATE TABLE students (
	id INT AUTO_INCREMENT PRIMARY KEY,
    student_code VARCHAR(20) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    class_name VARCHAR(20) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255) NOT NULL,
    cccd VARCHAR(255) NOT NULL,
    address VARCHAR(500) NOT NULL,
    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO accounts (username, password_hash, role)
VALUES
('admin1', '123456', 'admin'),
('user1', '123456', 'user');
