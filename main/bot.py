import telebot

TOKEN = '8375189884:AAFbLcLquvcZ33FdmilIYA4AJEsSV3cjwjk'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):

    text = """
🚖 SmartTaxi UZ

Buyruqlar:

/taxi - Taxi chaqirish
/help - Yordam
"""

    bot.send_message(
        message.chat.id,
        text
    )


@bot.message_handler(commands=['help'])
def help_command(message):

    bot.send_message(
        message.chat.id,
        '📍 Lokatsiya yuboring va taxi chaqiring.'
    )


@bot.message_handler(commands=['taxi'])
def taxi(message):

    keyboard = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    button = telebot.types.KeyboardButton(
        '📍 Lokatsiya yuborish',
        request_location=True
    )

    keyboard.add(button)

    bot.send_message(
        message.chat.id,
        '📍 Lokatsiyangizni yuboring',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['location'])
def location(message):

    lat = message.location.latitude
    lng = message.location.longitude

    bot.send_message(
        message.chat.id,
        f"""
🚖 Taxi topildi!

📍 Latitude: {lat}
📍 Longitude: {lng}

🚘 Driver:
JASUR

🚖 Mashina:
Chevrolet Cobalt

⭐ Rating:
4.9

📞 +998901112233

⏱ Taxi yo‘lda...
"""
    )


print('🤖 SmartTaxi Bot ishladi...')

bot.infinity_polling()