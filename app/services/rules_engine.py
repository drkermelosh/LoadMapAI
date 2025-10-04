import yaml, os

RULES_PATH = os.getenv("RULES_PATH", "app/rules/asce7-22.yml")

def load_rules():
    with open(RULES_PATH, "r") as f:
        return yaml.safe_load(f)

def map_label_to_load(label: str):
    rules = load_rules()
    ab = rules.get("abbrev", {})
    mp = rules.get("mappings", {})
    key = ab.get(label.upper())
    if key and key in mp:
        return mp[key]
    return {"uniform_psf": None, "code_ref": "Unknown"}
