from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import RoomOut
from app.services.repositories import rooms_repo
from app.services.rules.rules_engine import label_to_category, category_to_load


router = APIRouter(prefix="/plans", tags=["rooms"])

@router.get("/{plan_id}/rooms", response_model=List[RoomOut])
def get_rooms(plan_id: str):
    rooms_repo.seed_rooms(plan_id) # seed stub data if not already
    rooms = rooms_repo.get_rooms(plan_id)

    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found for this plan")
    
    out: List[RoomOut] = []
    for r in rooms:
        cat = label_to_category(r.raw_label)
        load = category_to_load(cat) if cat else None
        needs_review = (load is None) or (r.confidence < 0.90)
        
        out.append(
            RoomOut(
                id=r.id,
                plan_id=r.plan_id,
                raw_label=r.raw_label,
                category=cat,
                load=load,
                confidence=r.confidence,
                needs_review=needs_review,
            )
        )
    return out