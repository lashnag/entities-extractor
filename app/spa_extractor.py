import dateparser
from dateparser.search import search_dates
from regexp_extractor import extract_money

RANGE_PREPOSITIONS = {'al', 'hasta'}

def extract_entities(message):
    dates = []
    date_intervals = []
    date_entities = extract_dates(message)

    i = 0
    while i < len(date_entities):
        text, _, end = date_entities[i]
        if i + 1 < len(date_entities):
            next_text, next_start, _ = date_entities[i + 1]
            if message[end:next_start].strip().lower() in RANGE_PREPOSITIONS:
                d1 = dateparser.parse(text, languages=['es'])
                d2 = dateparser.parse(next_text, languages=['es'])
                if d1 and d2:
                    date_intervals.append({
                        'first': f"{d1.year}-{d1.month:02d}-{d1.day:02d}",
                        'second': f"{d2.year}-{d2.month:02d}-{d2.day:02d}"
                    })
                    i += 2
                    continue
        parsed = dateparser.parse(text, languages=['es'])
        if parsed:
            dates.append(f"{parsed.year}-{parsed.month:02d}-{parsed.day:02d}")
        i += 1

    return {
        'dates': dates,
        'date_intervals': date_intervals,
        'moneys': extract_money(message)
    }

def extract_dates(message):
    results = search_dates(message, languages=['es']) or []
    date_entities = []
    search_from = 0
    for text, _ in results:
        pos = message.find(text, search_from)
        if pos != -1:
            date_entities.append((text, pos, pos + len(text)))
            search_from = pos + len(text)
    return date_entities
