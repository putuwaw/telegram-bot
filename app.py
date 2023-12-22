import telebot
import os
import time
import requests
import random
from flask import Flask
from modules import modules
from handlers.routes import configure_routes
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
URL = os.getenv('URL')
OWNER = os.getenv('OWNER')
SHORTEN_URL_ENDPOINT = os.getenv('SHORTEN_URL_ENDPOINT')

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


@bot.message_handler(commands=['short'])
def command_team(message):
    string = str(message.text).replace('/short ', '').split()
    url = ""
    custom = ""
    if len(string) < 1:
        bot.reply_to(message, "Too few arguments!")
    elif len(string) > 2:
        bot.reply_to(message, "Too many arguments!")
    else:
        url = string[0]
        if len(string) == 2:
            custom = string[1]
        if not modules.is_valid_url(url):
            bot.reply_to(message, "URL is not valid!")
        elif not modules.is_valid_custom(custom) and custom != '':
            bot.reply_to(message, "Custom URL is not valid!")
        else:
            r = requests.post(SHORTEN_URL_ENDPOINT, json={
                'url': url,
                'custom': custom
            })
            response = r.json()
            result = response['status'] + "\n" + response['message']
            bot.reply_to(message, result)


@bot.message_handler(commands=['rand'])
def command_random(message):
    string = str(message.text)
    question = string.replace('/rand ', '').split()
    idx = random.randint(0, len(question) - 1)
    bot.reply_to(message, question[idx])


@bot.message_handler(commands=['team'])
def command_team(message):
    string = str(message.text).replace('/team ', '').split()
    if string[0].isnumeric():
        n_team = int(string[0])
        result = modules.get_random_team(n_team, string[1:])
        bot.reply_to(message, result)
    else:
        bot.reply_to(message, "First argument must be a number!")


@bot.message_handler(commands=['stats'])
def command_stats(message):
    if message.chat.id != int(OWNER):
        bot.reply_to(message, "Sorry you are not allowed to use this command!")
    else:
        string = str(message.text).replace('/stats ', '').split()
        if len(string) < 2:
            bot.reply_to(message, "Too few arguments!")
        elif len(string) > 2:
            bot.reply_to(message, "Too many arguments!")
        else:
            response = modules.get_github_stats(string[0], string[1])
            bot.reply_to(message, response)


@bot.message_handler(func=lambda message: modules.is_command(message.text))
def command_unknown(message):
    command = str(message.text).split()[0]
    bot.reply_to(
        message, "Sorry, {} command not found!\nPlease use /help to find all commands.".format(command))
