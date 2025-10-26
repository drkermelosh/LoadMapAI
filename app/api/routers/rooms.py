from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.models.schemas import RoomOut, RoomsResponse, RoomsMeta, SortBy, SortOrder
from app.services.repositories import rooms_repo
from app.services.rules.rules_engine import label_to_category, category_to_load


router = APIRouter(prefix="/plans", tags=["rooms"])

@router.get("/{plan_id}/rooms", response_model=RoomsResponse)
def get_rooms(
    plan_id: str,
    min_confidence: float = Query(0.0, ge=0.0, le=1.0, description="Minimum confidence filter"),
    require_review: bool = Query(False, description="If true, only return rooms needing review"),
    category: Optional[str] = Query(None, description="Filter by computed category (case-insensitive)"),
    q: Optional[str] = Query(None, description="Search raw_label substring (case-insensitive)"),
    limit: int = Query(50, ge=1, le=100, description="Number of rooms to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    sort_by: SortBy = Query(SortBy.confidence, description="Field to sort by"),
    sort_order: SortOrder = Query(SortOrder.desc, description="Sort order")
):
    rooms_repo.seed_rooms(plan_id) # seed stub data if not already
    rooms = rooms_repo.get_rooms(plan_id)

    total = len(rooms)
    

    if not rooms:
        raise HTTPException(status_code=404, detail="No rooms found for this plan")
    
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
    reverse = (sort_order == SortOrder.desc)
    if sort_by == SortBy.confidence:
        filtered.sort(key=lambda r: (r.confidence, r.raw_label.lower()), reverse=reverse)
    elif sort_by == SortBy.raw_label:
        filtered.sort(key=lambda r: r.raw_label.lower(), reverse=reverse)
    else: 
        filtered.sort(key=lambda r: (r.category or "", r.raw_label.lower()), reverse=reverse)

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
        sort_by=sort_by,
        sort_order=sort_order,
        filters={
            "min_confidence": min_confidence,
            "require_review": require_review,
            "category": category,
            "q": q,
        }  
    )

    return RoomsResponse(items=page_items, meta=meta)