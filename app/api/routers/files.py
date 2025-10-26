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
    return {"file_id": file_id, "filename": file.filename, "filepath": filepath}
