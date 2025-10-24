from __future__ import annotations
from typing import List, Tuple, Optional, Literal, Dict
from pydantic import BaseModel, Field

try:
    # pydantic v2
    from pydantic import ConfigDict
    V2 = True

except Exception: 
    V2 = False


# Common type aliases
Coord = Tuple[float, float]
Polygon = List[Coord]

# Plans
class PlanIn(BaseModel):
    name: str = Field(..., description="Human-readable plan name (unique-ish)")
    width: float = Field(..., gt=0, description="Plan width in same units as geometry")
    height: float = Field(..., gt=0, description="Plan height in same units as geometry")

class PlanOut(PlanIn):
    id: str = Field(..., description="Stable plan identifier (slug)")


# Rooms
class RoomOut(BaseModel):
    id: str
    plan_id: str
    raw_label: str
    name: str
    category: Optional[str] = None
    load: Optional[Dict] = None
    confidence: float = 0.0
    needs_review: bool = False
    area_sf: float = Field(..., ge=0)
    # boundary: Optional[Polygon] = Field(..., description="Room polygon as [(x,y),...]")
    # room_type: Optional[str] = Field(None, description="Semantic Label, e.g., office, corridor, bedroom")
    # centroid: Optional[Coord] = Field(None, description="(x,y) centroid of room polygon")
    # load_zone: Optional[Literal["A", "B", "C", "D"]] = Field(
        # None, description="Optional load category for downstream mapping")
    # overlay_url: Optional[str] = Field(None, description="Optional image/titles URL for front-end overlay")

    # pydantic v2 compatibility for ORM if needed

    if 'ConfigDict' in globals():
        model_config = ConfigDict(from_attributes=True)
    else:  # Pydantic v1 fallback
        class Config:
            orm_mode = True