from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from auth import RequirePrivilege

router = APIRouter(
    prefix="/api/departments",
    tags=["Departments"]
)

@router.post("/", response_model=schemas.DepartmentResponse, status_code=201, dependencies=[Depends(RequirePrivilege('manage:users'))])
def add_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    """
    Add a New Department
    
    Creates a new physical or logical department division in the database.
    """
    db_dept = models.Department(**department.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

@router.get("/", response_model=List[schemas.DepartmentResponse])
def view_all_departments(db: Session = Depends(get_db)):
    """
    View All Departments
    
    Returns the array of active departments. Highly useful for populating dropdown menus on a frontend application.
    """
    return db.query(models.Department).all()
