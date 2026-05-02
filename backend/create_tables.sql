-- Create all database tables for Price Tracker
-- Run this in Supabase SQL Editor

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS ix_users_email ON users(email);

-- Create tracked_products table
CREATE TABLE IF NOT EXISTS tracked_products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    product_name VARCHAR(500) NOT NULL,
    product_url TEXT NOT NULL,
    current_price NUMERIC(10, 2) NOT NULL,
    price_threshold NUMERIC(10, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    image_url TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    last_checked TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_tracked_products_user_id ON tracked_products(user_id);
CREATE INDEX IF NOT EXISTS idx_tracked_products_last_checked ON tracked_products(last_checked);

-- Create price_history table
CREATE TABLE IF NOT EXISTS price_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tracked_product_id UUID NOT NULL REFERENCES tracked_products(id) ON DELETE CASCADE,
    price NUMERIC(10, 2) NOT NULL,
    checked_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_price_history_product_id ON price_history(tracked_product_id);
CREATE INDEX IF NOT EXISTS idx_price_history_checked_at ON price_history(checked_at);

-- Create notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    tracked_product_id UUID NOT NULL REFERENCES tracked_products(id) ON DELETE CASCADE,
    old_price NUMERIC(10, 2) NOT NULL,
    new_price NUMERIC(10, 2) NOT NULL,
    sent_at TIMESTAMP NOT NULL DEFAULT NOW(),
    delivery_status VARCHAR(50) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_notifications_user_id ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_sent_at ON notifications(sent_at);

-- Create platform_errors table
CREATE TABLE IF NOT EXISTS platform_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    platform VARCHAR(50) NOT NULL,
    error_type VARCHAR(100) NOT NULL,
    error_message TEXT,
    occurred_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_platform_errors_occurred_at ON platform_errors(occurred_at);
CREATE INDEX IF NOT EXISTS idx_platform_errors_platform ON platform_errors(platform);
