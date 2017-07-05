import itertools
import grequests
import time

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
USERNAME = 'test1294'
DECODE_URL = 'https://the.delorean.codes/api/decode'

def chunks(items, n):
    for i in range(0, len(items), n):
        yield items[i:i + n]

def exception_handler(request, exception):
    print('exception:')
    print(exception)
    print('request:')
    print(request)

def request_chunks(requests, chunk_size=5):
    response_chunks = map(lambda chunk: grequests.map(chunk, exception_handler=exception_handler, size=chunk_size), chunks(requests, chunk_size))
    for chunk in response_chunks:
        yield from chunk

def main():
    codewords = []
    requests = []
    #for a in ALPHABET:
    #    codeword = a
    #    codewords.append(codeword)
    #    requests.append(grequests.post(DECODE_URL, data={
    #        'username': 'test1294',
    #        'codeword': codeword,
    #    }))
    #for a in ALPHABET:
    #    for b in ALPHABET:
    #        codeword = a + b
    #        codewords.append(codeword)
    #        requests.append(grequests.post(DECODE_URL, data={
    #            'username': 'test1294',
    #            'codeword': codeword,
    #        }))
    for a in ALPHABET:
        for b in ALPHABET:
            for c in ALPHABET:
                codeword = a + b + c
                codewords.append(codeword)
                requests.append(grequests.post(DECODE_URL, stream=False, data={
                    'username': 'test1294',
                    'codeword': codeword,
                }))

    for codeword, response in zip(codewords, request_chunks(requests)):
        response.close()
        print(codeword)
        continue
        data = response.json()
        if not data['well_formed']:
            continue
        print(dict(
            codeword=codeword,
            message=data['message'],
            message_bits=data['message_bits'],
        ))

if __name__ == '__main__':
    main()
