from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
import os

os.environ["OPENAI_API_KEY"] = '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'


class Endpoint:
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

    @staticmethod
    def chatbot(input_text) -> str:
        brain = GPTSimpleVectorIndex.load_from_disk('knowledge.json')

        return brain.query(input_text, response_mode="compact").response.strip()
