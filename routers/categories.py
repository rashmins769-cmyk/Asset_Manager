from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db
from auth import RequirePrivilege

router = APIRouter(
    prefix="/api/categories",
    tags=["Asset Categories"]
)

@router.post("/", response_model=schemas.CategoryResponse, status_code=201, dependencies=[Depends(RequirePrivilege('manage:inventory'))])
def add_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Add a New Asset Category
    
    Creates a grouping classification bucket like "Software Licenses" or "Laptops" for easier inventory management.
    """
    db_cat = models.AssetCategory(**category.model_dump())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@router.get("/", response_model=List[schemas.CategoryResponse])
def view_all_categories(db: Session = Depends(get_db)):
    """
    View All Categories
    
    Retrieves the global list of asset categories for frontend sorting and filtering.
    """
    return db.query(models.AssetCategory).all()
