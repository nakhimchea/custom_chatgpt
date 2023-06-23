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
            ir_en = dataframe.loc[i, 'Response EN'] + ' explained in part ' + str(counts) + '.'

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
        data = {
            'qEn': 'How to contact you?',
            'qKm': 'តើយើងអាចទាក់ទងអ្នកដោយរបៀបណា?',
            'rEn': 'the way to contact us explained in part {0}.'.format(counts),
            'aEn': 'Pardon, please contact the Customer Support team via care.centre@wingmoney.com or 023999989 or 012999489.',
            'aKm': 'សូមអធ្យាស្រ័យ! សូមទាក់ទងមកកាន់ក្រុមបម្រើអតិថិជនតាមអ៉ីម៉ែល care.centre@wingmoney.com រឺតាមរយៈលេខទូរសព្ទ 023999989 ឬ 012999489។',
        }
        db.collection('cxBots').document('wingGPT').collection('faqs').document(str(counts)).set(data, merge=True)
        counts += 1

        FileOperator.write_to_text('knowledge/knowledge.txt', content)
        db.collection('cxBots').document('wingGPT').set({'counts': counts}, merge=True)

        print("Done Writing to Firestore")
