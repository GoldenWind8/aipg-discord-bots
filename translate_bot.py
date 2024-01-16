import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from translation_model import T5Translator
from helpers.classify_lang import is_text_english

# Initialize the translator
translator = T5Translator()

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Active translation sessions
active_sessions = {}
language_codes = {
    1184390709231489105: "zh",  # Chinese
    1184552179600728124: "ru",  # Russian
    1184553739290427423: "fr",  # French
    1184553809146552482: "tr",   # Turkish
    1194896649521205268: "fr", # Test
    1196899790752055406: "zh",
}

# Bot command: Translate text to English
@bot.command()
async def translate_text(ctx, *, text):
    try:
        translated_text = translator.translate_to_english(text)
        await ctx.send(translated_text)
    except Exception as e:
        await ctx.send("Sorry, I was unable to process your request.")

# Bot command: Translate the replied-to message or provided text
@bot.command()
async def translate(ctx, *, text=None):
    try:
        if ctx.message.reference and ctx.message.reference.resolved:
            target_message = ctx.message.reference.resolved
            if isinstance(target_message, discord.Message):
                text_to_translate = target_message.content
            else:
                await ctx.send("I can't translate that message.")
                return
        else:
            if text is None:
                await ctx.send("Please provide a message or reply to a message to translate.")
                return
            text_to_translate = text

        translated_text = translator.translate_to_english(text_to_translate)
        await ctx.send(translated_text)

    except Exception as e:
        await ctx.send("Sorry, I was unable to process your request.")

# Bot command: Start a translation session in a channel
@bot.command()
async def start(ctx):
    active_sessions[ctx.channel.id] = True
    target_language = language_codes[ctx.channel.id]
    await ctx.send(f"Translation session started. Messages will be translated to {target_language}.")

# Bot command: End the translation session in a channel
@bot.command()
async def end(ctx):
    if ctx.channel.id in active_sessions:
        del active_sessions[ctx.channel.id]
        await ctx.send("Translation session ended.")
    else:
        await ctx.send("No active translation session in this channel.")

# Event handler for processing messages
@bot.event
async def on_message(message):
    if message.author.bot or not message.content:
        return

    if message.channel.id in active_sessions and message.content[0] != "!":
        target_language = language_codes[message.channel.id]
        translated_text = ""
        if(is_text_english((message.content))):
            translated_text = translator.translate_from_english(message.content, target_language)
        else:
            translated_text = translator.translate_to_english(message.content)

        if len(translated_text) != 0:
            await message.reply(translated_text)
        else:
            await message.reply("Unable to translate")

    await bot.process_commands(message)


# Run the bot
if __name__ == "__main__":
    load_dotenv()
    token = os.environ.get("DISCORD_TOKEN")
    bot.run(token)
