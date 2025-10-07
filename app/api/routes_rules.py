from fastapi import APIRouter, Query
from app.services.rules_engine import map_label_to_load

router = APIRouter()

@router.get("/map")
def map_rule(label: str = Query(..., description="Raw room label, e.g., 'BED', 'LIVING, 'OFFICE'")):
    result = map_label_to_load(label)
    return {
        "input label": label,
        "mapping": result
    }