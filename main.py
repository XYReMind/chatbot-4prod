from langchain.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
import pickle
import faiss
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI


urls = []
with open('links_file_0.txt') as f:
    for line in f.readlines():
        urls.append(line.strip('\n'))
print(urls[:1])
loaders = UnstructuredURLLoader(urls=urls[:1])
data = loaders.load()
print(data)
text_splitter = CharacterTextSplitter(separator='\n',
                                      chunk_size = 1000,
                                      chunk_overlap = 200)

docs = text_splitter.split_documents(data)
embeddings = OpenAIEmbeddings()

vectorStore_openAI = FAISS.from_documents(docs, embeddings)

with open("faiss_store_openai.pkl", 'wb') as f:
    pickle.dump(vectorStore_openAI, f)

with open("faiss_store_openai.pkl", 'rb') as f:
    VectorStore = pickle.load(f)

llm = OpenAI(temperature=0)

chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever = VectorStore.as_retriever())
chain({"queestion":"How much is Sojag Mykonos?"}, return_only_outputs=True)