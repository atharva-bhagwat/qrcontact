import os
from google.cloud import storage
from google.oauth2 import service_account

def get_credentials():
    keys = ['type', 'project_id', 'private_key_id', 'private_key', 'client_email',
            'client_id', 'auth_uri', 'token_uri', 'auth_provider_x509_cert_url',
            'client_x509_cert_url']
    credentials = {}
    for key in keys:
        credentials[key] = os.environ.get(f"QRCONTACT_{key}")
    return credentials