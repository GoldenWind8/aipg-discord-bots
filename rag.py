import os

import discord
from discord.ext import commands
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma
class DiscordQABot:
    def __init__(self, token, api_base, text_file_path):
        self.token = token
        self.api_base = api_base
        self.text_file_path = text_file_path

        self.bot = commands.Bot(command_prefix='!', intents=self.get_intents())
        self.qa_chain = self.setup_qa_chain()
        self.setup_bot_commands()

    def get_intents(self):
        intents = discord.Intents.default()
        intents.message_content = True
        return intents

    def load_texts(self):
        loader = TextLoader(self.text_file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function=len)
        return text_splitter.split_documents(documents)

    def create_vector_store(self, texts):
        embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        return Chroma.from_documents(texts, embeddings).as_retriever()

    def setup_qa_chain(self):
        texts = self.load_texts()
        retriever = self.create_vector_store(texts)
        llm = ChatOpenAI(openai_api_base=self.api_base, openai_api_key=self.api_base, max_tokens=1024)
        return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=False)

    def setup_bot_commands(self):
        @self.bot.command()
        async def question(ctx, *, question):
            try:
                llm_response = self.qa_chain(question)
                await ctx.send(llm_response['result'])
            except Exception as e:
                print(f"Error occurred: {e}")
                await ctx.send("Sorry, I was unable to process your question.")

    def run(self):
        self.bot.run(self.token)

if __name__ == "__main__":
    os.environ["DISCORD_TOKEN"] = "MTE5MjQ1ODQzNDUzNzMzMjc0Ng.GYa80l.HuTTIP2mY0xS4Hiy_owK58r0056yEdVjGG5xDA"
    token = os.environ.get("DISCORD_TOKEN")
    api_base = 'https://additionally-functional-first-hotel.trycloudflare.com/v1'
    text_file_path = "./aipg.txt"

    bot = DiscordQABot(token, api_base, text_file_path)
    bot.run()
