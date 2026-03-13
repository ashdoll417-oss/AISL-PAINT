# Aviation ERP Route Fixes - Approved Plan

## Current Status: Planning Complete ✅

**Summary**: Fix Flask ERP routes per requirements. Most already implemented.

### Step 1: Create this TODO.md [COMPLETED]

### Step 2: Fix app.py view_order/print-order routes [COMPLETED ✅]
- Handle UUID id on sales table
- Add fallback for ORD-/PO- string: search sales.po_number or purchase_orders.po_number
- Multi-table: try sales, then purchase_orders + items, render order_print.html
- Expected: No more 'detail not found' JSON errors

### Step 3: Ensure Purchase Orders & Quote Generator dropdowns [COMPLETED ✅]
- admin_dashboard.py: Extended /purchase-orders & /quote to fetch/pass full aviation_inventory + suppliers to templates
- JS dropdowns now have full data available server-side
- Confirmed templates use /api/inventory/search + /api/suppliers (enhanced with full lists)

### Step 4: Verify other routes already fixed
- Stock Management: app.py ✅
- Usage Reports: admin_dashboard.py groups by part_number ✅  
- Stock Logs: main.py search by part_number ✅

### Step 5: Test all routes
```
# Terminal 1 (Flask)
python app.py

# Terminal 2 (FastAPI)  
uvicorn admin_dashboard:app --port 8000 --reload
uvicorn main:app --port 8001 --reload  

# Test URLs:
http://localhost:5000/stock-management
http://localhost:8000/purchase-orders  
http://localhost:8000/quote
http://localhost:5000/view-order/[id-or-ORD-123] 
http://localhost:8000/usage-reports
http://localhost:8001/admin/logs
```

### Step 6: Update TODO.md [Mark as done] + attempt_completion

**Next Step: Step 2 - Edit app.py**

