# Quick Order Feature Implementation

## Task: Update Admin Dashboard with 'Quick Order' Feature

### Steps:

1. [x] **Database**: Add `preferred_supplier_id` column to `aviation_inventory` table
2. [x] **Backend**: Update inventory data to fetch supplier info and add supplier API
3. [x] **Stock Page**: Add Low Stock Alert section with animate-pulse and "Generate PO" buttons
4. [x] **Stock Page**: Add preferred supplier dropdown for each item
5. [x] **Purchase Order Page**: Auto-select supplier when redirecting from low stock alert
6. [x] **Backend**: Add API endpoint to update preferred supplier for items

### Status: COMPLETED ✅

### Summary of Changes:
- Added `preferred_supplier_id` column to `aviation_inventory` table in `aviation_inventory.sql`
- Updated `get_inventory_data()` in `admin_dashboard.py` to include supplier info and low_stock items
- Added `/api/suppliers` endpoint to get all suppliers
- Added `/api/inventory/update-supplier` endpoint to update preferred supplier
- Updated `/stock` route to pass suppliers and low_stock data to template
- Updated `templates/stock.html` with:
  - Low Stock Alert section with `animate-pulse` class (flashing red box)
  - "🛒 Generate PO" button for each low-stock item
  - Preferred supplier dropdown to select supplier from
- Updated `templates/purchase_order.html` to auto-select supplier when redirecting with `supplier_id` parameter

