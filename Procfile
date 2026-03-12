# Aviation ERP Dual Deploy (Render)
# FastAPI Staff App (Port $PORT) + Flask Admin App

# Staff/Sales Frontend (existing FastAPI)
web: uvicorn main:app --host 0.0.0.0 --port $PORT

# Admin Dashboard (Flask + Gunicorn)
admin: gunicorn app:app --bind 0.0.0.0:$PORT

# Admin Dashboard (Flask development - local testing only)
# admin: python app.py
