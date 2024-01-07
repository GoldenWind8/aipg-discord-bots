import os

import discord
from discord.ext import commands
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
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
        text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=100)
        return text_splitter.split_documents(documents)

    def create_vector_store(self, texts):
        embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")
        return Chroma.from_documents(texts, embeddings).as_retriever()

    def setup_qa_chain(self):
        texts = self.load_texts()
        retriever = self.create_vector_store(texts)
        llm = ChatOpenAI(openai_api_base=self.api_base, openai_api_key=self.api_base, max_tokens=1024)
        return RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True)

    def setup_bot_commands(self):
        @self.bot.command()
        async def question(ctx, *, question):
            try:
                llm_response = self.qa_chain(question)
                await ctx.send(llm_response)
            except Exception as e:
                print(f"Error occurred: {e}")
                await ctx.send("Sorry, I was unable to process your question.")

    def run(self):
        self.bot.run(self.token)

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    api_base = 'https://settled-pin-attraction-unto.trycloudflare.com/v1'
    text_file_path = "./aipg_alltext.txt"

    bot = DiscordQABot(token, api_base, text_file_path)
    bot.run()
