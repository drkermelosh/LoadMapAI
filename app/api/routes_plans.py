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
