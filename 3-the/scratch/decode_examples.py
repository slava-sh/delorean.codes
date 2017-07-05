import json

BITS_PER_CHAR = 5

def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]

def main():
    #with open('examples.json') as reader:
    #    examples = json.load(reader)
    with open('known.json') as reader:
        examples = json.load(reader)

    num_to_letter = {}
    letter_to_word = {}
    for example in examples:
        codeword = example['codeword']
        message = example['message']
        message_bits = example['message_bits']
        assert len(message_bits) / len(message) == BITS_PER_CHAR
        print()
        print(example)
        num_xor = 0
        num_sum = 0
        for word, letter, letter_bin in zip(codeword.split(),
                                            message,
                                            chunks(message_bits, BITS_PER_CHAR)):
            letter_num = int(letter_bin, 2)
            print(letter, letter_bin, letter_num)
            num_to_letter[letter_num] = letter
            num_xor ^= letter_num
            num_sum += letter_num
            letter_to_word.setdefault(letter, []).append(word)
        print('code len: {:>3}'.format(len(codeword)))
        print('letters:  {:>3}'.format(len(message)))
        print('xor:      {:>3}'.format(num_xor))
        print('sum:      {:>3}'.format(num_sum))
        print(letter_to_word)

    for num, letter in sorted(num_to_letter.items()):
        print(num, letter)

if __name__ == '__main__':
    main()
