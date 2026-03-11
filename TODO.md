# TODO: Dynamic Low Stock Alert Implementation

## Step 1: Database Schema Update
- [x] Update aviation_inventory.sql - Add min_threshold column

## Step 2: Backend Updates (main.py)
- [x] Update get_low_stock_items() function to check current_stock <= min_threshold
- [x] Add GET /api/low-stock/count endpoint for real-time polling
- [x] Add GET /api/low-stock/details endpoint for modal data
- [x] Update add_item endpoint to handle min_threshold field

## Step 3: Dashboard UI (dashboard.html)
- [x] Add Notifications section at top
- [x] Create red flashing alert card
- [x] Add clickable modal showing part numbers and quantities
- [x] Add JavaScript for polling every 10 seconds

## Step 4: Stock Page (stock.html)
- [x] Add min_threshold field to manual entry form

## Step 5: Real-time Update (issue_stock.html)
- [x] Update issue_stock.html to trigger notification on successful issue

## Implementation Complete!
All features have been implemented:
- Dynamic low stock alerts based on per-item min_threshold
- Flashing red alert on dashboard when items are low
- Clickable modal showing detailed list of low stock items
- Real-time polling every 10 seconds
- Immediate update after staff issues items

