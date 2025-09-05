from google.cloud import storage
from config.env_config import settings


def upload_blob(source_buffer, destination_blob_name):
    """Uploads a file to the bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(settings.CLOUD_STORAGE_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)

    source_buffer.seek(0)

    blob.upload_from_file(source_buffer, content_type="application/pdf")

    print(f"File uploaded to {destination_blob_name}.")
