from fastapi import FastAPI
from endpoint import Endpoint

app = FastAPI()


@app.get('/response')
def get_response(input_text: str) -> str:
    return Endpoint.chatbot(input_text)


@app.get('/')
def ping() -> str:
    return "Ping Successful..."


def main():
    Endpoint.construct_index("knowledge")


if __name__ == '__main__':
    main()
