from fastapi import APIRouter, HTTPException, Query
from typing import List, Literal
from app.models.schemas import ErrorResponse, PlanIn, PlanOut, PlansMeta, PlansResponse, V2
from app.services.repositories import plans_repo

router = APIRouter( tags=["plans"])

PlanSortBy = Literal["name", "width", "height"]
PlanSortOrder = Literal["asc", "desc"]

@router.post(
        "",
        response_model=PlanOut, 
        status_code=201,
        responses={409: {"model": ErrorResponse}},
        summary="Create a new plan"
)

def create_plan(plan_in: PlanIn):
    try:
        return plans_repo.create_plan(plan_in)
    except ValueError:
        raise HTTPException(status_code=400, detail="Plan with this name already exists")   
    
@router.get(
        "", 
        response_model=List[PlanOut],
        summary="List plan with pagination and sorting",
        responses={},
)

def list_plans(
    sort_by: PlanSortBy = Query(
        "name",
        description="Sort key: name, width, or height",
        example={"by_name": {"value": "name"}},
    ),

    sort_order: PlanSortOrder = Query(
        "asc",
        description="Sort order: asc or desc",
        example={"ascending": {"value": "asc"}, "descending": {"value": "desc"}},
    ),

    limit: int = Query(
        50, ge=1, le=100,
        description="Number of plans to return",
        example={"small_page": {"value": 10}, "large_page": {"value": 100}},
    ),

    offset: int = Query(
        0, ge=0,
        description="Offset for pagination",
        example={"second_page": {"value": 10}},
    
    )
    
):

    items: List[PlanOut] = plans_repo.list_all()
    total = len(items)

    #Sorting
    reverse = sort_order == "desc"
    key_map = {
        "name": lambda p: p.name.lower(),
        "width": lambda p: p.width,
        "height": lambda p: p.height,
    }

    items.sort(key=key_map[sort_by], reverse= reverse)

    #Pagination
    slice_start = offset
    slice_end = offset + limit
    page_items = items[slice_start:slice_end]
    next_offset = slice_end if slice_end < total else None

    meta = PlansMeta(
        total= total,
        limit= limit,
        offset= offset,
        next_offset= next_offset,
        count=len(page_items)
    )

    if V2:
        meta_data = meta.model_dump()
    else:
        meta_data = meta.dict()

    return PlansResponse(items= page_items, meta= meta_data) #type: ignore
    

@router.get(
    "/{plan_id}", 
    response_model=PlanOut,
    responses={404: {"model": ErrorResponse}},
    summary="Get plan by ID")

def get_plan(plan_id: str):
    plan = plans_repo.get(plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan