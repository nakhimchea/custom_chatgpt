import firebase_admin
from firebase_admin import credentials, firestore
from file_operator import *
import time

# Application Default credentials are automatically created.
cred = credentials.Certificate('serviceAccount.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()


class FireStore:
    @staticmethod
    def get_answers() -> list:
        counts = db.collection('cxBots').document('wingGPT').get().to_dict()['counts']

        faqs = []
        for i in range(counts):
            doc = db.collection('cxBots').document('wingGPT').collection('faqs').document(str(i)).get()
            faqs.append(doc.to_dict())

        return faqs

    @staticmethod
    def failed_faq(input_text: str):
        print("Pushing not trained question...")
        db.collection('cxBots').document('wingGPT').collection('new').document(str(time.time_ns()//1000000)).set({'qEn': input_text}, merge=False)
        print("Done Pushing not trained question.")

    @staticmethod
    def write_faqs(dataframe: DataFrame):
        print("Writing to Firestore")
        counts = db.collection('cxBots').document('wingGPT').get().to_dict()['counts']

        content = []
        for i in range(len(dataframe)):
            iq_en = dataframe.loc[i, 'Question EN']
            iq_km = dataframe.loc[i, 'Question KM']
            ir_en = dataframe.loc[i, 'Response EN'] + ' explained in part ' + str(counts+1) + '.'

            content.append(ir_en)

            data = {
                'qEn': iq_en,
                'qKm': iq_km,
                'rEn': ir_en,
                'aEn': dataframe.loc[i, 'Answer EN'],
                'aKm': dataframe.loc[i, 'Answer KM']
            }
            db.collection('cxBots').document('wingGPT').collection('faqs').document(str(counts)).set(data, merge=True)
            counts += 1

        FileOperator.write_to_text('knowledge/knowledge.txt', content)
        db.collection('cxBots').document('wingGPT').set({'counts': counts}, merge=True)

        print("Done Writing to Firestore")
