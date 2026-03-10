-- ============================================================
-- Aviation ERP - Inventory Table
-- PostgreSQL Script
-- ============================================================

-- Create the inventory table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    part_number TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    material_type TEXT,
    color TEXT,
    current_stock NUMERIC(18, 4) DEFAULT 0,
    unit TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for faster queries
CREATE INDEX idx_inventory_part_number ON inventory(part_number);
CREATE INDEX idx_inventory_category ON inventory(category);
CREATE INDEX idx_inventory_material_type ON inventory(material_type);
CREATE INDEX idx_inventory_color ON inventory(color);

-- ============================================================
-- Insert Sample Data
-- ============================================================

-- Insert paint product: EPOXY PRIMER 6KG (stored as 180 KG based on user request)
INSERT INTO inventory (part_number, description, category, material_type, color, current_stock, unit)
VALUES ('113-22-633B-3-033', 'EPOXY PRIMER', 'Paint', NULL, NULL, 180, 'KG');

-- Insert paint products from original requirements
INSERT INTO inventory (part_number, description, category, material_type, color, current_stock, unit)
VALUES 
    ('470-10-9100-9-003', 'WHITE TOPCOAT', 'Paint', NULL, NULL, 10, 'KG'),
    ('405-03-0000-0-232', 'TOPCOAT HARDENER', 'Paint', NULL, NULL, 5, 'L');

-- Insert carpet products
INSERT INTO inventory (part_number, description, category, material_type, color, current_stock, unit)
VALUES 
    ('CAR-WOV-001', 'Woven Carpet', 'Carpet', 'Woven', NULL, 100, 'M'),
    ('CAR-ECO-001', 'Econyl Rips', 'Carpet', 'Econyl', NULL, 50, 'M'),
    ('AER-992-GRY', 'AERMAT 9000/992 GREY', 'Carpet', 'AERMAT', 'Grey', 75, 'M'),
    ('AER-8451-BLU', 'AERMAT 9000/8451 BLUE', 'Carpet', 'AERMAT', 'Blue', 60, 'M');

-- ============================================================
-- Trigger: Auto-update updated_at timestamp
-- ============================================================

CREATE OR REPLACE FUNCTION update_inventory_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_inventory_updated_at
    BEFORE UPDATE ON inventory
    FOR EACH ROW
    EXECUTE FUNCTION update_inventory_timestamp();

-- ============================================================
-- Comments for documentation
-- ============================================================

COMMENT ON TABLE inventory IS 'Main inventory table for Aviation ERP system';
COMMENT ON COLUMN inventory.id IS 'Primary key - auto-incremented serial';
COMMENT ON COLUMN inventory.part_number IS 'Unique part code (e.g., 113-22-633B-3-033)';
COMMENT ON COLUMN inventory.description IS 'Product description (e.g., EPOXY PRIMER, AERMAT 9000)';
COMMENT ON COLUMN inventory.category IS 'Category: Paint or Carpet';
COMMENT ON COLUMN inventory.material_type IS 'Material type: Woven, Econyl, AERMAT';
COMMENT ON COLUMN inventory.color IS 'Color: Blue, Grey';
COMMENT ON COLUMN inventory.current_stock IS 'Current stock quantity';
COMMENT ON COLUMN inventory.unit IS 'Unit of measurement: KG, L, M';

-- ============================================================
-- END OF SCRIPT
-- ============================================================

