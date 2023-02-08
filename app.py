import telebot
import os
import openai
import time
from flask import Flask
from modules import modules
from handlers.routes import configure_routes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
OWNER = os.getenv('OWNER')
openai.api_key = os.getenv('OPENAI')

bot = telebot.TeleBot(token=TOKEN, threaded=False)
app = Flask(__name__)
configure_routes(app, bot)


@bot.message_handler(commands=['start'])
def command_start(message):
    cid = message.chat.id
    bot.send_message(
        cid, "Welcome to putuwaw_bot!\nType /help to find all commands.")


@bot.message_handler(commands=['help'])
def command_help(message):
    cid = message.chat.id
    help_text = "The following commands are available: \n"
    for key in modules.COMMANDS:
        help_text += '/' + key + ': '
        help_text += modules.COMMANDS[key] + '\n'
    bot.send_message(cid, help_text)


@bot.message_handler(commands=['ping', 'p'])
def command_ping(message):
    if message.chat.id != int(OWNER):
        bot.reply_to(message, "Sorry you are not allowed to use this command!")
    else:
        start_time = time.time()
        ping = modules.get_running_time(start_time)
        bot.reply_to(message, "PONG! Running time: {:.3f} s.".format(ping))


@bot.message_handler(commands=['caps'])
def command_caps(message):
    string = str(message.text)
    caps = string.replace('/caps ', '')
    bot.reply_to(message, caps.upper())


@bot.message_handler(commands=['ask'])
def command_ask(message):
    if message.chat.id != int(OWNER):
        bot.reply_to(message, "Sorry you are not allowed to use this command!")
    else:
        string = str(message.text)
        question = string.replace('/ask ', '')
        bot.reply_to(message, modules.get_answer(question))


@bot.message_handler(func=lambda message: modules.is_command(message.text))
def command_unknown(message):
    command = str(message.text).split()[0]
    bot.reply_to(
        message, "Sorry, {} command not found!\nPlease use /help to find all commands.".format(command))
