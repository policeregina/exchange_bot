import telebot
from config import TOKEN, keys
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['help','start'])
def help (message: telebot.types.Message):
    text = 'Этот бот создан для того, чтобы перевести валюту в нужную вам.\n ' \
           'Чтобы начать работу, введите команду в следующем формате: \n' \
           '<имя валюты> <в какую хотите перевести> <количество переводимой валюты>. \n' \
           '\n'\
           'Чтобы увидеть список всех валют, введите команду /values. \n'\
           'Пожалуйста, указывайте валюту в именительном падеже, единственном числе.\n' \
           'Если название валюты состоит из двух слов, пишите их без пробела. Например, турецкаялира.'
    bot.reply_to(message,text)

@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message,text)


@bot.message_handler(content_types = ['text'])
def convert(message: telebot.types.Message):
    try:
        val = message.text.split(' ')
        if len(val) != 3:
            raise APIException('Введено неверное количество параметров.')
        quote, base, amount = val
        total_base = CurrencyConverter.get_price(quote,base,amount)
    except APIException as e:
        bot.reply_to(message,f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду.\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id,text)

bot.polling()