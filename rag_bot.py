import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from rag import RetrievalAugmentedGeneration

api_base = 'https://australian-assigned-scanners-crowd.trycloudflare.com/v1'
text_file_path = "./aipg.txt"
load_dotenv()
token = os.environ.get("DISCORD_TOKEN")

# Initialize the translator
rag = RetrievalAugmentedGeneration(api_base, text_file_path)

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot command: Translate text to English
@bot.command()
async def question(ctx, *, question):
    try:
        llm_response = rag.qa_chain(question)
        await ctx.send(llm_response['result'])
    except Exception as e:
        await ctx.send("Sorry, I was unable to process your question.")
@bot.command()
async def add_to_db(ctx, *, text):
    try:
        rag.add_documents(text)
        print("Added to db")
    except Exception as e:
        await ctx.send("Sorry, I was unable to process your request.")






# Run the bot
if __name__ == "__main__":
    bot.run(token)
