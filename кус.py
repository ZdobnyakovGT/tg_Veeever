import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram import ReplyKeyboardMarkup
import wikipedia
import requests
import re
import random

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

TOKEN = '5068670749:AAE7ft22D0ilYGB71KYSLlFeR32x3Ql1Wfc'

wikipedia.set_lang("ru")

reply_keyboard = [['/help', '/site'],
                  ['/find', '/goroskop'],
                  ['/kurs']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikimas = wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        for x in wikimas:
            if not('==' in x):
                if len((x.strip())) > 3:
                    wikitext2 = wikitext2+x+'.'
            else:
                break

        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)

        return wikitext2
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


def wiki(update, massage):
    update.message.reply_text(getwiki(update.message.text))


def start(update, context):
    update.message.reply_text(
        "Тут ты сможешь узнать различную информацию и стать умнее",
        reply_markup=markup
    )


def help(update, context):
    update.message.reply_text(
        "/kurs - покажет текущий курс основных валют к рублю"
        '\n'
        "/site - предложит сайт для саморазвития"
        '\n'
        "/goroskop - предсказание на день"
        '\n'
        "Так же можете узнать новою информацию с помощью кнопки /find")


def site(update, context):
    update.message.reply_text(
        "Site: https://brain-school.ru/courses/mishlenie-millionera")


def find(update, context):
    update.message.reply_text(
        "Enter text")


first = ["Сегодня — идеальный день для новых начинаний.","Оптимальный день для того, чтобы решиться на смелый поступок!","Будьте осторожны, сегодня звёзды могут повлиять на ваше финансовое состояние.","Лучшее время для того, чтобы начать новые отношения или разобраться со старыми.","Плодотворный день для того, чтобы разобраться с накопившимися делами."]
second = ["Но помните, что даже в этом случае нужно не забывать про","Если поедете за город, заранее подумайте про","Те, кто сегодня нацелен выполнить множество дел, должны помнить про","Если у вас упадок сил, обратите внимание на","Помните, что мысли материальны, а значит вам в течение дня нужно постоянно думать про"]
second_add = ["отношения с друзьями и близкими.","работу и деловые вопросы, которые могут так некстати помешать планам.","себя и своё здоровье, иначе к вечеру возможен полный раздрай.","бытовые вопросы — особенно те, которые вы не доделали вчера.","отдых, чтобы не превратить себя в загнанную лошадь в конце месяца."]
third = ["Злые языки могут говорить вам обратное, но сегодня их слушать не нужно.","Знайте, что успех благоволит только настойчивым, поэтому посвятите этот день воспитанию духа.","Даже если вы не сможете уменьшить влияние ретроградного Меркурия, то хотя бы доведите дела до конца.","Не нужно бояться одиноких встреч — сегодня то самое время, когда они значат многое.","Если встретите незнакомца на пути — проявите участие, и тогда эта встреча посулит вам приятные хлопоты."]


def goroskop(update, context):
    msg = random.choice(first) + ' ' + random.choice(second) + ' ' + random.choice(second_add) + ' ' + random.choice(third)
    update.message.reply_text(msg)


def kurs(update, context):
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    update.message.reply_text(str(data['Valute']['USD']['Value']) + '  ---  ' + str(data['Valute']['USD']['Name']))
    update.message.reply_text(str(data['Valute']['EUR']['Value']) + '  ---  ' + str(data['Valute']['EUR']['Name']))
    update.message.reply_text(str(data['Valute']['GBP']['Value']) + '  ---  ' + str(data['Valute']['GBP']['Name']))
    update.message.reply_text(str(data['Valute']['KZT']['Value']) + '  ---  ' + str(data['Valute']['KZT']['Name']))


def main():

    updater = Updater(TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("site", site))
    dp.add_handler(CommandHandler("find", find))
    dp.add_handler(CommandHandler("goroskop", goroskop))
    dp.add_handler(CommandHandler("kurs", kurs)
    )

    text_handler = MessageHandler(Filters.text, wiki)
    dp.add_handler(text_handler)

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
