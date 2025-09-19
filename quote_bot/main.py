import logging
import os

from dotenv import load_dotenv
from telebot import TeleBot, apihelper

from api_telegram_handler import get_all_quotes, get_random_item, search_quote
from api_translate import clean_author, translate
from ai_bot import getBotQuote
from proxy import custom_proxy

is_ai_respond = False
load_dotenv()
bot = TeleBot(os.getenv("TOKEN"))
# setup custom proxy
apihelper.CUSTOM_REQUEST_SENDER = custom_proxy

def response_bot(message, quote, av):
    if av == 'ai':
        bot.reply_to(message, quote)
    else:
        tr_quote = dict()
        tr_quote["quote"] = translate(quote["quote"])
        tr_quote["person"] = translate(clean_author(quote["person"]))
        message_repl = f'{quote["person"]} says:\t\n{quote["quote"]}\n\n{tr_quote["person"]} میگه:\t\n{tr_quote["quote"]}'
        bot.reply_to(message, message_repl)


@bot.message_handler(commands=["start"])
def greetUser(message):
    """It gives a welcome to user"""
    bot.send_message(message.chat.id, "Hello {}!".format(message.from_user.first_name))


@bot.message_handler(commands=["random"])
def getRandomQuote(message):
    """It return a random qoute, with translation."""
    global is_ai_respond
    if is_ai_respond:
        is_ai_respond = False
        quote = getBotQuote(message.text)
        response_bot(message, quote, 'ai')
        return
    quotes = get_all_quotes()
    quote = get_random_item(quotes)

    response_bot(message, quote, 'hu')


@bot.message_handler(commands=["kword"])
def getKwordBot(message):
    global is_ai_respond
    is_ai_respond = True
    bot.send_message(message.chat.id, '✨ AI is ready to take over!!!')


@bot.message_handler(commands=["help"])
def getHelp(message):
    """It sends a short instruction."""
    bot.send_message(
        message.chat.id,
        """ربات تلگرامی سخنان ارزشمند توشته شده با پایتون:
    /start: شروع برنامه،
    /random: سخنان تصادفی،
    /kword: با کمک مدل زبانی یک سخن تصادفی طبق کلمه انتخابی شما می‌آورد,
    /help: طرز استفاده،
    `یک کلمه وارد کنید تا یک سخن تصادفی طبق آن کلمه دریافت کنید.`""",
    )


@bot.message_handler(func=lambda message: True)
def handleMessage(message):
    """It gets a keyword, and returns a random quote{person, quote} , based on that, with translation."""
    global is_ai_respond
    if is_ai_respond:
        is_ai_respond = False
        quote = getBotQuote(message.text)
        response_bot(message, quote, 'ai')
        return
    quotes = search_quote(message.text.strip())
    if len(quotes):
        quote = get_random_item(quotes)
        response_bot(message, quote, 'hu')
    else: # or else no quote
        bot.reply_to(message, message.text + "\nno quote found``\\_(^-^)_/")


bot.polling(interval=10, logger_level=logging.INFO)
