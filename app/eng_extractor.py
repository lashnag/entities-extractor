import re
import dateparser
from regexp_extractor import extract_money
import spacy

RANGE_PREPOSITIONS = {'to', 'until', 'through'}

def extract_entities(message):
    dates = []
    date_intervals = []
    date_entities = extract_dates(message)

    i = 0
    while i < len(date_entities):
        text, _, end = date_entities[i]
        prep = next((p for p in RANGE_PREPOSITIONS if re.search(rf'\s{p}\s', text, re.IGNORECASE)), None)
        # "Flights from June 1 to June 10" - splits to 1 date by space
        if prep:
            parts = re.split(rf'\s+{prep}\s+', text, 1, flags=re.IGNORECASE)
            d1 = dateparser.parse(parts[0], languages=['en'])
            d2 = dateparser.parse(parts[1], languages=['en'])
            if d1 and d2:
                date_intervals.append({
                    'first': f"{d1.year}-{d1.month:02d}-{d1.day:02d}",
                    'second': f"{d2.year}-{d2.month:02d}-{d2.day:02d}"
                })
                i += 1
                continue
        # "Flights starts at 2010-01-01 ends 2010-02-01" - splits to 2 date by spacy
        if i + 1 < len(date_entities):
            next_text, next_start, _ = date_entities[i + 1]
            if message[end:next_start].strip().lower() in RANGE_PREPOSITIONS:
                d1 = dateparser.parse(text, languages=['en'])
                d2 = dateparser.parse(next_text, languages=['en'])
                if d1 and d2:
                    date_intervals.append({
                        'first': f"{d1.year}-{d1.month:02d}-{d1.day:02d}",
                        'second': f"{d2.year}-{d2.month:02d}-{d2.day:02d}"
                    })
                    i += 2
                    continue
        parsed = dateparser.parse(text, languages=['en'])
        if parsed:
            dates.append(f"{parsed.year}-{parsed.month:02d}-{parsed.day:02d}")
        i += 1

    return {
        'dates': dates,
        'date_intervals': date_intervals,
        'moneys': extract_money(message)
    }

def extract_dates(message):
    doc = nlp_en(message)
    date_ents = []

    for entity in doc.ents:
        if entity.label_ == 'DATE':
            date_ents.append((entity.text, entity.start_char, entity.end_char))

    return date_ents

def load_or_download_model(model_name):
    try:
        nlp = spacy.load(model_name)
        print(f"Model {model_name} loaded successfully.")
    except OSError:
        print(f"Cant find model {model_name}. Downloading...")
        spacy.cli.download(model_name)
        nlp = spacy.load(model_name)
        print(f"Model {model_name} downloaded and loaded successfully.")
    return nlp

nlp_en = load_or_download_model("en_core_web_md")