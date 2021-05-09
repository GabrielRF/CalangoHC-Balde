import configparser
import db_ops
#import msgs
import telebot
from telebot import types

config = configparser.ConfigParser()
config.read('balde.conf')

TOKEN = config['BALDE']['TOKEN']
bot = telebot.TeleBot(TOKEN)
channelid = config['BALDE']['CHANNELID']
groupid = config['BALDE']['GROUPID']

button1 = types.InlineKeyboardMarkup()
button_post = types.InlineKeyboardButton('Postar', callback_data="/postar")
button1.row(button_post)
button2 = types.InlineKeyboardMarkup()
button_ask = types.InlineKeyboardButton('Eu quero!', callback_data="/quero")
button2.row(button_ask)

MEMBER = ['creator', 'administrator', 'member']
COMMANDS = ['/start']

def check_member(chatid, userid):
    status = bot.get_chat_member(chatid, userid).status
    if status in MEMBER:
        return True
    return False

@bot.message_handler(commands=['start', 'cancelar'])
def bot_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if not check_member(groupid, message.chat.id):
        bot.reply_to(message, 'https://calango.club')
    else:
        bot.reply_to(message, 'Para acrescentar algo ao balde, por favor, me envie uma foto do ítem.')

@bot.message_handler(content_types=['photo'])
def bot_photo(message):
    if not check_member(groupid, message.chat.id):
        bot.reply_to(message, 'https://calango.club')
    else:
        bot.send_chat_action(message.chat.id, 'typing')
        photo = message.photo[0].file_id
        db_ops.delete('Balde', 'post', message.chat.id)
        db_ops.add('Balde', photo, str(message.chat.id))
        msg = bot.reply_to(message, 'Envie uma descrição')
        bot.register_next_step_handler(msg, add_desc)

def add_desc(message):
    bot.send_chat_action(message.chat.id, 'typing')
    if message.content_type != "text":
        bot.reply_to(message, 'Erro. Por favor, envie /start')
    elif message.text not in COMMANDS:
        db_ops.update('Balde', 'desc', message.text, 'post', str(message.chat.id))
        post_sample = db_ops.select('Balde', 'post', str(message.chat.id))
        bot.send_photo(message.chat.id, post_sample[2], post_sample[3], reply_markup=button1)

@bot.callback_query_handler(lambda q: q.data == "/postar")
def post(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
    bot.edit_message_caption(call.message.caption, call.from_user.id, call.message.id)
    desc = '{}\nDias restantes no balde: {}'
    msg = bot.send_photo(channelid, call.message.photo[0].file_id, desc.format(call.message.caption, 7), reply_markup=button2)
    bot.pin_chat_message(channelid, msg.message_id, disable_notification=True)
    db_ops.update('Balde', 'post', msg.message_id, 'post', str(call.from_user.id))


@bot.callback_query_handler(lambda q: q.data == "/quero")
def want(call):
    try:
        bot.answer_callback_query(call.id)
    except:
        pass
   
    if check_member(groupid, call.from_user.id):
        post_text = db_ops.select('Balde', 'post', str(call.message.id))
        want_msg = '{}\n<a href="tg://user?id={}">{}</a> tem 7 dias para buscar.'.format(post_text[3], call.from_user.id, call.from_user.first_name)
        bot.edit_message_caption(want_msg, channelid, call.message.id, parse_mode='HTML')
        db_ops.update('Balde', 'newp', call.from_user.id, 'post', call.message.id)
        db_ops.update('Balde', 'name', call.from_user.first_name, 'post', call.message.id)
        db_ops.update('Balde', 'days', 7, 'post', call.message.id)
        bot.unpin_chat_message(channelid, call.message.id)

@bot.message_handler(content_types=['pinned_message'])
@bot.channel_post_handler(content_types=['pinned_message'])
def generic_file(message):
    bot.delete_message(channelid, message.message_id)

bot.polling()
