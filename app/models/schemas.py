from __future__ import annotations
from enum import Enum
from typing import Any, List, Tuple, Optional, Literal, Dict
from pydantic import BaseModel, Field, ConfigDict

V2 = False
try:
    # Attempt to import Pydantic V2 features
    from pydantic import ConfigDict, model_validator
    V2 = True
    CONFIG_CLASS = ConfigDict(from_attributes=True, extra='allow')
except ImportError: 
    # Fallback for Pydantic V1
    CONFIG_CLASS = type('Config', (object,), {'orm_mode': True, 'extra': 'allow'})
    # Note: We don't import ConfigDict in V1, so we handle model_config below

# Common type aliases
Coord = Tuple[float, float]
Polygon = List[Coord]

# Plans
class PlanIn(BaseModel):
    name: str = Field(..., description="Human-readable plan name (unique-ish)")
    width: float = Field(..., gt=0, description="Plan width in same units as geometry")
    height: float = Field(..., gt=0, description="Plan height in same units as geometry")

    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass

class PlanOut(PlanIn):
    id: str = Field(..., description="Stable plan identifier (slug)")
    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass

class PlansMeta(BaseModel):
    total: int = Field(..., description="Total number of plans available")
    count: int = Field(..., description="Number of plans returned in this response (after filters, after pagination)")
    limit: int = Field(..., ge=1, description="limit/number of plans requested")
    offset: int = Field(..., ge=0, description="The starting index of the returned plans")
    next_offset: Optional[int] = None
    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass

class PlansResponse(BaseModel):
    items: List[PlanOut]
    meta: PlansMeta
    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass

# Rooms
class RoomOut(BaseModel):
    id: str
    plan_id: str
    raw_label: str
    category: Optional[str] = None
    load: Optional[Dict] = None
    confidence: float = 0.0
    needs_review: bool = False
    
    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass

class RoomsMeta(BaseModel):
    total: int = Field(..., description="Total number of rooms available for plan before filters")
    count: int = Field(..., description="Number of rooms returned in this response (after fileters, after pagination)")
    limit: int = Field(..., ge=1, description="Limit/number of rooms requested")
    offset: int = Field(..., ge=0, description="The starting index of the returned rooms")
    next_offset: Optional[int] = Field(None, description="Offset for next page if any")
    reviewed: int = Field(..., description="Rooms not needing review in filtered set (pre-pagination)")
    needs_review: int = Field(..., description="Rooms needing review in filtered set (pre-pagination)")
    filters: Dict[str, Any]
    
    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass

class RoomsResponse(BaseModel):
    items: List[RoomOut]
    meta: RoomsMeta

    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass   

# Unified Error Payload
class ErrorResponse(BaseModel):
    error: dict = Field(..., description= '{"code":<int>, "message":<str>}')

    # V2 Configuration
    if V2:
        model_config = ConfigDict(from_attributes=True, extra='allow')
    # V1 Configuration
    else:
        class Config(CONFIG_CLASS): # type: ignore
            pass