from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional, Literal
from app.models.schemas import ErrorResponse, RoomOut, RoomsResponse, RoomsMeta, V2
from app.services.repositories import rooms_repo
from app.services.rules.rules_engine import label_to_category, category_to_load


router = APIRouter(prefix="/plans", tags=["rooms"])

SortBy = Literal["confidence", "raw_label", "category"]
SortOrder = Literal["asc", "desc"]

@router.get(
    "/{plan_id}/rooms",
    response_model=RoomsResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Bad Request"},
        404: {"model": ErrorResponse, "description": "Plan or rooms not found"},
    },
    summary="Get rooms for a given plan with filtering, sorting, and pagination",
    description=(
        "Returns AI-labeled rooms for a given plan."
        "Supports filtering, sorting, and pagination, plus review-status counts in metadata."
    ),
)
def get_rooms(
    plan_id: str,
    min_confidence: float = Query(
        0.0,
        ge=0.0,
        le=1.0,
        description="Minimum confidence filter",
        example={"strict": {"value": 0.95}, "default": {"value": 0.0}},
    ),
    require_review: bool = Query(
        False,
        description="If true, only return rooms needing review",
        example={"review_only": {"value": True}},
    ),
    category: Optional[str] = Query(
        None,
        description="Filter by computed category (case-insensitive)",
        example={"residential": {"value": "residential"}},
    ),
    q: Optional[str] = Query(
        None,
        description="Search raw_label substring (case-insensitive)",
        example={"find_living": {"value": "liv"}},
    ),
    limit: int = Query(
        50,
        ge=1,
        le=100,
        description="Number of rooms to return",
        example={"small_page": {"value": 10}, "large_page": {"value": 100}},
    ),
    offset: int = Query(
        0,
        ge=0,
        description="Offset for pagination",
        example={"first_page": {"value": 0}, "second_page": {"value": 10}},
    ),
    sort_by: SortBy = Query(
        "confidence",
        description='Sort key: "confidence" or "raw_label" or "category"',
        example={"by_confidence": {"value": "confidence"}},
    ),
    sort_order: SortOrder = Query(
        "desc",
        description="Sort order: 'asc' or 'desc'",
        example={"descending": {"value": "desc"}},
    ),
):

    rooms_repo.seed_rooms(plan_id)  # seed stub data if not already
    rooms = rooms_repo.get_rooms(plan_id)

    total = len(rooms)

    # If the plan doesn't exist or has no rooms, handle the 404
    if total == 0:
        # NOTE: You may need a plan_repo.get(plan_id) check here for a proper 404, 
        # but for simplicity, we continue with 200/empty if no rooms found.
        # If you wanted to 404 on plan not found:
        # if not plans_repo.get(plan_id): raise HTTPException(404, detail="Plan not found")
        pass

    # Enrich rooms with rule-driven fields(category, load, needs_review)
    enriched: List[RoomOut] = []
    for r in rooms:
        cat = label_to_category(r.raw_label)
        load = category_to_load(cat) if cat else None
        needs_review = (load is None) or (r.confidence < 0.90)

        enriched.append(
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

    # Apply filters
    filtered = []
    q_lc = q.lower() if q else None
    cat_lc = category.lower() if category else None
    for r in enriched:
        if r.confidence < min_confidence:
            continue
        if require_review and not r.needs_review:
            continue
        if q_lc and q_lc not in r.raw_label.lower():
            continue
        if cat_lc and (r.category or "").lower() != cat_lc:
            continue
        filtered.append(r)

    # Pre-pagination review counts for meta
    pre_page_reviewed = sum(1 for r in filtered if not r.needs_review)
    pre_page_needs_review = len(filtered) - pre_page_reviewed

    # Sorting
    reverse = sort_order == "desc"
    if sort_by == "confidence":
        filtered.sort(
            key=lambda r: (r.confidence, r.raw_label.lower()), reverse=reverse
        )
    elif sort_by == "raw_label":
        filtered.sort(key=lambda r: r.raw_label.lower(), reverse=reverse)
    else:
        filtered.sort(
            key=lambda r: (r.category or "", r.raw_label.lower()), reverse=reverse
        )

    # Pagination
    slice_start = offset
    slice_end = offset + limit
    page_items = filtered[slice_start:slice_end]
    next_offset = slice_end if slice_end < len(filtered) else None

    # If plan exists but no rooms after enrichment/filters, still 200 with empty list
    # If absolutely no rooms at all for this plan, you can choose to 404; we’ll stay 200 for consistency.

    meta = RoomsMeta(
        total=total,
        count=len(page_items),
        limit=limit,
        offset=offset,
        next_offset=next_offset,
        reviewed=pre_page_reviewed,
        needs_review=pre_page_needs_review,
        filters={
            "min_confidence": min_confidence,
            "require_review": require_review,
            "category": category,
            "q": q,
        },
    )

    # Convert the nested Pydantic model to a dict before passing it to the constructor.
    if V2:
        meta_data = meta.model_dump()
    else:
        meta_data = meta.dict()

    # Pass the dictionary to the meta field, ignoring the type checker warning.
    return RoomsResponse(items=page_items, meta=meta_data) # type: ignore
