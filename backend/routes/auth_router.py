# routers/auth_router.py
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from database import get_db
from models import Vendor
from schemas import PasswordResetRequest, PasswordResetConfirm
from utils import create_reset_token, verify_reset_token
from email_utils import send_reset_email

from passlib.context import CryptContext

auth_router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@auth_router.post("/password-reset-request")
def password_reset_request(request: PasswordResetRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(Vendor).filter(Vendor.email == request.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email not found")





    token = create_reset_token(user.email)
    reset_link = f"http://localhost:3000/reset-password/{token}"

    send_reset_email(background_tasks, user.email, user.email,"DIGI@"+user.email)
    user.password = pwd_context.hash("DIGI@"+user.email)
    db.commit()
    return {"message": "Welcome email sent"}

@auth_router.post("/password-reset-confirm")
def password_reset_confirm(data: PasswordResetConfirm, db: Session = Depends(get_db)):


    email = verify_reset_token(data.token)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

    user = db.query(Vendor).filter(Vendor.email == email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.password = pwd_context.hash(data.new_password)
    db.commit()
    return {"message": "Password has been reset successfully"}
