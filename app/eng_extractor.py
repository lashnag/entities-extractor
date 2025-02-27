import dateparser
from regexp_extractor import extract_money
import spacy

def extract_entities(message):
    dates = []
    for string_date in extract_dates(message):
        parsed_date = dateparser.parse(string_date, languages=['en'])
        dates.append(f"{parsed_date.year}-{parsed_date.month:02d}-{parsed_date.day:02d}")

    return {
        'dates': dates,
        'moneys': extract_money(message)
    }

def extract_dates(message):
    doc = nlp_en(message)
    date_strings = []

    for entity in doc.ents:
        if entity.label_ == 'DATE':
            date_strings.append(entity.text)

    return date_strings

def load_or_download_model(model_name):
    try:
        nlp = spacy.load(model_name)
        print(f"Модель {model_name} успешно загружена.")
    except OSError:
        print(f"Модель {model_name} не найдена. Скачивание...")
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)
        print(f"Модель {model_name} успешно скачана и загружена.")
    return nlp

nlp_en = load_or_download_model("en_core_web_md")