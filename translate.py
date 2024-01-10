import discord
from discord.ext import commands
from transformers import T5ForConditionalGeneration, T5Tokenizer


class T5Translator:
    def __init__(self):
        model_name = 'jbochi/madlad400-3b-mt'

        self.model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)

        #Discord bot setup
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

    def run(self, token):
        self.bot.run(token)


if __name__ == "__main__":
    token = "MTE5MjQ1ODQzNDUzNzMzMjc0Ng.GYa80l.HuTTIP2mY0xS4Hiy_owK58r0056yEdVjGG5xDA"

    bot = T5Translator()
    bot.run(token)