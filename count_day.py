import configparser
import db_ops
import telebot
from telebot import types

config = configparser.ConfigParser()
config.read('balde.conf')

TOKEN = config['BALDE']['TOKEN']
bot = telebot.TeleBot(TOKEN)
channelid = config['BALDE']['CHANNELID']

button2 = types.InlineKeyboardMarkup()
button_ask = types.InlineKeyboardButton('Eu quero!', callback_data="/quero")
button2.row(button_ask)

posts = db_ops.selectbigger('Balde', 'days', 0)
for post in posts:
    days_left = post[4]-1
    if days_left == 0:
        desc = '{}\nPrazo expirado.'.format(post[3])
        bot.edit_message_caption(desc, channelid, post[1], parse_mode='HTML')
        bot.unpin_chat_message(channelid, post[1])
    elif int(post[5]) > 0:
        desc = '{}\n<a href="tg://user?id={}">{}</a> tem {} dias para buscar.'.format(post[3], post[5], post[6], days_left)
        bot.edit_message_caption(desc, channelid, post[1], parse_mode='HTML')
    else:
        desc = '{}\nDias restantes no balde: {}'.format(post[3], days_left)
        bot.edit_message_caption(desc, channelid, post[1], parse_mode='HTML', reply_markup=button2)
    db_ops.update('Balde', 'days', days_left, 'post', post[1])
