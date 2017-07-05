import itertools
import requests
import json
import collections

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
USERNAME = 'test1294'
DECODE_URL = 'https://the.delorean.codes/api/decode'
KNOWN_FILENAME = 'known.json'

class Decoder:
    def __init__(self):
        self._read_known_words()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._write_known_words()

    def _read_known_words(self):
        try:
            with open(KNOWN_FILENAME) as reader:
                known_words = json.load(reader)
        except FileNotFoundError:
            known_words = []
        self._known_words = {data['codeword']: data for data in known_words}

    def _write_known_words(self):
        with open(KNOWN_FILENAME, 'w') as writer:
            json.dump(list(self._known_words.values()), writer, indent=2)

    def decode(self, codeword):
        if codeword in self._known_words:
            return self._known_words[codeword]
        response = requests.post(DECODE_URL, data={
            'username': USERNAME,
            'codeword': codeword,
        })
        data = response.json()
        if not data['well_formed']:
            return None
        data = dict(
            codeword=codeword,
            message=data['message'],
            message_bits=data['message_bits'])
        self._known_words[codeword] = data
        return data

def main():
    with Decoder() as decoder:
        while True:
            try:
                codeword = input('> ')
            except Exception:
                break
            data = decoder.decode(codeword)
            if data:
                print(data)
            else:
                print('bad')
    print()
    print('bye')

if __name__ == '__main__':
    main()
