import telebot

from bot_config import TOKEN, allowed_currencys
from extensions import APIException, BotMainHandler

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Добро пожаловать в CurrencyBot!\n\n \
    Вы можете управлять мной, отправляя следующие команды:\n \
/start или /help - вызов инструкции по использованию бота\n \
/values - информация о всех доступных валютах\n\n \
    Для расчета цены определённого количества валюты введите команду в следующем формате:\n \
<код валюты> <код валюты, в которую нужно перевести> <количество переводимой валюты>'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def handle_get_allowed_currency(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for curr in allowed_currencys.keys():
        text += str(curr) + ' - ' + str(allowed_currencys.get(curr)) + '\n'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def calculate_currency_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Некорректное количество параметров.')

        quote, base, amount = values
        total = BotMainHandler.get_price(quote, base, amount)
    except APIException as ex:
        bot.reply_to(message, f'Ошибка пользователя:\n{ex}')
    except Exception as ex:
        bot.reply_to(message, f'Не удалось обработать команду:\n{ex}')
    else:
        text = f'Цена {amount} {quote} в {base} - {round(total, 2)}'
        bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
