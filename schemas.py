from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date

"""
This file contains the Pydantic schemas. 
They are heavily documented with docstrings and Field descriptions to ensure the Swagger UI is highly professional and informative.
"""

# --- Department Schemas ---
class DepartmentBase(BaseModel):
    """Base fields for a Department"""
    name: str = Field(..., description="The exact name of the department, e.g., 'Human Resources'")

class DepartmentCreate(DepartmentBase):
    """Schema for creating a new Department via POST requests."""
    pass

class DepartmentResponse(DepartmentBase):
    """Schema representing the API response for a fetched Department."""
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

# --- Employee Schemas ---
class EmployeeBase(BaseModel):
    """Base fields representing an employee."""
    first_name: str = Field(..., description="The employee's first name")
    last_name: str = Field(..., description="The employee's last name")
    email: str = Field(..., description="A unique company email address")
    department_id: Optional[int] = Field(None, description="Logical link to the departments table")
    role_id: Optional[int] = Field(None, description="Logical link to the roles table")

class EmployeeCreate(EmployeeBase):
    """Schema detailing required fields to create an employee."""
    pass

class EmployeeResponse(EmployeeBase):
    """Schema formatting the database Employee model for client consumption."""
    id: int
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

# --- Asset Category Schemas ---
class CategoryBase(BaseModel):
    name: str = Field(..., description="Name of the category, e.g., 'Laptop', 'Monitor'")
    description: Optional[str] = Field(None, description="More details about the category")

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

# --- Asset Schemas ---
class AssetBase(BaseModel):
    """Base Asset schema details."""
    name: str = Field(..., description="Physical name or model identifier of the asset")
    serial_number: str = Field(..., description="Unique barcode or serial code")
    category_id: Optional[int] = Field(None, description="Logical foreign key linking to a category id")
    status: str = Field("Available", description="Current condition, e.g., Available, Assigned, Retired")
    purchase_date: Optional[date] = Field(None, description="Date of physical purchase")
    notes: Optional[str] = Field(None, description="Any additional quirks or damage notes")

class AssetCreate(AssetBase):
    """Payload to add a new physical asset into the system."""
    pass

class AssetResponse(AssetBase):
    """API read representation of a physical asset."""
    id: int
    created_at: datetime
    class Config:
        from_attributes = True

class AssetStatusUpdate(BaseModel):
    """Payload specifically designed for PATCH requests to alter item statuses."""
    status: str = Field(..., description="New string status, like 'In Maintenance' or 'Retired'")

# --- Assignment (Check-in/Check-out) Schemas ---
class AssignmentCreate(BaseModel):
    """Payload containing everything required to execute a Check-Out action."""
    asset_id: int = Field(..., description="ID of the asset being given to an employee")
    employee_id: int = Field(..., description="ID of the employee taking the asset")
    assigned_by_id: Optional[int] = Field(None, description="ID of Admin/HR authorizing this")
    notes: Optional[str] = Field(None, description="Initial check-out condition notes")

class AssignmentResponse(BaseModel):
    """Response structure of an assignment audit event."""
    id: int
    asset_id: int
    employee_id: int
    assigned_by_id: Optional[int]
    assigned_at: datetime
    returned_at: Optional[datetime]
    assignment_status: str
    notes: Optional[str]
    class Config:
        from_attributes = True
