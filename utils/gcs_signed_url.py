from google.cloud import storage
from datetime import timedelta
import re


def parse_gs_uri(gs_uri: str):
    """
    Parse a Google Cloud Storage URI (gs://bucket/object) into bucket and blob name.
    """
    match = re.match(r"gs://([^/]+)/(.+)", gs_uri)
    if not match:
        raise ValueError(f"Invalid GCS URI: {gs_uri}")
    return match.group(1), match.group(2)


def generate_signed_url(gs_uri: str, expiration_minutes: int = 60) -> str:
    """
    Generate a signed URL for a GCS object given its gs:// URI.
    """
    bucket_name, blob_name = parse_gs_uri(gs_uri)
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    url = blob.generate_signed_url(
        version="v4",
        expiration=timedelta(minutes=expiration_minutes),
        method="GET",
    )
    return url
