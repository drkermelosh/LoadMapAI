import yaml, os
from functools import lru_cache

RULES_PATH = os.getenv("RULES_PATH", "app/rules/asce7-22.yml")

@lru_cache(maxsize=1)
def _load_rules_cached():
    with open(RULES_PATH, "r") as f:
        return yaml.safe_load(f)
    
def load_rules():
    return _load_rules_cached()

def label_to_category(label: str) -> str | None:
    if not label:
        return None
    rules = _load_rules_cached()
    ab = rules.get("abbrev", {})
    return ab.get(label.strip().upper())

def category_to_load(category: str) -> dict | None:
    if not category:
        return None
    rules = _load_rules_cached()
    mp = rules.get("mappings", {})
    return mp.get(category)

def map_label_to_load(label: str) -> dict | None:
    cat = label_to_category(label)
    if not cat:
        return None
    return category_to_load(cat)

