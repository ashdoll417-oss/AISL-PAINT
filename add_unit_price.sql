-- Add unit_price column to aviation_inventory (safe)
ALTER TABLE aviation_inventory ADD COLUMN IF NOT EXISTS unit_price DECIMAL(10,2) DEFAULT 0;

-- Create sales table for Quotes → Sales workflow
CREATE TABLE IF NOT EXISTS sales (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    quote_number TEXT UNIQUE NOT NULL,
    part_number TEXT REFERENCES aviation_inventory(part_number),
    description TEXT,
    category TEXT,
    uom TEXT,
    quantity DECIMAL(10,2) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) GENERATED ALWAYS AS (quantity * unit_price) STORED,
    order_status TEXT CHECK (order_status IN ('Quote', 'Completed', 'Cancelled')) DEFAULT 'Quote',
    customer_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    notes TEXT
);

-- Indexes
CREATE INDEX idx_sales_quote_number ON sales(quote_number);
CREATE INDEX idx_sales_status ON sales(order_status);
CREATE INDEX idx_sales_part_number ON sales(part_number);
CREATE INDEX idx_sales_created ON sales(created_at DESC);

-- Trigger: Update completed_at on status change
CREATE OR REPLACE FUNCTION update_sales_completed_at()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_status = 'Completed' AND OLD.order_status != 'Completed' THEN
        NEW.completed_at = NOW();
    ELSIF NEW.order_status != 'Completed' THEN
        NEW.completed_at = NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_sales_status 
BEFORE UPDATE ON sales 
FOR EACH ROW EXECUTE FUNCTION update_sales_completed_at();

