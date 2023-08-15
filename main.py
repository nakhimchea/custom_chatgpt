from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from endpoint import Endpoint
from firestore_service import *
from file_operator import *
from pydantic import BaseModel

app = FastAPI()
endpoint = Endpoint()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Request(BaseModel):
    input_text: str


@app.post('/rgx_response')
def get_response(input_text: Request) -> str:
    return endpoint.chatbot(input_text.input_text.strip())


@app.post('/wingchat')
def get_response(input_text: Request) -> str:
    return endpoint.chatbot(input_text.input_text.strip())


@app.get('/')
def ping() -> str:
    return "Ping Successful..."


def main():
    print("Reading from file...")
    dataframe = FileOperator.read_from_excel('pure/wingbank_faqs.xlsx')
    print("Done Reading from file.")

    print("Write FAQs to Firestore...")
    FireStore.write_faqs(dataframe)
    print("Done writing FAQs to Firestore.")

    print("Creating knowledge base override OpenAI...")
    endpoint.construct_index("knowledge")
    print("Done Creating knowledge base.")


if __name__ == '__main__':
    main()
