from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
import models

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
    """
    MOCK JWT PARSER: 
    To satisfy the professor's RBAC requirements without the complexity of JWT encryption setups, 
    the Token natively IS the numerical employee ID.
    Example frontend request: 'Authorization: Bearer 1' -> Authenticates as employee ID 1 (Admin/HR).
    """
    token = credentials.credentials
    try:
        user_id = int(token)
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token constraint. Mock token must be a valid Employee ID.")
    
    user = db.query(models.Employee).filter(models.Employee.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User/Employee not found")
        
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is deactivated")
        
    return user

class RequirePrivilege:
    """
    Core Dependency generator for Role-Based Access Control (RBAC).
    Usage Example: @router.delete("/", dependencies=[Depends(RequirePrivilege('delete:asset'))])
    """
    def __init__(self, required_privilege: str):
        self.required_privilege = required_privilege

    def __call__(self, current_user: models.Employee = Depends(get_current_user), db: Session = Depends(get_db)):
        if not current_user.role_id:
            raise HTTPException(status_code=403, detail="Fatal Auth Error: User has no assigned role.")
            
        role = db.query(models.Role).filter(models.Role.id == current_user.role_id).first()
        if not role:
            raise HTTPException(status_code=403, detail="Fatal Auth Error: Integrity Error, Assigned role not found in DB.")
            
        # Parse comma-separated permissions string (e.g., "view:asset,delete:asset") safely
        permissions = [p.strip() for p in role.permissions.split(",")] if role.permissions else []
        
        # Guard Check
        if self.required_privilege not in permissions:
            raise HTTPException(
                status_code=403, 
                detail=f"RBAC Access Denied: Missing required organizational privilege '{self.required_privilege}'"
            )
            
        return current_user
