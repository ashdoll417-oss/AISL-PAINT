import os
from flask import Flask, render_template, request, jsonify, redirect
from datetime import datetime
import pytz
from config import settings
from database import get_supabase_service_client

app = Flask(__name__)

def get_supabase():
    return get_supabase_service_client()

def get_greeting():
    nairobi_tz = pytz.timezone('Africa/Nairobi')
    current_hour = datetime.now(nairobi_tz).hour
    if 5 <= current_hour < 12:
        return "Good Morning, AISL Aviation Team"
    elif 12 <= current_hour < 18:
        return "Good Afternoon"
    else:
        return "Good Evening"

@app.route('/api/inventory/search', methods=['GET'])
def search_inventory():
    query = request.args.get('q', '')
    try:
        supabase = get_supabase()
        res = supabase.table('aviation_inventory').select('*').ilike('part_number', f'%{query}%').execute()
        return jsonify(res.data or [])
    except Exception as e:
        print(f"Search Error: {e}")
        return jsonify([]), 500

@app.route('/api/suppliers', methods=['GET'])
def get_suppliers_api():
    try:
        supabase = get_supabase()
        res = supabase.table('suppliers').select('id, supplier_name').order('supplier_name').execute()
        return jsonify({'success': True, 'suppliers': res.data or []})
    except Exception as e:
        print(f"Supplier API Error: {e}")
        return jsonify({'success': False, 'suppliers': []}), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    try:
        supabase = get_supabase()
        res = supabase.table('aviation_inventory').select('*').execute()
        return jsonify(res.data or [])
    except Exception as e:
        print(f"Products API Error: {e}")
        return jsonify([]), 500

@app.route('/api/stock/update', methods=['POST', 'OPTIONS'])
def update_stock_api():
    if request.method == 'OPTIONS':
        return '', 200
    try:
        data = request.get_json() or request.form.to_dict()
        item_id = data.get('id') or data.get('item_id') or data.get('product_id')
        part_num = data.get('part_number')
        new_qty = float(data.get('new_quantity') or data.get('quantity') or 0)
        
        supabase = get_supabase()
        
        if item_id:
            result = supabase.table('aviation_inventory').update({'current_stock': new_qty}).eq('id', item_id).execute()
        else:
            result = supabase.table('aviation_inventory').update({'current_stock': new_qty}).eq('part_number', part_num).execute()
        
        return jsonify({"success": True}), 200
    except Exception as e:
        print(f"Update Error: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/')
def index():
    return render_template('dashboard.html', greeting=get_greeting(), low_stock_items=[], low_stock_count=0)

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

@app.route('/stock')
def stock():
    try:
        supabase = get_supabase()
        response = supabase.table("aviation_inventory").select("*").execute()
        inventory = response.data or []
        return render_template('stock.html', greeting=get_greeting(), inventory=inventory)
    except:
        return render_template('stock.html', greeting=get_greeting(), inventory=[])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

