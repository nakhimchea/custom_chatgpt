from fastapi import FastAPI
from endpoint import Endpoint

app = FastAPI()
endpoint = Endpoint()


@app.get('/response')
def get_response(input_text: str) -> str:
    return endpoint.chatbot("Intention code of \"" + input_text.strip().replace('?', '') + "?\"?")


@app.get('/')
def ping() -> str:
    return "Ping Successful..."


def main():
    endpoint.construct_index("knowledge")


if __name__ == '__main__':
    main()
