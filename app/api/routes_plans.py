from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel

from app.services.rules_engine import category_to_load, label_to_category


router = APIRouter()

class RoomOut(BaseModel):
    id: str
    raw_label: str
    category: Optional[str] = None
    load: Optional[dict] = None
    confidence: float = 0.0
    needs_review: bool = False
    # polygon: list | None = None  # add later when geometry is ready

# Temporary Stub: Pretend the following rooms came from a pdf or CAD parser

_FAKE_ROOMS = [
    {"id": "1", "raw_label": "BED",    "confidence": 0.98},
    {"id": "2", "raw_label": "LIVING", "confidence": 0.95},
    {"id": "3", "raw_label": "MECH",   "confidence": 0.92},  # not in abbrev yet
]

@router.get("/{plan_id}/rooms", response_model=List[RoomOut])
def get_rooms(plan_id: str):
    out: List[RoomOut] = []

    for r in _FAKE_ROOMS:
        cat = label_to_category(r["raw_label"])
        load = category_to_load(cat) if cat else None
        needs_review = (load is None) or (r["confidence"] < 0.90)
        out.append(RoomOut(
            id=r["id"],
            raw_label=r["raw_label"],
            category=cat,
            load=load,
            confidence=r["confidence"],
            needs_review=needs_review,
        ))
        return out
        