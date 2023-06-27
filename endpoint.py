import re

from llama_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
from firestore_service import *

os.environ["OPENAI_API_KEY"] = ''


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

    def chatbot(self, input_text) -> str:
        brain = GPTSimpleVectorIndex.load_from_disk('knowledge.json')
        response = brain.query(input_text, response_mode="compact").response.strip()
        response1 = brain.query('Account: ' + input_text, response_mode="compact").response.strip()
        if 'account' not in input_text:
            response1.replace(' account', '')

        print('Res1: ', response)
        print('Res2: ', response1)

        number = re.findall(r'\d+', response)
        number1 = re.findall(r'\d+', response1)

        answers = []

        try:
            string = ''
            for i in range(len(number)):
                string += '{0} '.format(int(number[i]))
            if string != '':
                answers.append(string)

        except:
            print('Cannot extract number from Number')

        try:
            string = ''
            for i in range(len(number1)):
                string += '{0} '.format(int(number1[i]))
            if string != '':
                answers.append(string)
        except:
            print('Cannot extract number from Number1')

        if len(answers) == 0:
            FireStore.failed_faq(input_text)

        return answers[-1] if len(answers) != 0 else '68'
