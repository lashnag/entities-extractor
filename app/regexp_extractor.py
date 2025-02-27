import re

def extract_money(text):
    money_regex = re.compile(r"\d{3,}")
    raw_money_values = money_regex.findall(text)

    cleaned_money_values = []
    for money_value in raw_money_values:
        cleaned_value = money_value.replace(" ", "").replace(".", "").replace(",", "")

        if not (len(cleaned_value) == 4 and cleaned_value.startswith("20")):
            cleaned_money_values.append(cleaned_value)

    return cleaned_money_values