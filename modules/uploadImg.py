from google.cloud import storage

client = storage.Client.from_service_account_json(
    'credentials.json')
bucket = client.get_bucket('user-images-bucket-flask')
