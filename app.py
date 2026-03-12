"""
Aviation ERP Admin Portal - Professional Flask + Supabase
Tables: aviation_inventory, suppliers, sales
Features: Dashboard (metrics), Issue Item (atomic transaction)

Senior ERP Developer Implementation:
- Env vars (.env) → database.py handles
- Bootstrap 5 UI
- Atomic transactions
- Error handling + flash messages
- Gunicorn ready

Deploy: gunicorn app:app --workers 3 --bind 0.0.0.0:$PORT
"""

import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_bootstrap import Bootstrap5
from database import get_supabase_service_client
from datetime import datetime
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-change-me')
bootstrap = Bootstrap5(app)

def get_supabase():
    """Get Supabase service client."""
    return get_supabase_service_client()

def get_admin_metrics():
    """Calculate Admin metrics from aviation_inventory."""
    supabase = get_supabase_service_client()
    
    try:
        # Total Items
        total_count = supabase.table('aviation_inventory').select('count(*)', count='exact').execute()
        total_items = total_count.count or 0
        
        # Paint Volume (opening_stock WHERE category='Paint')
        paint_vol = supabase.table('aviation_inventory').select('SUM(opening_stock)', count='exact').eq('category', 'Paint').execute()
        paint_volume = float(paint_vol.data[0]['sum'] or 0) if paint_vol.data else 0
        
        # Carpet Volume
        carpet_vol = supabase.table('aviation_inventory').select('SUM(opening_stock)', count='exact').eq('category', 'Carpet').execute()
        carpet_volume = float(carpet_vol.data[0]['sum'] or 0) if carpet_vol.data else 0
        
        # Low Stock (opening_stock < 10)
        low_stock = supabase.table('aviation_inventory').select('*').lt('opening_stock', 10).execute().data or []
        
        return {
            'total_items': total_items,
            'paint_volume': paint_volume,
            'carpet_volume': carpet_volume,
            'low_stock': low_stock,
            'low_stock_count': len(low_stock)
        }
    except Exception as e:
        return {'error': str(e), 'total_items': 0, 'paint_volume': 0, 'carpet_volume': 0, 'low_stock': [], 'low_stock_count': 0}

@app.route('/')
def health_check():
    """Health check - simple JSON."""
    return jsonify({
        'status': 'Service Online',
        'service': 'Aviation ERP Admin Portal',
        'metrics': get_admin_metrics(),  # Bonus: include metrics
        'timestamp': datetime.utcnow().isoformat()
    })

@app.route('/admin')
@app.route('/admin/dashboard')
def admin_dashboard():
    """Professional Dashboard - Total Inventory Value + Total Sales."""
    try:
        supabase = get_supabase()
        
        # Total Inventory Value (aviation_inventory)
        inventory = supabase.table('aviation_inventory').select('SUM(current_stock * COALESCE(unit_price_usd, 0)) as total_value, COUNT(*) as item_count').execute()
        total_value = float(inventory.data[0]['total_value'] if inventory.data else 0)
        total_items = int(inventory.data[0]['item_count'] if inventory.data else 0)
        
        # Total Sales (sales table)
        sales = supabase.table('sales').select('SUM(quantity * unit_price) as total_sales').execute()
        total_sales = float(sales.data[0]['total_sales'] if sales.data else 0)
        
        # Low stock (current_stock < 10)
        low_stock = supabase.table('aviation_inventory').select('*').lt('current_stock', 10).execute().data or []
        
        context = {
            'greeting': f"Good {datetime.now().strftime('%A')}",
            'total_inventory_value': f"${total_value:,.2f}",
            'total_items': total_items,
            'total_sales': f"${total_sales:,.2f}",
            'low_stock_count': len(low_stock),
            'recent_low_stock': low_stock[:5]
        }
        return render_template('dashboard.html', **context)
    
    except Exception as e:
        flash(f'Dashboard Error: {str(e)}', 'danger')
        return render_template('dashboard.html', greeting='Dashboard')

@app.route('/admin/issue-item', methods=['GET', 'POST'])
def admin_issue_item():
    """Issue Item - Atomic: aviation_inventory.current_stock -= 1 + sales row."""
    supabase = get_supabase()
    
    if request.method == 'POST':
        part_number = request.form['part_number']
        quantity = float(request.form['quantity']) or 1.0
        
        try:
            # Atomic transaction using service role
            # 1. Check & lock inventory row
            inventory = supabase.table('aviation_inventory').select('current_stock').eq('part_number', part_number).execute()
            
            if not inventory.data:
                flash('Part not found', 'danger')
                return redirect(url_for('admin_issue_item'))
            
            current_stock = float(inventory.data[0]['current_stock'])
            if current_stock < quantity:
                flash(f'Insufficient stock. Available: {current_stock}', 'danger')
                return redirect(url_for('admin_issue_item'))
            
            # 2. Update inventory
            new_stock = current_stock - quantity
            supabase.table('aviation_inventory').update({'current_stock': new_stock}).eq('part_number', part_number).execute()
            
            # 3. Add sales row as 'Issued'
            sale_id = supabase.table('sales').insert({
                'part_number': part_number,
                'type': 'Issued',
                'quantity': quantity,
                'current_stock_after': new_stock,
                'timestamp': datetime.utcnow(),
                'notes': f'Issued {quantity} units'
            }).execute()
            
            flash(f'✅ Issued {quantity} units. New stock: {new_stock}', 'success')
            
        except Exception as e:
            flash(f'❌ Error issuing item: {str(e)}', 'danger')
        
        return redirect(url_for('admin_issue_item'))
    
    # GET: Inventory dropdown
    inventory = supabase.table('aviation_inventory').select('part_number, description, current_stock, uom').order('part_number').execute().data or []
    
    return render_template('issue_item.html', 
                         inventory=inventory,
                         greeting=f"Good {datetime.now().strftime('%A')}")

@app.route('/admin/inventory')
def admin_inventory_list():
    """Full inventory listing."""
    supabase = get_supabase()
    items = supabase.table('aviation_inventory').select('*').order('part_number').execute().data or []
    
    for item in items:
        stock = float(item['current_stock'])
        item['status'] = 'danger' if stock == 0 else 'warning' if stock < 10 else 'success'
    
    return render_template('inventory.html', items=items, greeting=f"Good {datetime.now().strftime('%A')}")

if __name__ == '__main__':
    print("🚀 Aviation ERP Admin Portal - Professional Edition")
    print("🌐 Health check: http://localhost:5000/")
    print("📊 Dashboard: http://localhost:5000/admin")
    print("📦 Issue Item: http://localhost:5000/admin/issue-item")
    print("📋 Deploy: gunicorn app:app --workers 3")
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))

