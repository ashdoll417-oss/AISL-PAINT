-- Suppliers Table
-- This script creates the suppliers table for the Aviation ERP system

CREATE TABLE IF NOT EXISTS suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_name TEXT NOT NULL,
    contact_person TEXT,
    email TEXT,
    phone TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for supplier name search
CREATE INDEX IF NOT EXISTS idx_suppliers_name ON suppliers(supplier_name);

-- Insert sample suppliers (optional)
-- INSERT INTO suppliers (supplier_name, contact_person, email, phone)
-- VALUES 
-- ('Aircraft Supplies Co.', 'John Doe', 'john@aircraftsupplies.com', '+254 700 123456'),
-- ('Aviation Parts Ltd', 'Jane Smith', 'jane@aviationparts.co.ke', '+254 700 234567');

