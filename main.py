from fastapi import FastAPI
from database import engine, Base
from routers import assets, assignments, employees, categories, departments

# Automatically generate all SQLite database tables modeled in models.py on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AssetLink API Ecosystem",
    description="Professional Enterprise Asset Management API endpoints mapped perfectly to the API Design Sheet. Features atomic CRUD actions spanning personnel and physical asset distribution.",
    version="1.0.0"
)

# Connect all modular endpoints to the central application
app.include_router(departments.router)
app.include_router(categories.router)
app.include_router(employees.router)
app.include_router(assets.router)
app.include_router(assignments.router)

@app.get("/", tags=["System"])
def read_root():
    return {"message": "Welcome to AssetLink API! Navigate your browser to /docs to experiment with the interactive Swagger validation UI."}
