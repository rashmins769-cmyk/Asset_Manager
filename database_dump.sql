-- ====================================================================
-- AssetLink - PostgreSQL Database Dump
-- Client Meet #2: Accommodating 1000 employees and an HR department
-- ====================================================================

-- --------------------------------------------------------------------
-- TABLE CREATION (Data Components)
-- Note: As per the requirements, no dedicated FOREIGN KEY constraints 
-- have been utilized. Instead, simple integer ID referencing is used 
-- to keep tables independent yet logically linked.
-- --------------------------------------------------------------------

-- 1. Departments Table
-- Captures the various departments in the company, such as HR, Engineering, etc.
CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Roles Table
-- Defines the access levels (e.g., Admin, HR Manager, Standard Employee)
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    permissions_level INT DEFAULT 1
);

-- 3. Employees Table
-- Stores the 1000+ employees of the company. Linked logically to departments and roles.
CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    department_id INT, -- Logical reference to departments.id
    role_id INT,       -- Logical reference to roles.id
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Asset Categories Table
-- Groupings for assets (Hardware, Software, Furniture, etc.)
CREATE TABLE asset_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT
);

-- 5. Assets Table
-- The actual items being tracked.
CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    serial_number VARCHAR(100) UNIQUE,
    category_id INT,   -- Logical reference to asset_categories.id
    status VARCHAR(50) DEFAULT 'Available', -- Available, Assigned, Maintenance, Retired
    purchase_date DATE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Asset Assignments (Transactions) Table
-- The history/log of which asset was assigned to which employee, and by whom.
CREATE TABLE asset_assignments (
    id SERIAL PRIMARY KEY,
    asset_id INT NOT NULL,      -- Logical reference to assets.id
    employee_id INT NOT NULL,   -- Logical reference to employees.id
    assigned_by_id INT,         -- Logical reference to employees.id (The HR/Admin who issued it)
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    returned_at TIMESTAMP,
    assignment_status VARCHAR(50) DEFAULT 'Active', -- Active, Returned
    notes TEXT
);

-- --------------------------------------------------------------------
-- DATA INSERTION (Dummy Data)
-- --------------------------------------------------------------------

-- Insert Dummy Departments (Generates IDs 1 to 5)
INSERT INTO departments (name) VALUES 
('Human Resources'),
('Engineering'),
('Design'),
('Sales'),
('IT/System Administration');

-- Insert Dummy Roles (Generates IDs 1 to 3)
INSERT INTO roles (name, permissions_level) VALUES 
('System Admin', 10),
('HR Manager', 8),
('Standard Employee', 1);

-- Insert Dummy Employees (Generates IDs 1 to 5)
-- Assuming IDs map to: Alice (1), Bob (2), Charlie (3), Diana (4), Evan (5)
INSERT INTO employees (first_name, last_name, email, department_id, role_id) VALUES 
('Alice', 'Smith', 'alice.smith@assetlink.com', 1, 2),   -- HR Manager
('Bob', 'Johnson', 'bob.j@assetlink.com', 2, 3),         -- Engineering, Employee
('Charlie', 'Davis', 'charlie.d@assetlink.com', 3, 3),   -- Design, Employee
('Diana', 'Prince', 'diana.p@assetlink.com', 4, 3),      -- Sales, Employee
('Evan', 'Wright', 'evan.w@assetlink.com', 5, 1);        -- IT, System Admin
-- NOTE: In a production environment, the remaining 995 employees would be imported or inserted here.

-- Insert Dummy Asset Categories (Generates IDs 1 to 4)
INSERT INTO asset_categories (name, description) VALUES 
('Laptops', 'Company assigned laptops and computers'),
('Mobile Devices', 'Company phones and tablets'),
('Software Licenses', 'Purchased software subscriptions'),
('Office Furniture', 'Desks, chairs, and ergonomic equipment');

-- Insert Dummy Assets (Generates IDs 1 to 5)
INSERT INTO assets (name, serial_number, category_id, status, purchase_date) VALUES 
('MacBook Pro 16"', 'MBP16-2023-001', 1, 'Assigned', '2023-01-15'),
('Dell XPS 15', 'DXPS-2023-042', 1, 'Assigned', '2023-02-20'),
('iPhone 14 Pro', 'IP14P-4910', 2, 'Available', '2023-03-10'),
('Adobe Creative Cloud', 'ACC-LIC-991', 3, 'Assigned', '2023-01-05'),
('Ergonomic Office Chair', 'EOC-1002', 4, 'Assigned', '2022-11-20');

-- Insert Dummy Asset Assignments (Generates IDs 1 to 4)
-- This records the history of items being checked out to employees
INSERT INTO asset_assignments (asset_id, employee_id, assigned_by_id, assigned_at, returned_at, assignment_status, notes) VALUES 
(1, 2, 5, '2023-01-20 10:00:00', NULL, 'Active', 'MacBook assigned to Bob for engineering work.'),
(2, 1, 5, '2023-02-25 11:30:00', NULL, 'Active', 'Dell XPS assigned to Alice in HR.'),
(4, 3, 1, '2023-01-10 09:15:00', NULL, 'Active', 'Design software assigned to Charlie by HR.'),
(5, 2, 1, '2022-12-01 14:00:00', NULL, 'Active', 'Office chair provided for Bob.');
