import firebase_admin
from firebase_admin import credentials, firestore

# Application Default credentials are automatically created.
cred = credentials.Certificate('serviceAccount.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


class FireStore:
    @staticmethod
    def get_answers() -> dict:
        doc = db.collection('test').document('data').get()

        return doc.to_dict()
