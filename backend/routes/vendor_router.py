from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])

@vendor_router.post("/", response_model=schemas.VendorOut, status_code=status.HTTP_201_CREATED)
def add_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    existing = crud.get_vendor_by_code(db, vendor.vendor_code)
    if existing:
        raise HTTPException(status_code=400, detail="Vendor code already exists")
    return crud.create_vendor(db, vendor)

@vendor_router.get("/", response_model=list[schemas.VendorOut])
def list_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vendors(db, skip=skip, limit=limit)
