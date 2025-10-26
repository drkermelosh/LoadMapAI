from typing import List, Dict
from app.models.schemas import RoomOut

_FAKE_DB_: Dict[str, List[RoomOut]] = {}

def seed_rooms(plan_id: str):
    """Seed fake data for testing"""
    if plan_id in _FAKE_DB_:
        return
    _FAKE_DB_[plan_id] = [
        RoomOut(id= "1", plan_id=plan_id, raw_label= "BED",    confidence= 0.98),
        RoomOut(id= "2", plan_id=plan_id, raw_label= "LIVING", confidence= 0.95),
        RoomOut(id= "3", plan_id=plan_id, raw_label= "OFC",   confidence= 0.92),
        ]
    
def get_rooms(plan_id: str) -> List[RoomOut]:
    """Return all rooms for a given plan_id"""
    return _FAKE_DB_.get(plan_id, [])