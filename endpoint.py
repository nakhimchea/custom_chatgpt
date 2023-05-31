import re

from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import os
from firestore_service import *

os.environ["OPENAI_API_KEY"] = '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'


class Endpoint:
    faqs = None

    def __init__(self):
        self.faqs = FireStore.get_answers()

    @staticmethod
    def construct_index(directory_path) -> GPTSimpleVectorIndex:
        max_input_size = 2048
        num_outputs = 512
        max_chunk_overlap = 20
        chunk_size_limit = 600

        prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

        # noinspection PyTypeChecker
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

        documents = SimpleDirectoryReader(directory_path).load_data()

        brain = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

        brain.save_to_disk('knowledge.json')

        return brain

    def chatbot(self, input_text) -> str:
        brain = GPTSimpleVectorIndex.load_from_disk('knowledge.json')
        response = brain.query(input_text, response_mode="compact").response.strip()
        number = re.findall(r'\d+', response[:25])

        try:
            return self.faqs.get(number[0])['en']
        except:
            print('Cannot get number')
            return 'Contact Customer Support for more info.'
