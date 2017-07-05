import collections
import pickle
import re
import requests

USERNAME = 'test1294'
CHALLENGE_URL = 'https://the.delorean.codes/api/challenge'
EXAMPLES_URL = 'https://the.delorean.codes/api/examples'
DECODE_URL = 'https://the.delorean.codes/api/decode'

WordInfo = collections.namedtuple('WordInfo', ['word', 'pos', 'letter'])


def decode(codeword):
    response = requests.post(DECODE_URL, data={
        'username': USERNAME,
        'codeword': codeword,
    })
    data = response.json()
    if not data['well_formed']:
        return None
    return data['message']


def get_challenge():
    return requests.get(CHALLENGE_URL, params={
        'username': USERNAME,
    }).json()['message']


def get_vocab(n=None):
    with open('data/btf_transcript.txt', 'r') as reader:
        text = reader.read()
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    vocab = collections.Counter(re.findall(r'[a-z]+', text))
    if n is None:
        n = len(vocab)
    vocab = [word for word, count in vocab.most_common(n)]
    return vocab


def main():
    challenge = get_challenge()
    vocab = get_vocab()

    try:
        from cache.pwi import pwi
        print('loaded cached PWI')
    except Exception:
        pwi = {}
        print('starting clean')

    vocab = set(vocab)
    for pos, wis in pwi.items():
        for wi in wis:
            vocab.remove(wi.word)
    vocab = list(vocab)

    print(vocab)
    print(challenge)

    sentence = []
    for pos, letter in enumerate(challenge):
        if pos in pwi:
            for wi in pwi[pos]:
                if wi.letter == letter:
                    sentence.append(wi.word)
                    print(wi)
                    break
            if len(sentence) == pos + 1:
                continue
        new_vocab = []
        for i, word in enumerate(vocab):
            message = decode(' '.join(sentence + [word]))
            if not message:
                new_vocab.append(word)
                continue
            new_letter = message[-1]
            wi = WordInfo(word, pos, new_letter)
            pwi.setdefault(pos, set()).add(wi)
            print(wi)
            if new_letter == letter:
                new_vocab.extend(vocab[i + 1:])
                break
        else:
            print('letter {} not found'.format(letter))
            break
        print()
        sentence.append(word)
        vocab = new_vocab

    print(' '.join(sentence))


if __name__ == '__main__':
    main()
