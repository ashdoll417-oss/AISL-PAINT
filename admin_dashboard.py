"""
FastAPI Admin Dashboard Application
Uses Jinja2 templates for rendering the admin interface
"""

from fastapi import FastAPI, Request, templating
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pathlib import Path

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
    """Stock page."""
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "page.html",
        {
            "request": request,
            "greeting": greeting,
            "page_title": "Stock",
            "page_icon": "box-seam"
        }
    )


@app.get("/logout")
async def logout(request: Request):
    """Logout - redirects to dashboard."""
    greeting = get_time_greeting()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "greeting": greeting
        }
    )


# =============================================================================
# API ENDPOINTS (for AJAX calls)
# =============================================================================

@app.get("/api/greeting")
async def api_greeting():
    """API endpoint to get current greeting."""
    return {"greeting": get_time_greeting()}


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
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
