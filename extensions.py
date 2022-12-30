import requests
import json
from config import keys
class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote:str, base:str, amount:str):
        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}.')
        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество{amount}')
        r = requests.get(f'https://api.getgeoapi.com/v2/currency/convert?api_key=977de9c150f3aee01064983b4209c50fbb804303&from={quote_ticket}&to={base_ticket}&amount={amount}&format=json')
        total_base = json.loads(r.content)['rates'][keys[base]]['rate_for_amount']
        return total_base