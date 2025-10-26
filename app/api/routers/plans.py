from fastapi import APIRouter, HTTPException
from typing import List
from app.models.schemas import PlanIn, PlanOut
from app.services.repositories import plans_repo

router = APIRouter( tags=["plans"])

@router.post("", response_model=PlanOut, status_code=201)
def create_plan(plan_in: PlanIn):
    try:
        return plans_repo.create_plan(plan_in)
    except ValueError:
        raise HTTPException(status_code=400, detail="Plan with this name already exists")   
    
@router.get("", response_model=List[PlanOut])
def list_plans():
    return plans_repo.list_all()

@router.get("/{plan_id}", response_model=PlanOut)
def get_plan(plan_id: str):
    plan = plans_repo.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan