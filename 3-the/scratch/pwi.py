import collections
import pickle
import re
import requests

USERNAME = 'test1294'
CHALLENGE_URL = 'https://the.delorean.codes/api/challenge'
EXAMPLES_URL = 'https://the.delorean.codes/api/examples'
DECODE_URL = 'https://the.delorean.codes/api/decode'

WordInfo = collections.namedtuple('WordInfo', ['word', 'pos', 'letter'])


def get_challenge():
    return requests.get(CHALLENGE_URL, params={
        'username': USERNAME,
    }).json()['message']


def get_examples():
    return requests.get(EXAMPLES_URL, params={
        'username': USERNAME,
    }).json()


def decode(codeword):
    response = requests.post(DECODE_URL, data={
        'username': USERNAME,
        'codeword': codeword,
    })
    data = response.json()
    if not data['well_formed']:
        return None
    return data['message']


def vocab_to_pwi(vocab):
    pwi = {}
    pos = 0
    prefix = []
    while True:
        new_vocab = []
        for word in vocab:
            message = decode(' '.join(prefix + [word]))
            if not message:
                new_vocab.append(word)
                continue
            letter = message[-1]
            wi = WordInfo(word, pos, letter)
            pwi.setdefault(pos, []).append(wi)
            print(wi)
        if not new_vocab or pos not in pwi:
            break
        prefix.append(pwi[pos][0].word)
        pos += 1
        vocab = new_vocab
    return pwi


def merge_pwis(pwis):
    result = {}
    for pwi in pwis:
        for pos, wis in pwi.items():
            result.setdefault(pos, set()).update(wis)
    return result


def examples_to_pwi(examples):
    pwis = [vocab_to_pwi(example['codeword'].split()) for example in examples]
    return merge_pwis(pwis)


def get_pwi_from_examples():
    return examples_to_pwi(get_examples())


def maybe_pickle(filename, getter):
    try:
        with open(filename, 'rb') as reader:
            return pickle.load(reader)
    except Exception:
        pass
    result = getter()
    with open(filename, 'wb') as writer:
        pickle.dump(result, writer)
    return result


def get_pwi_from_top100():
    vocab = set()
    with open('data/top100.txt', 'r') as reader:
        for line in reader.readlines():
            word = line.strip()
            vocab.add(word)
    print(vocab)
    return vocab_to_pwi(vocab)


def get_pwi_from_btf(n=300):
    with open('data/btf_transcript.txt', 'r') as reader:
        text = reader.read()
    text = text.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    vocab = collections.Counter(re.findall(r'[a-z]+', text))
    vocab = [word for word, count in vocab.most_common(n)]
    print(vocab)
    return vocab_to_pwi(vocab)


def main():
    challenge = maybe_pickle('cache/challenge.pickle', get_challenge)
    print(challenge)
    pwi = maybe_pickle('cache/pwi_from_btf.pickle', get_pwi_from_btf)
    print(pwi)
    pwi = maybe_pickle('cache/pwi_from_examples.pickle', get_pwi_from_examples)
    print(pwi)
    pwi = maybe_pickle('cache/pwi_from_top100.pickle', get_pwi_from_top100)
    print(pwi)


if __name__ == '__main__':
    main()
