from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date
from datetime import datetime
from database import Base

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    permissions_level = Column(Integer, default=1)

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    # Logical IDs mirroring Task 2 DB structure (No hard Foreign Keys)
    department_id = Column(Integer, nullable=True)
    role_id = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AssetCategory(Base):
    __tablename__ = "asset_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=True)

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    serial_number = Column(String(100), unique=True, index=True)
    category_id = Column(Integer, nullable=True)
    status = Column(String(50), default='Available')
    purchase_date = Column(Date, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AssetAssignment(Base):
    __tablename__ = "asset_assignments"
    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, nullable=False)
    employee_id = Column(Integer, nullable=False)
    assigned_by_id = Column(Integer, nullable=True)
    assigned_at = Column(DateTime, default=datetime.utcnow)
    returned_at = Column(DateTime, nullable=True)
    assignment_status = Column(String(50), default='Active')
    notes = Column(String, nullable=True)
