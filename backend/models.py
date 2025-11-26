# models.py
from sqlalchemy import Column, Integer, String
from database import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    vendor_mobile = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    vendor_type = Column(String(100), nullable=False)
    vendor_code = Column(String(100), unique=True, nullable=False)
    gst_number = Column(String(50), nullable=True)
    website = Column(String(255), nullable=True)
    password = Column(String(255), nullable=True)

    # ⭐ NEW FIELD FOR TOGGLE STATUS
    status = Column(String(20), default="inactive")   # active / inactive


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
