from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.db.database import get_db
import backend.services.crud as crud, backend.schemas.schemas as schemas

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])




# -------------------------------------------------------------
# ADD NEW VENDOR
# -------------------------------------------------------------
@vendor_router.post("/", response_model=schemas.VendorOut, status_code=status.HTTP_201_CREATED)
def add_vendor(vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    
    existing_code = crud.get_vendor_by_code(db, vendor.vendor_code)
    if existing_code:
        raise HTTPException(status_code=400, detail="Vendor code already exists")

    existing_email = crud.get_vendor_by_email(db, vendor.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    return crud.create_vendor(db, vendor)
    

# -------------------------------------------------------------
# GET ALL VENDORS
# -------------------------------------------------------------
@vendor_router.get("/", response_model=list[schemas.VendorOut])
def list_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vendors(db, skip=skip, limit=limit)


# -------------------------------------------------------------
# UPDATE VENDOR
# -------------------------------------------------------------
@vendor_router.put("/{vendor_id}", response_model=schemas.VendorOut)
def update_vendor(vendor_id: int, vendor: schemas.VendorCreate, db: Session = Depends(get_db)):
    
    db_vendor = crud.get_vendor_by_id(db, vendor_id)
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if vendor.email != db_vendor.email:
        existing_email = crud.get_vendor_by_email(db, vendor.email)
        if existing_email:
            raise HTTPException(status_code=400, detail="Email already exists")

    if vendor.vendor_code != db_vendor.vendor_code:
        existing_code = crud.get_vendor_by_code(db, vendor.vendor_code)
        if existing_code:
            raise HTTPException(status_code=400, detail="Vendor code already exists")

    return crud.update_vendor(db, db_vendor, vendor)


# -------------------------------------------------------------
# DELETE VENDOR
# -------------------------------------------------------------
@vendor_router.delete("/{vendor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vendor(vendor_id: int, db: Session = Depends(get_db)):
    
    db_vendor = crud.get_vendor_by_id(db, vendor_id)
    if not db_vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    crud.delete_vendor(db, db_vendor)
    return {"message": "Vendor deleted successfully"}


# -------------------------------------------------------------
# UPDATE ONLY VENDOR STATUS (Active / Inactive)
# -------------------------------------------------------------
@vendor_router.patch("/{vendor_id}/status")
def update_vendor_status(vendor_id: int, status: str, db: Session = Depends(get_db)):
    vendor = crud.get_vendor_by_id(db, vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")

    if status.lower() not in ["active", "inactive"]:
        raise HTTPException(status_code=400, detail="Status must be 'active' or 'inactive'")

    vendor.status = status.lower()
    db.commit()
    db.refresh(vendor)

    return {"message": "Status updated successfully", "status": vendor.status}

