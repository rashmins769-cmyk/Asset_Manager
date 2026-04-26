from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/assignments",
    tags=["Assignments"]
)

@router.post("/", response_model=schemas.AssignmentResponse, status_code=201)
def assign_asset(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    """
    Assign an Item to an Employee (Check-out)
    
    Creates a transaction log of who holds what. 
    **Crucial Database Action Identified in Task 4:** This endpoint simultaneously locates the linked `Asset` in the database 
    and automatically flips its 'status' state to 'Assigned'.
    """
    # 1. Verify physical asset exists
    asset = db.query(models.Asset).filter(models.Asset.id == assignment.asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
        
    if asset.status == "Assigned":
        raise HTTPException(status_code=400, detail="Asset is already marked as 'Assigned' to someone else!")
        
    # 2. Proceed to create assignment event
    db_assignment = models.AssetAssignment(**assignment.model_dump())
    db.add(db_assignment)
    
    # 3. Update physical asset state concurrently
    asset.status = "Assigned"
    
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.put("/{assignment_id}/return", response_model=schemas.AssignmentResponse)
def return_asset(assignment_id: int, db: Session = Depends(get_db)):
    """
    Return an Assigned Item (Check-in)
    
    Logs the exact timestamp the asset was handed back and sets its condition back to 'Available' stock.
    
    - **assignment_id**: The specific ID of the checkout receipt/log, NOT the asset ID.
    """
    db_assignment = db.query(models.AssetAssignment).filter(models.AssetAssignment.id == assignment_id).first()
    if not db_assignment:
        raise HTTPException(status_code=404, detail="Assignment record not found")
        
    # Update assignment history row
    db_assignment.returned_at = datetime.utcnow()
    db_assignment.assignment_status = "Returned"
    
    # Locate linked physical asset and free it up
    asset = db.query(models.Asset).filter(models.Asset.id == db_assignment.asset_id).first()
    if asset:
        asset.status = "Available"
        
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=List[schemas.AssignmentResponse])
def view_all_assignments(db: Session = Depends(get_db)):
    """
    View Historical Audit Log
    
    Returns the entirety of 'Check-in' and 'Check-out' lifecycle receipts recorded in the database.
    Highly useful for exporting to CSVs or generating Admin usage overviews.
    """
    return db.query(models.AssetAssignment).all()
