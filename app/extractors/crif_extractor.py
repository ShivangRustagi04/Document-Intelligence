import re
from app.utils import clean_number, confidence_score


def extract_pattern(chunks, pattern):
    """
    Generic regex extractor for semantic fields (e.g., Bureau Score).
    """
    for text, sim in chunks:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            value = match.group(1)
            return {
                "value": clean_number(value),
                "source": "CRIF Document",
                "confidence": confidence_score(sim)
            }

    return {
        "value": None,
        "status": "not_found",
        "confidence": 0.0
    }


def extract_crif_parameters(bureau_score_chunks, overdue_chunks):
    """
    Entry point called from main.py
    """
    return {
        "bureau_score": extract_bureau_score(bureau_score_chunks),
        "total_overdue_amount": extract_total_overdue_amount(overdue_chunks)
    }


def extract_bureau_score(chunks):
    for text, sim in chunks:
        match = re.search(
            r"CRIF HM Score\(S\)[\s\S]{0,200}?300-900\s+(\d{3})",
            text,
            re.IGNORECASE
        )
        if match:
            return {
                "value": int(match.group(1)),
                "source": "CRIF HM Score(S) Section",
                "confidence": confidence_score(sim)
            }

    return {
        "value": None,
        "status": "not_found",
        "confidence": 0.0
    }


def extract_total_overdue_amount(chunks):
    for text, sim in chunks:
        parts = re.split(
            r"Group\s+Account\s+Summary",
            text,
            flags=re.IGNORECASE
        )

        if len(parts) < 2:
            continue

        before_group_summary = parts[0]

        numbers = re.findall(r"\b[\d,]+\b", before_group_summary)

        if not numbers:
            continue

        overdue_raw = numbers[-1]
        overdue_value = clean_number(overdue_raw)

        if overdue_value > 1000:
            return {
                "value": overdue_value,
                "source": "Account Summary → Total Amount Overdue",
                "confidence": 1.0
            }

    return {
        "value": None,
        "status": "not_found",
        "confidence": 0.0
    }
