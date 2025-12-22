# Document Intelligence – CRIF & GSTR-3B Extraction

This project extracts structured financial data from:
- CRIF Bureau Reports (PDF)
- GSTR-3B Returns (PDF)

Using:
- PDF parsing (PyMuPDF + PyPDF)
- Semantic search (embeddings)
- Rule-based extraction
- Confidence scoring

---

## 1. How to Run Locally

### Prerequisites
- Python 3.9+
- pip

### Install dependencies
```bash
pip install -r requirements.txt
```

### Start the API
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The API UI will be available at:
```
http://127.0.0.1:8000/docs
```

## 2. API Usage

### Endpoint
POST /extract

### Example curl request
```bash
curl -X POST "http://127.0.0.1:8000/extract" \
    -F "crif_pdf=@sample_crif.pdf" \
    -F "gst_pdf=@sample_gstr3b.pdf"
```

## 3. Sample Output
```json
{
    "bureau_parameters": {
        "bureau_score": {
            "value": 677,
            "source": "CRIF HM Score(S) Section",
            "confidence": 0.96
        },
        "total_overdue_amount": {
            "value": 8468,
            "source": "Account Summary Table",
            "confidence": 0.97
        }
    },
    "gst_sales": [
        {
            "month": "December 2024",
            "sales": 917677,
            "source": "GSTR-3B Table 3.1(a)",
            "confidence": 0.97
        }
    ],
    "overall_confidence_score": 0.97
}
```


## 4. Hard-coded Test Examples 

`tests/test_examples.py`

Run it with:
```bash
python tests/test_examples.py
```
