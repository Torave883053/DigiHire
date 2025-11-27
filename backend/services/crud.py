# crud.py
from sqlalchemy.orm import Session
from backend.models.models import Vendor
from backend.schemas.schemas import VendorCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import re


# ------------------------
# GST VALIDATION
# ------------------------
def validate_gst_number(gst_number: str | None) -> bool:
    """Returns True only if GST format is correct OR field is empty."""
    if not gst_number or gst_number.strip() == "":
        return True   # GST is optional

    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return bool(re.match(pattern, gst_number))


# ------------------------
# GET VENDOR BY EMAIL
# ------------------------
def get_vendor_by_email(db: Session, email: str):
    return db.query(Vendor).filter(Vendor.email == email).first()


# ------------------------
# CREATE VENDOR
# ------------------------
def create_vendor(db: Session, vendor_in: VendorCreate):

    if not validate_gst_number(vendor_in.gst_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GST number format"
        )

    vendor = Vendor(
        vendor_name=vendor_in.vendor_name,
        company_name=vendor_in.company_name,
        vendor_mobile=vendor_in.vendor_mobile,
        email=vendor_in.email,
        vendor_type=vendor_in.vendor_type,
        vendor_code=vendor_in.vendor_code,
        gst_number=vendor_in.gst_number,
        website=vendor_in.website,
        status="inactive"   # Default status added
    )

    db.add(vendor)

    try:
        db.commit()
        db.refresh(vendor)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database error: {str(e.orig)}"
        )

    return vendor


# ------------------------
# GET ALL VENDORS
# ------------------------
def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vendor).offset(skip).limit(limit).all()


# ------------------------
# GET VENDOR BY CODE
# ------------------------
def get_vendor_by_code(db: Session, code: str):
    return db.query(Vendor).filter(Vendor.vendor_code == code).first()


# ------------------------
# GET VENDOR BY ID
# ------------------------
def get_vendor_by_id(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()


# ------------------------
# UPDATE VENDOR
# ------------------------
def update_vendor(db: Session, db_vendor: Vendor, vendor_in: VendorCreate):

    if not validate_gst_number(vendor_in.gst_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GST number format"
        )

    # Update fields dynamically, excluding 'status' unless explicitly present
    for key, value in vendor_in.model_dump().items():
        setattr(db_vendor, key, value)

    try:
        db.commit()
        db.refresh(db_vendor)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database error: {str(e.orig)}"
        )

    return db_vendor


# ------------------------
# DELETE VENDOR
# ------------------------
def delete_vendor(db: Session, db_vendor: Vendor):
    db.delete(db_vendor)
    db.commit()
    return {"detail": "Vendor deleted successfully"}
