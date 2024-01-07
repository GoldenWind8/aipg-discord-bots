import discord
from discord.ext import commands
from transformers import T5ForConditionalGeneration, T5Tokenizer


class T5Translator:
    def __init__(self, model_path):
        model_name = 'jbochi/madlad400-3b-mt'
        if model_path:
            self.model = T5ForConditionalGeneration.from_pretrained(model_path, device_map="auto")
            self.tokenizer = T5Tokenizer.from_pretrained(model_path)

        self.model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)

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


#Discord Bot setup
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Usage example
# model_path = '/path/to/save/model'
# translator = T5Translator(model_path)
# translated_text = translator.translate_to_english("Hola mundo")
# print(translated_text)

@bot.command()
async def translate(ctx, *, question):
    try:
        translated_text = 1
        await ctx.send(translated_text)
    except Exception as e:
        print(f"Error occurred: {e}")
        await ctx.send("Sorry, I was unable to process your request.")


bot.run("MTE5MjQ1WjfDmH7n7YJ_kb6nmLy0")
