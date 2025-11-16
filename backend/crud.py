# crud.py
from sqlalchemy.orm import Session
from models import Vendor
from schemas import VendorCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
import re

import re

def validate_gst_number(gst_number: str) -> bool:
    """
    Validate an Indian GST number.

    Format: 15 characters total
      - 2 digits for state code
      - 10 characters for PAN (5 letters, 4 digits, 1 letter)
      - 1 entity code (alphanumeric)
      - 1 'Z' by default
      - 1 checksum character (alphanumeric)

    Example: 27AAPFU0939F1ZV
    """
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return True



def create_vendor(db: Session, vendor_in: VendorCreate):
    # Validate GST Number
    if not validate_gst_number(vendor_in.gst_number):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid GST number format"
        )

    # Create Vendor object
    vendor = Vendor(
        vendor_name=vendor_in.vendor_name,
        company_name=vendor_in.company_name,
        vendor_mobile=vendor_in.vendor_mobile,
        email=vendor_in.email,
        vendor_type=vendor_in.vendor_type,
        vendor_code=vendor_in.vendor_code,
        gst_number=vendor_in.gst_number,
        website=vendor_in.website,
    )

    db.add(vendor)
    try:
        db.commit()
        db.refresh(vendor)
    except IntegrityError as e:
        db.rollback()
        # Handle duplicate or constraint errors
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Database integrity error: {str(e.orig)}"
        )

    return vendor

def get_vendors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Vendor).offset(skip).limit(limit).all()

def get_vendor_by_code(db: Session, code: str):
    return db.query(Vendor).filter(Vendor.vendor_code == code).first()
