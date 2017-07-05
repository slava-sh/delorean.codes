import json
import random
from decode import Decoder

def main():
    #with open('known.json') as reader:
    with open('examples.json') as reader:
        examples = json.load(reader)
    words = set()
    for example in examples:
        codeword = example['codeword']
        words.update(codeword.split())
    print(words)
    #with Decoder() as decoder:
    #    for word in words:
    #        print(word, decoder.decode(word))

    #with Decoder() as decoder:
    #    for example in examples:
    #        words = example['codeword'].split()
    #        for i in range(1, len(words) + 1):
    #            codeword = ' '.join(words[:i])
    #            print(codeword, decoder.decode(codeword))

    with Decoder() as decoder:
        words = list(words)
        while True:
            codeword = []
            for i in range(3):
                word = random.choice(words)
                codeword.append(word)
            codeword = ' '.join(codeword)
            print(codeword, decoder.decode(codeword))

if __name__ == '__main__':
    main()
