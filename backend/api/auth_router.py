# routers/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.models.models import Vendor
from backend.schemas.schemas import PasswordResetRequest, PasswordResetConfirm
from backend.utils.utils import create_reset_token, verify_reset_token
from backend.services.email_utils import send_reset_email
from passlib.context import CryptContext
import random
import string

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


# ---------------------------------------------------------
# ENVIRONMENT MODE (CHANGE THIS ONLY)
# ---------------------------------------------------------
# "LOCAL" → http://company.localhost:3000/login
# "PRODUCTION" → https://company.digihire.com/login
ENV_MODE = "LOCAL"     # Change to PRODUCTION when deploying


# ---------------------------------------------------------
# RANDOM PASSWORD GENERATOR
# ---------------------------------------------------------
def generate_random_password(length: int = 10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# ---------------------------------------------------------
# SEND LOGIN DETAILS INSERTED FROM VENDOR FORM
# ---------------------------------------------------------
@auth_router.post("/password-reset-request")
def password_reset_request(
    request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    # Check if vendor exists
    user = db.query(Vendor).filter(Vendor.email == request.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not found"
        )

    # Create token (optional future use)
    token = create_reset_token(user.email)

    # -------------------------------------------------
    # CREATE COMPANY SUBDOMAIN
    # -------------------------------------------------
    company_slug = user.company_name.lower().replace(" ", "")

    # -------------------------------------------------
    # LOGIN URL BASED ON MODE
    # -------------------------------------------------
    if ENV_MODE == "LOCAL":
        # Example → http://capgemini.localhost:3000/login
        login_url = f"http://{company_slug}.localhost:3000/login"
    else:
        # Example → https://capgemini.digihire.com/login
        login_url = f"https://{company_slug}.digihire.com/login"

    # -------------------------------------------------
    # GENERATE RANDOM PASSWORD AND SAVE
    # -------------------------------------------------
    random_password = generate_random_password()
    user.password = pwd_context.hash(random_password)
    db.commit()

    # -------------------------------------------------
    # SEND EMAIL
    # -------------------------------------------------
    send_reset_email(
        background_tasks,
        to_email=user.email,
        Username=user.email,
        Password=random_password,
        LoginURL=login_url,
        VendorName=user.vendor_name        # <-- ADDED FOR EMAIL GREETING
    )

    return {"message": "Vendor login details sent successfully"}


# ---------------------------------------------------------
# CONFIRM PASSWORD RESET
# ---------------------------------------------------------
@auth_router.post("/password-reset-confirm")
def password_reset_confirm(
    data: PasswordResetConfirm,
    db: Session = Depends(get_db)
):

    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired token"
        )

    user = db.query(Vendor).filter(Vendor.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.password = pwd_context.hash(data.new_password)
    db.commit()

    return {"message": "Password has been reset successfully"}
