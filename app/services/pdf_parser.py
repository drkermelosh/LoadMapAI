import pdfplumber
import re
from typing import List, Dict

# basic label patterns & whitelist (expand as you go)

ROOM_LABEL_REGEX = re.compile(r"^[A-Z][A-Z0-9/\-\s]{1,30}$")  # uppercase-ish words
COMMON_ROOM_TOKENS = {
    "BED", "BEDROOM", "MBR", "LIVING", "DINING", "KITCHEN", "BATH", "BATHROOM",
    "CLOSET", "CL", "OFFICE", "OFC", "MECH", "MECHANICAL", "ELEC", "ELECTRICAL",
    "STORAGE", "STOR", "HALL", "CORRIDOR", "STAIR", "STAIRWAY", "LAUNDRY"
}

def _looks_like_room_label(text: str) -> bool:
    t = text.strip()
    if not t or len(t) < 2 or len(t) > 32:
        return False
    if not ROOM_LABEL_REGEX.match(t):
        return False
    
    # accept if any token matches our known set

    tokens = {tok for tok in re.split(r"[\s\-\/]+", t) if tok}
    return bool(tokens & COMMON_ROOM_TOKENS)
