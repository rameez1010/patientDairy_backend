import hashlib

def get_pdf_summary_hash(gs_url: str) -> str:
    """
    Generate a unique hash for a PDF gs_url (GCS URI) to use as a cache key.
    Args:
        gs_url (str): The gs:// URL of the PDF file
    Returns:
        str: A SHA256 hash string
    """
    return hashlib.sha256(gs_url.encode('utf-8')).hexdigest()
