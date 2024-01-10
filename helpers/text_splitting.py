from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

loader = TextLoader("aipg.txt")
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len)
chunks = text_splitter.split_text(documents[0].page_content)


for i, _ in enumerate(chunks):
    print(f"chunk #{i}, size: {chunks[i]}")
    print("--------------------------------------------------")


text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len)
chunks = text_splitter.split_documents(documents)
for i, _ in enumerate(chunks):
    print(f"chunk #{i}, size: {chunks[i]}")
