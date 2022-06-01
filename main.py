import os
from turtle import update
from urllib import request
from xmlrpc import server
from flask import Flask
import telebot
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('b2890d83290c3c6bdcd8b56d2f56714d')
owm.supported_languages
mgr = owm.weather_manager()
Token = '5353887133:AAHecYcHJd_4YFNu71mqmZfBr-C-3uwcRxo'
bot = telebot.TeleBot(Token, parse_mode=None)
app_URL = 'https://pogodajwbot.herokuapp.com/'
server = Flask(__name__)
@server.route('/' + Token, methonds=['POST'])
def get_message():
    json_string = request.get_data().dcode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200
@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=app_URL)
    return '!', 200
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
@bot.message_handler(content_types=['text'])
def send_echo(message):
    observation = mgr.weather_at_place( message.text)
    w = observation.weather
    t = w.temperature('celsius')
    t1 = t['temp']
    t2 = t['feels_like']
    t3 = t['temp_max']
    t4 = t['temp_min']
    humb = w.humidity 
    wi = w.wind()['speed']
    cl = w.clouds 
    ti = w.reference_time('iso')
    pr = w.pressure['press']
    vd = w.visibility_distance
    answer = "В городе " + message.text + " сейчас " + str(w.detailed_status) + "\n"
    answer += f"Тeмпература сейчас {str(t1)}, ощущается как {str(t2)}, максимальная {str(t3)}, минимальная {str(t4)} "  + "\n"
    answer += "Скорость ветра: " + str(wi) + "км/ч" + "\n"
    answer += "Влажность примерно: " + str(humb) + "%" + "\n"
    answer += "Облачность сейчас примерно: " + str(cl) + "%" + "\n"
    answer += "Время взятия показаний с метиостанции: " + str(ti) + "\n"
    answer += "Давление: " + str(pr) + " ртутного столба" + "\n"
    answer += "Видимость: " + str(vd) + " Метров" + "\n"

    bot.send_message(message.chat.id, answer)
bot.polling( none_stop=True)