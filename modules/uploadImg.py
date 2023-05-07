from google.cloud import storage

client = storage.Client.from_service_account_json(
    'deploy-flask-testing-89a87c693e13.json')
bucket = client.get_bucket('user-images-bucket-flask')
