from __future__ import annotations
from enum import Enum
from typing import Any, List, Tuple, Optional, Literal, Dict
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
    category: Optional[str] = None
    load: Optional[Dict] = None
    confidence: float = 0.0
    needs_review: bool = False

class SortBy(str, Enum):
    raw_label = "raw_label"
    category = "category"
    confidence = "confidence"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

class RoomsMeta(BaseModel):
    total: int = Field(..., description="Total number of rooms available for plan before filters")
    count: int = Field(..., description="Number of rooms returned in this response (after fileters, after pagination)")
    limit: int = Field(..., ge=1, description="Limit/number of rooms requested")
    offset: int = Field(..., ge=0, description="The starting index of the returned rooms")
    next_offset: Optional[int] = Field(None, description="Offset for next page if any")
    reviewed: int = Field(..., description="Rooms not needing review in filtered set (pre-pagination)")
    needs_review: int = Field(..., description="Rooms needing review in filtered set (pre-pagination)")
    sort_by: SortBy
    sort_order: SortOrder
    filters: Dict[str, Any]

class RoomsResponse(BaseModel):
    items: List[RoomOut]
    meta: RoomsMeta