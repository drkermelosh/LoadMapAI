#!/usr/bin/env bash

# ===============================
# Setup script for LoadMap AI
# Creates FastAPI project structure
# ===============================

set -e

echo "🚀 Setting up LoadMap AI project structure..."

# Create base folders
mkdir -p app/{api,core,services,models,rules}
mkdir -p uploads
touch app/__init__.py
touch app/api/__init__.py
touch app/core/__init__.py
touch app/services/__init__.py
touch app/models/__init__.py
touch app/rules/__init__.py

# -------- main.py --------
cat > app/main.py << 'EOF'
from fastapi import FastAPI
from app.api import routes_files, routes_jobs, routes_plans

app = FastAPI(
    title="LoadMap AI",
    version="0.1.0",
    description="Engineer-ready tool for generating draft load maps from architectural plans."
)

app.include_router(routes_files.router, prefix="/files", tags=["files"])
app.include_router(routes_jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(routes_plans.router, prefix="/plans", tags=["plans"])

@app.get("/")
def root():
    return {"message": "Welcome to LoadMap AI"}
EOF

# -------- routes_files.py --------
cat > app/api/routes_files.py << 'EOF'
from fastapi import APIRouter, UploadFile, File
import uuid, os

router = APIRouter()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/")
async def upload_plan(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    filepath = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(filepath, "wb") as f:
        f.write(await file.read())
    return {"file_id": file_id, "filename": file.filename}
EOF

# -------- routes_jobs.py --------
cat > app/api/routes_jobs.py << 'EOF'
from fastapi import APIRouter
from pydantic import BaseModel
import uuid

router = APIRouter()

class JobStatus(BaseModel):
    job_id: str
    status: str
    progress: float

@router.post("/parse")
def start_parse(file_id: str):
    return {"job_id": str(uuid.uuid4()), "status": "queued"}

@router.get("/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    return JobStatus(job_id=job_id, status="processing", progress=0.5)
EOF

# -------- routes_plans.py --------
cat > app/api/routes_plans.py << 'EOF'
from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

class Room(BaseModel):
    id: str
    raw_label: str
    category: Optional[str] = None
    confidence: float = 0.0

@router.get("/{plan_id}/rooms", response_model=List[Room])
def get_rooms(plan_id: str):
    return [
        Room(id="1", raw_label="BED", category="ResidentialSleeping", confidence=0.98),
        Room(id="2", raw_label="LIVING", category="ResidentialLiving", confidence=0.95)
    ]
EOF

# -------- settings.py --------
cat > app/core/settings.py << 'EOF'
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "LoadMap AI"
    environment: str = "dev"
    upload_dir: str = "uploads"

settings = Settings()
EOF

# -------- rules_engine.py --------
cat > app/services/rules_engine.py << 'EOF'
import yaml, os

RULES_PATH = os.getenv("RULES_PATH", "app/rules/asce7-22.yml")

def load_rules():
    with open(RULES_PATH, "r") as f:
        return yaml.safe_load(f)

def map_label_to_load(label: str):
    rules = load_rules()
    ab = rules.get("abbrev", {})
    mp = rules.get("mappings", {})
    key = ab.get(label.upper())
    if key and key in mp:
        return mp[key]
    return {"uniform_psf": None, "code_ref": "Unknown"}
EOF

# -------- ASCE 7 rules file --------
cat > app/rules/asce7-22.yml << 'EOF'
version: ASCE7-22
mappings:
  ResidentialSleeping:
    uniform_psf: 30
    code_ref: "ASCE 7-22 Table 4.3-1"
  ResidentialLiving:
    uniform_psf: 40
    code_ref: "ASCE 7-22 Table 4.3-1"
  Office:
    uniform_psf: 50
    code_ref: "ASCE 7-22 Table 4.3-1"
abbrev:
  BR: ResidentialSleeping
  BED: ResidentialSleeping
  LIVING: ResidentialLiving
  OFFICE: Office
EOF

# -------- requirements.txt --------
cat > requirements.txt << 'EOF'
fastapi
uvicorn[standard]
pydantic
PyYAML
EOF

# -------- .gitignore --------
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
.env
.DS_Store
uploads/
EOF

echo "✅ LoadMap AI structure created successfully!"
echo "Next steps:"
echo "1️⃣  python -m venv .venv && source .venv/bin/activate"
echo "2️⃣  pip install -r requirements.txt"
echo "3️⃣  uvicorn app.main:app --reload"
echo "4️⃣  Open http://127.0.0.1:8000/docs"
