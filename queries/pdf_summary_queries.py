from config.config import pdf_summaries_collection
from utils.pdf_summary_cache import get_pdf_summary_hash

async def get_pdf_summary(gs_url: str):
    """Fetch the cached summary for a PDF by gs_url. Returns None if not found."""
    doc_id = get_pdf_summary_hash(gs_url)
    doc = await pdf_summaries_collection.document(doc_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

async def set_pdf_summary(gs_url: str, title: str, summary: str):
    """Store the summary for a PDF by gs_url."""
    doc_id = get_pdf_summary_hash(gs_url)
    data = {
        "uri": gs_url,
        "title": title,
        "summary": summary
    }
    await pdf_summaries_collection.document(doc_id).set(data)
    return data
