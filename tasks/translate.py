from deep_translator import GoogleTranslator

def translate_text(text, target_language='en'):
    translated_text = GoogleTranslator(source='auto', target=target_language).translate(text)
    return translated_text