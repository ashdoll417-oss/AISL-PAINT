-- Create tint_recipes table for Paint Tinting System
CREATE TABLE IF NOT EXISTS tint_recipes (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recipe_name TEXT NOT NULL,  -- 'Client Name - Color Recipe'
    client_name TEXT NOT NULL,
    base_part_number TEXT NOT NULL REFERENCES aviation_inventory(part_number),
    tint_part_numbers JSONB NOT NULL,  -- ["TINT001", "TINT002"]
    tint_quantities JSONB NOT NULL,    -- [50, 25] ML amounts
    total_volume_ml DECIMAL(10,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    used_count INTEGER DEFAULT 0
);

-- Index for fast lookup
CREATE INDEX idx_tint_recipes_client ON tint_recipes(client_name);
CREATE INDEX idx_tint_recipes_base ON tint_recipes(base_part_number);

-- View for recipes by client
CREATE OR REPLACE VIEW view_tint_recipes_by_client AS
SELECT 
    recipe_name,
    client_name, 
    base_part_number,
    total_volume_ml,
    used_count,
    created_at
FROM tint_recipes
ORDER BY created_at DESC;

