# TODO: Fix Dashboard Routes - Fail-Safe Implementation

## Task Overview
Make the dashboard routes fail-safe with proper try/except handling, explicit table names, and default min_threshold values.

## Steps to Complete

- [x] 1. Fix main.py - Dashboard route `/` with try/except and item.get('min_threshold', 5)
- [x] 2. Fix admin_dashboard.py - Dashboard route `/` with try/except and item.get('min_threshold', 5)
- [x] 3. Fix admin_dashboard.py - Clean up malformed code section
- [x] 4. Fix admin_dashboard.py - Ensure /usage-report uses TemplateResponse

## Changes Summary

### main.py changes:
- Wrap stock fetching in dashboard route with try/except
- Use item.get('min_threshold', 5) for low-stock calculation

### admin_dashboard.py changes:
- Wrap stock fetching in dashboard route with try/except
- Use item.get('min_threshold', 5) for low-stock calculation
- Fix malformed code between two usage report functions
- Ensure /usage-report route uses templates.TemplateResponse

## All Tasks Completed! ✅

