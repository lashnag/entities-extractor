import re

def extract_money(text):
    default_currency = "RUB"  # По умолчанию рубли
    currency_hints = {
        "usd": "USD", "$": "USD",
        "eur": "EUR", "€": "EUR",
        "руб": "RUB", "рублей": "RUB", "₽": "RUB", "р": "RUB"
    }
    for word, iso_code in currency_hints.items():
        if word.isalnum():
            pattern = rf"\b{re.escape(word)}\b"
        else:  # Для символов валют
            pattern = re.escape(word)
        if re.search(pattern, text, re.IGNORECASE):
            default_currency = iso_code
            break

    money_regex = re.compile(r"\d{3,}")
    raw_money_values = money_regex.findall(text)

    cleaned_money_values = []
    for money_value in raw_money_values:
        cleaned_value = money_value.replace(" ", "").replace(".", "").replace(",", "")

        if not (len(cleaned_value) == 4 and cleaned_value.startswith("202")): # Исключаем год
            cleaned_money_values.append({
                "amount" : int(cleaned_value),
                "currency": default_currency
            })

    return cleaned_money_values