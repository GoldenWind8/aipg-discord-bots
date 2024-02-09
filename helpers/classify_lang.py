import fasttext


def is_text_english(text):
    # Load the pre-trained language identification model
    model = fasttext.load_model('./models/lid.176.bin')

    # Predict the language of the text
    predictions = model.predict(text, k=1)  # k=1 means get the top 1 prediction
    language = predictions[0][0].split("__label__")[1]

    # Check if the predicted language is English
    print("language is ", language)
    is_english = (language == 'en')

    return is_english

# Example usage
# text = "cia blat"
# print(is_text_english(text))  # Should return True for English text
