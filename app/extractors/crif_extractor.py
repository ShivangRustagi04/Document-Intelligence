import re
from app.utils import clean_number, confidence_score

def extract_crif_parameters(bureau_score_chunks, overdue_chunks):
    result = {}

    # ---- Bureau Score ----
    result["bureau_score"] = extract_pattern(
    bureau_score_chunks,
    r"CRIF HM Score\(S\)[\s\S]{0,200}?300-900\s+(\d{3})"
)




    # ---- Total Overdue ----
    result["total_overdue_amount"] = extract_pattern(
    overdue_chunks,
    r"Total\s+Amount\s+Overdue\s*(?:INR|Rs\.?|₹)?\s*[:\-|]?\s*([\d,]+)"
)







    return result


def extract_pattern(chunks, pattern):
    for text, sim in chunks:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # ✅ Always take the LAST captured group
            value = match.group(match.lastindex)

            return {
                "value": clean_number(value),
                "source": "CRIF Account Summary",
                "confidence": confidence_score(sim)
            }

    return {
        "value": None,
        "status": "not_found",
        "confidence": 0.0
    }

