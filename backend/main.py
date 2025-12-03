from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.db.database import engine, Base
import backend.models.models as models
from backend.api.vendor_router import vendor_router

app = FastAPI(title="DigiHire Backend")

# Allow CORS for frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include Routers
app.include_router(vendor_router)

@app.get("/")
def root():
    return {"message": "Vendor & Auth API running successfully 🚀"}
