from transformers import T5ForConditionalGeneration, T5Tokenizer

class T5Translator:
    def __init__(self):
        model_name = 'jbochi/madlad400-3b-mt'
        self.model = T5ForConditionalGeneration.from_pretrained(model_name, device_map="auto")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)

    def translate_to_english(self, text):
        text_to_translate = f"<2en> {text}"
        input_ids = self.tokenizer(text_to_translate, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(input_ids=input_ids)
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translation

    def translate_from_english(self, text, target_language):
        text_to_translate = f"<2{target_language}> {text}"
        input_ids = self.tokenizer(text_to_translate, return_tensors="pt").input_ids.to(self.model.device)
        outputs = self.model.generate(input_ids=input_ids)
        translation = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return translation
