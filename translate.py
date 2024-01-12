import discord
from discord.ext import commands
from transformers import T5ForConditionalGeneration, T5Tokenizer


class T5Translator:
    def __init__(self):
        model_name = 'jbochi/madlad400-3b-mt'

        self.model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")

        self.model.save_pretrained("./models/madlad", from_pt=True)
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)

        #Discord bot setup
        self.active_sessions = {}
        intents = discord.Intents.default()
        intents.message_content = True
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.setup_bot_commands()

    def translate_to_english(self, text):
        # Prefixing the input text with language identifier
        text_to_translate = f"<2en> {text}"

        input_ids = self.tokenizer(text_to_translate, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(input_ids=input_ids)

        # Decoding the output
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translation

    def translate_from_english(self, text, target_language):
        # Prefixing the input text with language identifier
        text_to_translate = f"<2{target_language}> {text}"

        input_ids = self.tokenizer(text_to_translate, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(input_ids=input_ids)

        # Decoding the output
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translation

    def setup_bot_commands(self):
        @self.bot.command()
        async def translate(ctx, *, text):
            try:
                translated_text = self.translate_to_english(text)
                await ctx.send(translated_text)
            except Exception as e:
                print(f"Error occurred: {e}")
                await ctx.send("Sorry, I was unable to process your request.")

        @self.bot.command()
        async def translateReply(ctx, *, text=None):
            try:
                # Check if the message is a reply to another message
                if ctx.message.reference and ctx.message.reference.resolved:
                    target_message = ctx.message.reference.resolved
                    if isinstance(target_message, discord.Message):
                        text_to_translate = target_message.content
                    else:
                        await ctx.send("I can't translate that message.")
                        return
                else:
                    # If it's not a reply, use the provided text
                    if text is None:
                        await ctx.send("Please provide a message or reply to a message to translate.")
                        return
                    text_to_translate = text

                # Translate the text
                translated_text = self.translate_to_english(text_to_translate)
                await ctx.send(translated_text)

            except Exception as e:
                print(f"Error occurred: {e}")
                await ctx.send("Sorry, I was unable to process your request.")

        @self.bot.command()
        async def start_session(ctx, target_language: str):
            # Start a translation session in the current channel with the specified target language
            self.active_sessions[ctx.channel.id] = target_language
            await ctx.send(f"Translation session started. Messages will be translated to {target_language}.")

        @self.bot.command()
        async def end_session(ctx):
            # End the translation session in the current channel
            if ctx.channel.id in self.active_sessions:
                del self.active_sessions[ctx.channel.id]
                await ctx.send("Translation session ended.")
            else:
                await ctx.send("No active translation session in this channel.")

    async def on_message(self, message):
        # Override the on_message event to translate messages in active sessions
        if message.channel.id in self.active_sessions and not message.author.bot:
            target_language = self.active_sessions[message.channel.id]
            translated_text = self.translate_to_english(message.content)

            # Reply to the original message with the translation
            await message.reply(translated_text)

        # Don't forget to process commands
        await self.bot.process_commands(message)



    def run(self, token):
        self.bot.run(token)


if __name__ == "__main__":
    token = "MTE5MjQ1ODQzNDUzNzMzMjc0Ng.GS5OZQ.DwxKPHdjLOQ89UIOtDuSec8hYNXeMq69H_QZls"
    bot = T5Translator()
    bot.run(token)