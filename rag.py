import os

import discord
from discord.app_commands import commands
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores.chroma import Chroma

from bot import system_message_prompt

host = "23.244.73.132"
api_base = 'https://settled-pin-attraction-unto.trycloudflare.com/v1'
os.environ["DISCORD_TOKEN"] = "MTE5MjQ1ODQzNDUzNzMzMjc0Ng.G8sfdd.BH5Rh09LxxHevmop3B97kxVHzk2O8-HXoJ7HBY"

#Load the text
loader = TextLoader("./aipg_alltext.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

#Create vector store
embeddings = HuggingFaceBgeEmbeddings(model_name="BAAI/bge-small-en-v1.5")
retriever = Chroma.from_documents(texts, embeddings).as_retriever()

#Connect to open source llm
llm = ChatOpenAI( openai_api_base=api_base,
                  openai_api_key=api_base,max_tokens=1024)

qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                  chain_type="stuff",
                                  retriever=retriever,
                                  return_source_documents=True)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def question(ctx, *, question):
    try:
        llm_response = qa_chain(question)
        await ctx.send(llm_response)
    except Exception as e:
        print(f"Error occurred: {e}")
        await ctx.send("Sorry, I was unable to process your question.")


bot.run(os.environ.get("DISCORD_TOKEN"))