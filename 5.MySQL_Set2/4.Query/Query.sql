-- Create Database
CREATE DATABASE coding_two;
USE coding_two;

-- Create Employees Table
CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    salary INT,
    department_id INT
);

-- Insert Employee Data
INSERT INTO employees (employee_id, name, age, salary, department_id) VALUES
(1, 'John', 30, 80000, 101),
(2, 'Emily', 25, 50000, 102),
(3, 'Michael', 40, 90000, 103),
(4, 'Sara', 35, 56000, 101),
(5, 'David', 28, 49000, 102),
(6, 'Robert', 45, 95000, 103),
(7, 'Sophia', 29, 51000, 102);


-- Create Departments Table
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(50)
);

-- Insert Department Data
INSERT INTO departments (department_id, department_name) VALUES
(101, 'HR'),
(102, 'Finance'),
(103, 'IT');

-- Create Sales Table
CREATE TABLE sales (
    sale_id INT PRIMARY KEY,
    product_id INT,
    customer_id INT,
    amount DECIMAL(10,2),
    sale_date DATE
);

-- Insert Sales Data
INSERT INTO sales (sale_id, product_id, customer_id, amount, sale_date) VALUES
(1, 1, 101, 4500.00, '2023-03-01'),
(2, 2, 102, 5500.00, '2023-03-02'),
(3, 3, 103, 7000.00, '2023-04-01'),
(4, 1, 104, 3000.00, '2023-04-02'),
(5, 2, 105, 6000.00, '2023-05-01');

-- Create Orders Table
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    order_date DATETIME,
    order_amount INT
);

-- Insert Order Data
INSERT INTO orders (order_id, customer_name, order_date, order_amount) VALUES
(1, 'John', '2023-05-01 10:00:00', 500),
(2, 'Emily', '2023-05-02 10:15:00', 700),
(3, 'Michael', '2023-05-03 10:30:00', 1200),
(4, 'Sara', '2023-05-04 11:00:00', 450),
(5, 'David', '2023-05-05 10:45:00', 900),
(6, 'John', '2023-05-06 10:30:00', 600),
(7, 'Emily', '2023-05-07 10:15:00', 750);

-- Create Products Table
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    price INT
);

-- Insert Product Data
INSERT INTO products (product_id, product_name, price) VALUES
(1, 'Laptop', 1000),
(2, 'Mobile', 500),
(3, 'Tablet', 300),
(4, 'Headphones', 100),
(5, 'Smartwatch', 200);


-- 1.Retrieve all employees whose salary is greater than 60000.

SELECT * FROM employees
WHERE salary > 60000;

-- 2.Calculate the total sales amount for each customer from the sales table.

SELECT customer_id, SUM(amount) AS total_sales
FROM sales
GROUP BY customer_id;

-- 3.Retrieve the names and salaries of all employees working in the Finance department.

SELECT name, salary 
FROM employees e
LEFT JOIN departments d ON e.department_id = d.department_id
WHERE d.department_name = 'Finance';

-- 4.Find the total sales amount made on 2023-03-17 from the sales table.

SELECT SUM(amount) as tot_sales
FROM sales
GROUP BY sale_date
HAVING sale_date = '2023-03-17';

-- 5.Get the names of customers who have placed an order of more than 600 from the orders table.

SELECT customer_name FROM orders
WHERE order_amount > 600;
