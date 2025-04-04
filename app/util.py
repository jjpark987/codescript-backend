from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from google.cloud import storage
from os import getenv, environ

load_dotenv()

GCP_CREDENTIALS = getenv('GCP_CREDENTIALS')
GC_BUCKET_NAME = getenv('GC_BUCKET_NAME')
CREDENTIALS_PATH = '/tmp/gcp_credentials.json'

def get_signed_image_url(image_path: str, expiration_seconds: int = 3600) -> str:
    with open(CREDENTIALS_PATH, 'w') as cred_file:
        cred_file.write(GCP_CREDENTIALS)

    environ['GOOGLE_APPLICATION_CREDENTIALS'] = CREDENTIALS_PATH

    storage_client = storage.Client()
    bucket = storage_client.bucket(GC_BUCKET_NAME)
    blob = bucket.blob(image_path)

    expiration_time = datetime.now(tz=timezone.utc) + timedelta(seconds=expiration_seconds)

    url = blob.generate_signed_url(expiration=expiration_time)

    return url
