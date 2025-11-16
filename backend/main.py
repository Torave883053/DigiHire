from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routes.vendor_router import vendor_router
from routes.auth_router import auth_router  # 👈 import your new auth router

app = FastAPI(title="DigiHire Backend")

# ✅ Allow CORS for your frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ✅ Add middleware BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # Allowed frontend origins
    allow_credentials=True,         # Allow cookies/auth headers
    allow_methods=["*"],            # Allow all HTTP methods
    allow_headers=["*"],            # Allow all headers
)

# ✅ Create all database tables
Base.metadata.create_all(bind=engine)

# ✅ Include routers
app.include_router(vendor_router)
app.include_router(auth_router)     # 👈 add this for password reset and auth

@app.get("/")
def root():
    return {"message": "Vendor & Auth API running successfully 🚀"}
