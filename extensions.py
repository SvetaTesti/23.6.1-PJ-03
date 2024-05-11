import json
import requests

from bot_config import allowed_currencys


class APIException(Exception):
    pass


class BotMainHandler:
    @staticmethod
    def check_currency(curr):
        try:
            allowed_currencys[curr]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {curr}.')

    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {quote}.')

        BotMainHandler.check_currency(quote)
        BotMainHandler.check_currency(base)

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        rq = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        total = float(json.loads(rq.content)[base]) * amount

        return total
