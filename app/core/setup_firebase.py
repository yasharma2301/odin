import firebase_admin
from firebase_admin import credentials


def initialize_firebase(service_account):
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account)
        firebase_admin.initialize_app(cred)
