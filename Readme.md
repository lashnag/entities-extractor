Сервис для извлечения из текста сущностей

Запускается на локальном порту 4319

Пример запроса POST /extract {'message' : 'Летим из москвы в стамбул 3 ноября за 10000 рублей или в дубай с 10 по 19 октября'}

Пример ответа {'entities' [
    'dates' : ['2025-11-03'],
    'moneys' : ['10000'],
    'date_intervals': ['2025-10-10-2025-10-19']
]}