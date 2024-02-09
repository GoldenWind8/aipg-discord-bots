from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.chroma import Chroma



class RetrievalAugmentedGeneration:
    def __init__(self, api_base, text_file_path):
        self.api_base = api_base
        self.text_file_path = text_file_path
        self.vector_store = self.create_vector_store()
        self.qa_chain = self.setup_qa_chain()

    def create_vector_store(self):
        texts = self.load_texts(self.text_file_path)
        embeddings = OpenAIEmbeddings() #TODO REPLACE HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        return Chroma.from_documents(texts, embeddings).as_retriever()

    def add_documents(self, texts):
        # Split the input texts into smaller chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len)
        split_texts = text_splitter.split_documents(texts)

        # Add these chunks to the vector store
        self.vector_store.add_documents(split_texts)

    def setup_qa_chain(self):
        llm = ChatOpenAI(openai_api_base=self.api_base, openai_api_key=self.api_base, max_tokens=1024)
        return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=self.vector_store, return_source_documents=False)


    def load_texts(self, text_file_path):
        loader = TextLoader(text_file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len)
        return text_splitter.split_documents(documents)




