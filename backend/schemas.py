from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class VendorBase(BaseModel):
    vendor_name: str = Field(..., example="Rahul Recruiters")
    company_name: str = Field(..., example="Rahul Corp")
    vendor_mobile: str = Field(..., example="+91-9999999999")
    email: EmailStr
    vendor_type: str = Field(..., example="Recruitment Agency")
    gst_number: Optional[str] = None
    website: Optional[str] = None


class VendorCreate(VendorBase):
    vendor_code: str = Field(..., example="VEND-001")
    # No status here → Frontend does not send it


class VendorOut(VendorBase):
    id: int
    vendor_code: str
    status: str   # ⭐ Added field

    class Config:
        orm_mode = True


class PasswordResetRequest(BaseModel):
    """Schema for requesting a password reset email"""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Schema for confirming password reset with new password"""
    token: str
    new_password: str
