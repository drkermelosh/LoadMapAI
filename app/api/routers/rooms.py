from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import RoomOut
from app.services.rules.rules_engine import label_to_category, category_to_load


router = APIRouter(prefix="/plans", tags=["rooms"])

# stub data just for prototyping
_FAKE_ROOMS = [
    {"id": "1", "raw_label": "BED",    "confidence": 0.98},
    {"id": "2", "raw_label": "LIVING", "confidence": 0.95},
    {"id": "3", "raw_label": "MECH",   "confidence": 0.92},
]

@router.get("/{plan_id}/rooms", response_model=List[RoomOut])
def get_rooms(plan_id: str):
    out: List[RoomOut] = []
    for r in _FAKE_ROOMS:
        cat = label_to_category(r["raw_label"])
        load = category_to_load(cat) if cat else None
        needs_review = (load is None) or (r["confidence"] < 0.90)
        
        out.append(
            RoomOut(
                id=r["id"],
                plan_id=plan_id,
                raw_label=r["raw_label"],
                category=cat,
                load=load,
                confidence=r["confidence"],
                needs_review=needs_review,
            )
        )
    return out