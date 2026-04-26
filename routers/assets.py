from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import get_db

router = APIRouter(
    prefix="/api/assets",
    tags=["Assets"]
)

@router.post("/", response_model=schemas.AssetResponse, status_code=201)
def add_new_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    """
    Add a New Asset to Inventory
    
    Creates a new physical asset row in the database.
    
    - **name**: Identifier of the physical asset (e.g. MacBook Pro).
    - **serial_number**: Unique identifier or company tag ID.
    - **category_id**: Links to predefined asset categories.
    - **status**: Defaults to 'Available' but can be overridden.
    
    Returns the newly generated asset object including its exact database ID.
    """
    db_asset = models.Asset(**asset.model_dump())
    try:
        db.add(db_asset)
        db.commit()
        db.refresh(db_asset)
        return db_asset
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail="Error creating asset. Serial number likely taken.")

@router.get("/", response_model=List[schemas.AssetResponse])
def view_all_assets(db: Session = Depends(get_db)):
    """
    View All Assets
    
    Fetches the entire catalog of physical assets in the company system.
    Returns a list of Asset schema objects.
    """
    return db.query(models.Asset).all()

@router.get("/{asset_id}", response_model=schemas.AssetResponse)
def view_specific_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    View a Specific Asset's Details
    
    Supply the unique internal integer ID to look up an exact physical instance.
    Throws a 404 error if the asset cannot be found in the SQL database.
    """
    asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset

@router.put("/{asset_id}", response_model=schemas.AssetResponse)
def edit_asset_details(asset_id: int, asset_data: schemas.AssetCreate, db: Session = Depends(get_db)):
    """
    Edit an Asset's Core Details
    
    Used to fully update fields such as fixing a misspelled name, altering the serial number, 
    or modifying purchase dates. Completely overwrites the existing row data.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    for key, value in asset_data.model_dump().items():
        setattr(db_asset, key, value)
    
    db.commit()
    db.refresh(db_asset)
    return db_asset

@router.patch("/{asset_id}/status", response_model=schemas.AssetResponse)
def update_asset_status(asset_id: int, status_update: schemas.AssetStatusUpdate, db: Session = Depends(get_db)):
    """
    Update an Asset's Physical Status
    
    A partial update method (PATCH) designed explicitly to cleanly mark an item as 
    'Retired', 'In Maintenance', 'Lost', etc., without needing to re-submit the full asset data payload.
    """
    db_asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    
    db_asset.status = status_update.status
    db.commit()
    db.refresh(db_asset)
    return db_asset
