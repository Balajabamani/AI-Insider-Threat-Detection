-- =====================================================
-- AI Powered Insider Threat Detection System
-- Database Schema
-- =====================================================

CREATE TABLE IF NOT EXISTS login_logs (

    id SERIAL PRIMARY KEY,

    employee_id VARCHAR(20) NOT NULL,

    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    ip_address VARCHAR(50),

    device_name VARCHAR(100),

    login_status VARCHAR(20)

);