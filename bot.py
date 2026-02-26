import os
import telebot
from telebot.types import LabeledPrice
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
PROVIDER_TOKEN = os.getenv("PROVIDER_TOKEN")

bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот магазина.\nНажмите /pay, чтобы протестировать оплату."
    )


@bot.message_handler(commands=['pay'])
def pay(message):
    chat_id = message.chat.id

    title = "Тестовый товар"
    description = "Демонстрация оплаты"
    payload = "test-invoice-001"
    currency = "BYN"
    price = 10.00

    prices = [LabeledPrice(label=title, amount=int(price * 100))]

    bot.send_invoice(
        chat_id=chat_id,
        title=title,
        description=description,
        invoice_payload=payload,
        provider_token=PROVIDER_TOKEN,
        currency=currency,
        prices=prices,
        start_parameter="start-param"
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(
        message.chat.id,
        f"Спасибо за оплату! "
        f"{message.successful_payment.total_amount / 100:.2f} "
        f"{message.successful_payment.currency}"
    )


bot.polling(none_stop=True)