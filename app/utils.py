import re

def clean_number(value):
    if value is None:
        return None
    return int(re.sub(r"[^\d]", "", str(value)))

def confidence_score(similarity, found=True):
    if not found:
        return 0.0
    return round(min(1.0, 0.6 + similarity * 0.4), 2)
