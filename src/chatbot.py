from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts.prompt import PromptTemplate
from langchain.callbacks import get_openai_callback
from config import *
from langchain.chains import RetrievalQA
#fix Error: module 'langchain' has no attribute 'verbose'
import langchain
from langchain.llms import OpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
langchain.verbose = False

class Chatbot:

    def __init__(self, vectors):
        self.vectors = vectors

    def conversational_chat(self, query):
        retriever = self.vectors.as_retriever()

        # Create a question-answering chain using the index
        # chain = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", 
        #                                     retriever=retriever, 
        #                                     input_key="question")
        chain = ConversationalRetrievalChain.from_llm(
            llm = ChatOpenAI(temperature=0.0,model_name='gpt-3.5-turbo'),
            retriever=retriever)
        return chain
        # chain_input = {"question": query}
        # result = chain(chain_input)
        # print(result["result"])
        # return result["result"]

