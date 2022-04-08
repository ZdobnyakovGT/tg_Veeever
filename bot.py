import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5068670749:AAE7ft22D0ilYGB71KYSLlFeR32x3Ql1Wfc'


reply_keyboard = [['/help', '/site'],
                  ['/find']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def echo(update, context):
    update.message.reply_text(update.message.text)


def start(update, context):
    update.message.reply_text(
        "Hi! I am music-bot. Sent part of your song to me, and I ll find it to you",
        reply_markup=markup
    )


def help(update, context):
    update.message.reply_text(
        "Sam sebe pomogej")


def site(update, context):
    update.message.reply_text(
        "Site: https://tort4u.ru/tort-shrek/image/tort-shrek-31")


def find(update, context):
    update.message.reply_text(
        "Enter text")


def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("find", find))

    text_handler = MessageHandler(Filters.text, echo)
    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
