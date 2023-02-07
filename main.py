import telebot
from telebot import types
from auth_data import token
from collect_data import get_weather, get_crypto_price


def telegram_bot(token: str):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start", "help"])
    def start(message):
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton("Weather", callback_data="weather")
        btn2 = types.InlineKeyboardButton(
            "Course of cryptocurrencies", callback_data="crypto"
        )
        msg = ("Hi friend, I can send you information about the weather"
               " or course of cryptocurrencies. What do you want to do?")
        markup.add(btn1, btn2)
        bot.send_message(
            message.chat.id,
            msg,
            reply_markup=markup,
        )

    @bot.callback_query_handler(func=lambda c: c.data == "weather")
    def process_callback_button(callback_query: types.CallbackQuery):

        def send_weather(message):
            try:
                weather_data = get_weather(message.text)
                bot.send_message(
                    message.chat.id,
                    f"Today is {weather_data[0]}\n"
                    f"The temperature will be in the gap of {weather_data[1]}"
                    f" to {weather_data[2]}°C\n"
                    f"{weather_data[3]}\nCondition: {weather_data[4]}",
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn, something was wrong..."
                )

        bot.answer_callback_query(callback_query.id)
        msg = bot.send_message(
            callback_query.from_user.id,
            "Write the name of your city"
        )
        bot.register_next_step_handler(msg, send_weather)

    @bot.callback_query_handler(func=lambda c: c.data == "crypto")
    def process_callback_button(callback_query: types.CallbackQuery):

        def send_crypto(message):
            try:
                crypto_data = get_crypto_price(message.text)
                bot.send_message(message.chat.id, crypto_data)
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Damn, something was wrong..."
                )

        bot.answer_callback_query(callback_query.id)
        msg = bot.send_message(
            callback_query.from_user.id,
            "Write a couple of currencies you are interested"
            " in in format 'btc_usdt'",
        )
        bot.register_next_step_handler(msg, send_crypto)

    bot.polling(none_stop=True, interval=0)


if __name__ == "__main__":
    telegram_bot(token)
