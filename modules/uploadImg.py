from google.cloud import storage

client = storage.Client.from_service_account_json(
    'deploy-flask-testing-6223247fd3e8.json')
bucket = client.get_bucket('user-images-bucket-flask')
