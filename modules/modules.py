import re
import openai
import time
from tests import test_routes


COMMANDS = {
    'start': 'Gives information about the bot',
    'help': 'Gives information about all of the available commands',
    'ping': 'Measure the execution time to run test and send a message',
    'caps your sentence': 'Converts your sentence to uppercase',
    'ask your question': 'Ask your question to the bot powered by ChatGPT'
}


def is_command(string):
    pattern = r"^\/.*$"
    return bool(re.match(pattern, string))


def get_answer(question):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=question,
        max_tokens=1024,
        n=1,
        temperature=.1,
        frequency_penalty=.1,
        presence_penalty=.1
    )
    return completion.choices[0].text


def get_running_time(start_time):
    test_routes.test_index()
    return time.time() - start_time


def hello():
    return "Hello, World!"


def content():
    return '''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            '''
