from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from auth import RequirePrivilege

router = APIRouter(
    prefix="/api/employees",
    tags=["Employees"]
)

@router.post("/", response_model=schemas.EmployeeResponse, status_code=201, dependencies=[Depends(RequirePrivilege('manage:users'))])
def add_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    """
    Add a New Employee
    
    Registers a new worker into the SQL system. Requires a name and unique email address.
    """
    db_emp = models.Employee(**employee.model_dump())
    try:
        db.add(db_emp)
        db.commit()
        db.refresh(db_emp)
        return db_emp
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating employee. Email might already exist.")

@router.get("/", response_model=List[schemas.EmployeeResponse])
def view_all_employees(db: Session = Depends(get_db)):
    """
    View All Employees
    
    Returns the basic database directory of active and inactive staff members.
    """
    return db.query(models.Employee).all()

@router.get("/{employee_id}", response_model=schemas.EmployeeResponse)
def view_single_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Fetch Single Employee Profile
    
    Finds exact database details for one specific ID. Throws 404 if missing.
    """
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.get("/{employee_id}/assignments", response_model=List[schemas.AssignmentResponse])
def get_employee_active_assets(employee_id: int, db: Session = Depends(get_db)):
    """
    View Active Holding Log for Employee
    
    Queries the assignments log directly to list every asset this user hasn't returned yet.
    """
    assignments = db.query(models.AssetAssignment).filter(
        models.AssetAssignment.employee_id == employee_id,
        models.AssetAssignment.assignment_status == "Active"
    ).all()
    return assignments

@router.delete("/{employee_id}", dependencies=[Depends(RequirePrivilege('manage:users'))])
def deactivate_employee(employee_id: int, db: Session = Depends(get_db)):
    """
    Deactivate Employee
    
    Performs a 'soft-delete'. Instead of erasing data and breaking past audit trails, 
    this simply flips their `is_active` boolean to false.
    """
    emp = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    emp.is_active = False
    db.commit()
    return {"message": f"Employee {employee_id} successfully deactivated."}
