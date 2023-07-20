import re
import time
import random
import os
import requests
from dotenv import load_dotenv
from tests import test_routes

load_dotenv()

COMMANDS = {
    'start': 'Gives information about the bot',
    'help': 'Gives information about all of the available commands',
    'ping': 'Measure the execution time to run test and send a message',
    'caps your sentence': 'Converts your sentence to uppercase',
    'ask your question': 'Ask your question to the bot powered by ChatGPT',
    'short URL customURL': 'Shorten your URL with optional custom URL',
    'rand option1 option2': 'Randomly choose one of the options',
    'team nteam member1 member2': 'Randomly assign members to teams',
    'stats': 'Get statistics of a GitHub repository',
}


def is_command(string):
    pattern = r"^\/.*$"
    return bool(re.match(pattern, string))


def get_answer(question):
    try:
        API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
        TOKEN = os.getenv('HF_TOKEN')
        headers = {"Authorization": "Bearer " + TOKEN}
        response = requests.post(API_URL, headers=headers, json={"inputs": question})
        result = response.json()
        return result[0]['generated_text']
    except:
        return "Error, sorry something went wrong!"


def get_running_time(start_time):
    test_routes.test_index()
    return time.time() - start_time


# using djago validators
# https://github.com/django/django/blob/stable/1.3.x/django/core/validators.py#L45
def is_valid_url(url):
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        # domain...
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None


def is_valid_custom(custom):
    pattern = r'^[\w-]+$'
    return re.match(pattern, custom)


def get_random_team(n_team, member_list):
    result = ''
    if n_team > len(member_list):
        result = 'Too many teams!'
    elif n_team < 1:
        result = 'Too few teams!'
    else:
        n_plus = len(member_list) % n_team
        length = len(member_list)
        result = ''
        for i in range(n_team):
            result += 'Team {}:\n'.format(i+1)
            if i < n_plus:
                result += member_list.pop(
                    random.randint(0,
                                   len(member_list) - 1)) + '\n'
            for j in range(length // n_team):
                result += member_list.pop(
                    random.randint(0,
                                   len(member_list) - 1)) + '\n'
            result += '\n'
    return result


def get_github_stats(username, repo):
    API_BASE = f'https://api.github.com/repos/{username}/{repo}'
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
    RESULT = ''
    DATA_DICT = {'Name': 'name', 'Watchers': 'watchers_count', 'Forks': 'forks_count',
                 'Stars': 'stargazers_count', 'Issues': 'open_issues_count', 'Language': 'language'}
    try:
        response = requests.get(
            API_BASE,
            headers={
                'Accept': 'application/vnd.github+json',
                'Authorization': 'Bearer {}'.format(GITHUB_TOKEN),
                'X-GitHub-Api-Version': '2022-11-28'
            }
        )
        r = response.json()
        for key, value in DATA_DICT.items():
            RESULT = RESULT + f"{key}: {r[value]}\n"
        commit = re.search('\d+$', requests.get(f'{API_BASE}/commits?per_page=1'
                                                ).links['last']['url']).group()
        first_commit = requests.get(
            f'{API_BASE}/commits?per_page=1&page={commit}')

        response = first_commit.json()
        first_commit_date = str(response[0]['commit']['author']['date']).replace(
            'T', ' ').replace('Z', '')
        RESULT += f"Total commit: {commit}\n"
        RESULT += f"First commit: {first_commit_date}"
        return RESULT
    except:
        return 'Username or repository not found!'


def hello():
    return "Hello, World!"


def content():
    return '''
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
            '''
