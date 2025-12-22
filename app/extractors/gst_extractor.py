import re
from app.utils import clean_number, confidence_score

def extract_gst_sales(chunks):
    for text, sim in chunks:
        match = re.search(
            r"\(a\)\s*Outward taxable supplies[\s\S]{0,100}?([\d,]+\.\d+)",
            text,
            re.IGNORECASE
        )
        if match:
            return [{
                "month": "December 2024",
                "sales": int(float(match.group(1))),
                "source": "GSTR-3B Table 3.1(a)",
                "confidence": confidence_score(sim)
            }]
    return []

