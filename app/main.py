from fastapi import FastAPI, UploadFile
from app.loaders.pdf_loader import parse_pdf
from app.embeddings.embedder import Embedder
from app.embeddings.vector_store import VectorStore
from app.extractors.crif_extractor import extract_crif_parameters
from app.extractors.gst_extractor import extract_gst_sales

app = FastAPI()

@app.post("/extract")
async def extract(
    crif_pdf: UploadFile,
    gst_pdf: UploadFile
):
    # ---- Load PDFs ----
    crif_pages = parse_pdf(crif_pdf.file)
    gst_pages = parse_pdf(gst_pdf.file)

    document_texts = [p["text"] for p in crif_pages + gst_pages]

    # ---- Build embeddings ----
    embedder = Embedder()
    doc_embeddings = embedder.fit_transform(document_texts)

    store = VectorStore(doc_embeddings.shape[1])
    store.add(doc_embeddings, document_texts)

    # ---- CRIF semantic queries ----
    bureau_score_query = "bureau score credit score CRIF report"
    overdue_query = (
    "Total Amount Overdue Account Summary table CRIF "
    "All amounts are in INR Overdue Accounts"
)


    bureau_score_emb = embedder.transform([bureau_score_query])[0]
    overdue_emb = embedder.transform([overdue_query])[0]

    bureau_score_chunks = store.search(bureau_score_emb, k=3)
    # pass ALL crif text for overdue extraction
    overdue_chunks = [(p["text"], 1.0) for p in crif_pages]


    # ---- Extract CRIF parameters ----
    bureau_parameters = extract_crif_parameters(
        bureau_score_chunks=bureau_score_chunks,
        overdue_chunks=overdue_chunks
    )

    # ---- GST semantic query ----
    gst_query = "GSTR-3B Table 3.1(a) outward taxable supplies"
    gst_emb = embedder.transform([gst_query])[0]
    gst_chunks = store.search(gst_emb, k=3)

    gst_sales = extract_gst_sales(gst_chunks)

    overall_conf = round(
        sum(v["confidence"] for v in bureau_parameters.values()) /
        len(bureau_parameters),
        2
    )

    return {
        "bureau_parameters": bureau_parameters,
        "gst_sales": gst_sales,
        "overall_confidence_score": overall_conf
    }
