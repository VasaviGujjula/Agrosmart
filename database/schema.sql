CREATE DATABASE IF NOT EXISTS agrosmart;
USE agrosmart;

-- 1. Base Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('farmer', 'buyer', 'admin') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Farmer Profiles (1-to-1 with users)
CREATE TABLE farmer_profiles (
    farmer_id INT PRIMARY KEY,
    full_name VARCHAR(100),
    location VARCHAR(255),
    land_size_acres DECIMAL(10, 2),
    farming_experience_years INT,
    FOREIGN KEY (farmer_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 3. Buyer Profiles (1-to-1 with users)
CREATE TABLE buyer_profiles (
    buyer_id INT PRIMARY KEY,
    company_name VARCHAR(150),
    business_registration_no VARCHAR(100),
    industry_type VARCHAR(100),
    FOREIGN KEY (buyer_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- 4. Crops Master Table
CREATE TABLE crops (
    crop_id INT AUTO_INCREMENT PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    base_price_per_unit DECIMAL(10, 2)
);

-- 5. Contracts (Links Farmer, Buyer, and Crop)
CREATE TABLE contracts (
    contract_id INT AUTO_INCREMENT PRIMARY KEY,
    buyer_id INT NOT NULL,
    farmer_id INT,
    crop_id INT NOT NULL,
    quantity_quintals DECIMAL(10, 2) NOT NULL,
    agreed_price_per_unit DECIMAL(10, 2) NOT NULL,
    status ENUM('open', 'signed', 'completed', 'cancelled') DEFAULT 'open',
    start_date DATE,
    delivery_date DATE,
    FOREIGN KEY (buyer_id) REFERENCES users(user_id),
    FOREIGN KEY (farmer_id) REFERENCES users(user_id),
    FOREIGN KEY (crop_id) REFERENCES crops(crop_id)
);

-- 6. Insurance Policies
CREATE TABLE insurance_policies (
    policy_id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    policy_number VARCHAR(50) UNIQUE NOT NULL,
    premium_amount DECIMAL(10, 2) NOT NULL,
    coverage_limit DECIMAL(12, 2) NOT NULL,
    status ENUM('active', 'expired', 'claimed') DEFAULT 'active',
    FOREIGN KEY (contract_id) REFERENCES contracts(contract_id)
);

-- 7. Insurance Claims
CREATE TABLE insurance_claims (
    claim_id INT AUTO_INCREMENT PRIMARY KEY,
    policy_id INT NOT NULL,
    claim_reason TEXT NOT NULL,
    claim_amount DECIMAL(12, 2) NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    filed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (policy_id) REFERENCES insurance_policies(policy_id)
);

-- 8. Payments
-- Main Payment Records
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    contract_id INT NOT NULL,
    buyer_id INT NOT NULL,
    farmer_id INT NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    status ENUM('pending', 'completed', 'failed') DEFAULT 'pending',
    payment_method VARCHAR(50),
    transaction_reference VARCHAR(100) UNIQUE,
    paid_at TIMESTAMP NULL,
    FOREIGN KEY (contract_id) REFERENCES contracts(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (farmer_id) REFERENCES users(id)
);

-- 9. Transactions (Ledger for Audit)
-- Financial Ledger for Audit
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    payment_id INT,
    type ENUM('credit', 'debit') NOT NULL,
    amount DECIMAL(12, 2) NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (payment_id) REFERENCES payments(id)
);

-- 10. Chatbot Queries
CREATE TABLE chatbot_queries (
    query_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    language_code VARCHAR(10) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- 11. Audit Logs
CREATE TABLE audit_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(255) NOT NULL,
    table_affected VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);