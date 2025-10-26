from typing import Dict, List, Optional
from app.models.schemas import PlanIn, PlanOut


_PLANS: Dict[str, PlanOut] = {}

def slugify(name: str) -> str:
    """Generate a simple slug from a name"""
    return "-".join(name.strip().lower().split())

def create_plan(plan_in: PlanIn) -> PlanOut:
    plan_id = slugify(plan_in.name)
    if plan_id in _PLANS:
        raise ValueError("Plan with this name already exists")
    plan_out = PlanOut(id=plan_id, **plan_in.model_dump())
    _PLANS[plan_id] = plan_out
    return plan_out

def get(plan_id: str) -> Optional[PlanOut]:
    return _PLANS.get(plan_id)

def list_all() -> List[PlanOut]:
    return list(_PLANS.values())