import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message:telebot.types.Message):
    text = 'Чтобы начать работу, введите команду боту в следующем формате: \n<имя валюты> \
<в какую валюту перевести> \n <количество переводимой валюты> \nУвидеть список всех доступных валют: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message:telebot.types.Message):
    text = 'Доступные валюты'
    for key in keys.keys():
        text = '\n'.join((text,key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
             raise ConvertionException('Некорректно введен запрос')
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        sum = total_base * float(amount)
        text = f'Цена{amount} {quote} в {base} - {sum}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)













