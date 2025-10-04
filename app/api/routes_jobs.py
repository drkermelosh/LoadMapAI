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
