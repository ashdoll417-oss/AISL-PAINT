"""
FastAPI Admin Dashboard Application
Uses Jinja2 templates for rendering the admin interface
"""

from fastapi import FastAPI, Request, templating, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

from config import settings, get_supabase_client, get_supabase_service_client

# =============================================================================
# FASTAPI APP INITIALIZATION
# =============================================================================

app = FastAPI(
    title="Aviation ERP Admin Dashboard",
    description="Admin Dashboard for Aviation ERP System",
    version="1.0.0",
)

# =============================================================================
# CORS MIDDLEWARE
# =============================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# TEMPLATES CONFIGURATION
# =============================================================================

# Get the directory where this file is located
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# =============================================================================
# PYDANTIC MODELS
# =============================================================================

class StockUpdateRequest(BaseModel):
    """Request model for updating stock."""
    part_number: str
    new_quantity: float
    operation: str  # 'set', 'add', 'subtract'


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_time_greeting() -> str:
    """
    Get time-based greeting.
    
    Returns:
        Greeting message based on current hour
    """
    now = datetime.now()
    current_hour = now.hour
    
    # 05:00-11:59 = Good Morning
    # 12:00-17:59 = Good Afternoon
    # Otherwise (18:00-04:59) = Good Evening
    if 5 <= current_hour < 12:
        return "Good Morning, AISL Aviation Team"
    elif 12 <= current_hour < 18:
        return "Good Afternoon, AISL Aviation Team"
    else:
        return "Good Evening, AISL Aviation Team"


def get_inventory_data() -> Dict[str, List[Dict[str, Any]]]:
    """
    Fetch inventory data from Supabase and group by category.
    
    Returns:
        Dictionary with 'paints' and 'carpets' lists
    """
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("aviation_inventory").select("*").execute()
        
        if not response.data:
            return {"paints": [], "carpets": []}
        
        paints = []
        carpets = []
        
        for item in response.data:
            description = item.get("description", "").upper()
            category = item.get("category", "").lower()
            current_stock = float(item.get("current_stock", 0)) if item.get("current_stock") else 0
            uom = item.get("uom", "")
            
            # Determine stock unit
            stock_unit = uom
            if 'AERMAT' in description or 'CARPET' in description:
                stock_unit = "Linear Meters"
            
            # Check if it's a carpet/flooring item
            is_carpet = category == "carpet" or 'AERMAT' in description or 'CARPET' in description
            
            item_data = {
                "part_number": item.get("part_number", ""),
                "description": item.get("description", ""),
                "current_stock": current_stock,
                "uom": uom,
                "stock_unit": stock_unit,
                "stock_display": f"{current_stock} {stock_unit}" if current_stock > 0 else "Out of Stock",
                "is_available": current_stock > 0,
                # For carpets, add color/type info
                "color_type": get_carpet_color_type(item.get("description", ""))
            }
            
            if is_carpet:
                carpets.append(item_data)
            else:
                paints.append(item_data)
        
        return {
            "paints": paints,
            "carpets": carpets
        }
        
    except Exception as e:
        print(f"Error fetching inventory: {e}")
        return {"paints": [], "carpets": []}


def get_carpet_color_type(description: str) -> str:
    """
    Extract color/type from carpet description.
    
    Args:
        description: Product description
    
    Returns:
        Color/type string (e.g., 'BLUE', 'GREY', 'WOVEN', 'ECONYL RIPS')
    """
    if not description:
        return ""
    
    desc_upper = description.upper()
    
    # Check for AERMAT colors
    if 'AERMAT' in desc_upper:
        if 'BLUE' in desc_upper or '8451' in desc_upper:
            return 'BLUE'
        elif 'GREY' in desc_upper or '992' in desc_upper:
            return 'GREY'
    
    # Check for CARPET types
    if 'CARPET' in desc_upper:
        if 'WOVEN' in desc_upper:
            return 'WOVEN'
        elif 'ECONYL' in desc_upper or 'RIPS' in desc_upper:
            return 'ECONYL RIPS'
    
    return ""


# =============================================================================
# DASHBOARD ROUTES
# =============================================================================

@app.get("/")
async def dashboard(request: Request):
    """
    Main Dashboard page.
    
    Displays welcome message and quick stats.
    """
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "greeting": greeting
        }
    )


@app.get("/sales")
async def sales(request: Request):
    """Sales page."""
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "greeting": greeting,
            "page_title": "Sales",
            "page_icon": "cart3"
        }
    )


@app.get("/purchase-orders")
async def purchase_orders(request: Request):
    """Purchase Orders page."""
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "greeting": greeting,
            "page_title": "Purchase Orders",
            "page_icon": "basket"
        }
    )


@app.get("/completed-orders")
async def completed_orders(request: Request):
    """Completed Orders page."""
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "greeting": greeting,
            "page_title": "Completed Orders",
            "page_icon": "check2-circle"
        }
    )


@app.get("/reports")
async def reports(request: Request):
    """Reports page."""
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "greeting": greeting,
            "page_title": "Reports",
            "page_icon": "graph-up"
        }
    )


@app.get("/stock")
async def stock(request: Request):
    """Stock page - displays inventory from Supabase."""
    greeting = get_time_greeting()
    inventory = get_inventory_data()
    
    return templates.TemplateResponse(
        "stock.html",
        {
            "request": request,
            "greeting": greeting,
            "page_title": "Stock Management",
            "page_icon": "box-seam",
            "paints": inventory["paints"],
            "carpets": inventory["carpets"]
        }
    )


@app.get("/logout")
async def logout(request: Request):
    """
    Logout - clears session cookies and redirects to home page.
    
    Clears authentication tokens (access_token, refresh_token) from cookies
    and redirects user to the home greeting page.
    """
    from fastapi.responses import RedirectResponse
    
    # Create response with redirect to home
    response = RedirectResponse(url="/", status_code=302)
    
    # Clear authentication cookies
    cookie_options = {
        "path": "/",
        "httponly": True,
        "secure": False,  # Set to True in production with HTTPS
        "samesite": "lax"
    }
    
    # Clear common Supabase auth cookies
    response.delete_cookie("access_token", **cookie_options)
    response.delete_cookie("refresh_token", **cookie_options)
    response.delete_cookie("id_token", **cookie_options)
    response.delete_cookie("session", **cookie_options)
    response.delete_cookie("sb-access-token", **cookie_options)
    response.delete_cookie("sb-refresh-token", **cookie_options)
    
    return response


# =============================================================================
# API ENDPOINTS (for AJAX calls)
# =============================================================================

@app.get("/api/greeting")
async def api_greeting():
    """API endpoint to get current greeting."""
    return {"greeting": get_time_greeting()}


@app.get("/api/inventory")
async def api_inventory():
    """API endpoint to get inventory data."""
    inventory = get_inventory_data()
    return {
        "success": True,
        "paints": inventory["paints"],
        "carpets": inventory["carpets"]
    }


@app.post("/api/stock/update")
async def update_stock(request: StockUpdateRequest):
    """
    API endpoint to update stock quantity.
    
    Args:
        request: StockUpdateRequest with part_number, new_quantity, and operation
    
    Returns:
        Success message with updated stock
    """
    supabase = get_supabase_service_client()
    
    try:
        # Get current stock
        response = supabase.table("aviation_inventory").select("current_stock").eq("part_number", request.part_number).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Item not found: {request.part_number}")
        
        current_stock = float(response.data[0].get("current_stock", 0))
        
        # Calculate new stock based on operation
        if request.operation == "set":
            new_stock = request.new_quantity
        elif request.operation == "add":
            new_stock = current_stock + request.new_quantity
        elif request.operation == "subtract":
            new_stock = max(0, current_stock - request.new_quantity)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation. Use 'set', 'add', or 'subtract'")
        
        # Update stock in database
        update_response = supabase.table("aviation_inventory").update({
            "current_stock": new_stock
        }).eq("part_number", request.part_number).execute()
        
        if not update_response.data:
            raise HTTPException(status_code=500, detail="Failed to update stock")
        
        return {
            "success": True,
            "message": f"Stock updated successfully for {request.part_number}",
            "old_stock": current_stock,
            "new_stock": new_stock
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating stock: {str(e)}")


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("Aviation ERP Admin Dashboard Starting...")
    print("=" * 60)
    print(f"\nTemplates Directory: {BASE_DIR / 'templates'}")
    print(f"\nDashboard URL: http://localhost:8000/")
    print(f"Stock Management URL: http://localhost:8000/stock")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
