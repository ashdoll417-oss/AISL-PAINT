# Barcode Scanning Implementation TODO

## Phase 1: Database Schema Update
- [x] Add barcode_number column to aviation_inventory table in SQL
- [x] Add index for barcode_number column

## Phase 2: Stock Form & Display Updates
- [x] Update stock.html - Add Barcode Number input field in Manual Entry Form
- [x] Add JavaScript autofocus on Barcode Number field
- [ ] Add barcode column to stock tables (Paints & Carpets) - OPTIONAL display enhancement

## Phase 3: Backend Route Updates
- [x] Update /add-item route to save barcode_number to Supabase
- [ ] Update /stock page to include barcode data - OPTIONAL display enhancement

## Phase 4: Issue Item Feature (NEW)
- [x] Create /issue-item route in main.py
- [x] Create templates/issue_item.html
- [x] Implement barcode lookup functionality
- [x] Implement quantity input and stock subtraction

## Phase 5: Search Updates
- [x] Add search by barcode OR part number (via API endpoint)
- [ ] Integrate search in stock page - OPTIONAL enhancement

## Phase 6: Navigation Update
- [x] Add "Issue Item" link to sidebar in base.html

## Implementation Complete
- All core features implemented!
- To apply database changes, run the SQL from aviation_inventory.sql in your Supabase dashboard

