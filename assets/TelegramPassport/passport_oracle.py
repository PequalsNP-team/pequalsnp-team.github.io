import requests
from base64 import b64decode, b64encode
import itertools

MAIN_PAGE = "http://127.0.0.1:9999{}"
BLOCK_SIZE = 16


def request(url, data=None, method='GET', cookies=None):
    r = requests.request(method, MAIN_PAGE.format(url), data=data, cookies=cookies, allow_redirects=False)
    if r.status_code == 200:
            return r.text
    else:
            return str(r.status_code)


def encrypt(msg):
    # print("-> msg - {}".format(msg))
    payload = {'msg': msg}
    return request("/encrypt", data=payload, method='POST')


def decrypt(msg):
    # print("-> msg - {}".format(msg))
    payload = {'msg': msg}
    return request("/decrypt", data=payload, method='POST')


def oracle(token):
    magic = decrypt(token)
    # print(magic)
    return 'Padding Error' in magic


def check(last, i):
    b = last[i]
    payload = last[:i] + bytes([b ^ 255]) + last[i + 1:]
    print(payload, len(payload))
    print("flipping bit at pos {}".format(i))
    if oracle(b64encode(payload)) is True:
        payload = last[:i] + bytes([b ^ 127]) + last[i + 1:]
        print(payload, len(payload))
        print("verifying bit at pos {}".format(i))
        if oracle(b64encode(payload)) is True:
            return True
    return False


def brute_padding(last):
    for i in range(0, len(last), 1):
        if check(last, i):
            print("Found i: {}".format(i))
            break
    return i


starting_message = "{'data':'helloworld'}"
print("plaintext payload size: {}".format(len(starting_message)))
starting_message = encrypt("{'data':'helloworld'}")
print(starting_message)
print("base64 payload size: {}".format(len(starting_message)))
s = b64decode(starting_message)
print("encrypted payload size: {}".format(len(s)))
c = [s[c:c + BLOCK_SIZE] for c in range(0, len(s), BLOCK_SIZE)]
print(s)

print("starting the oracle")

l = brute_padding(s)
print("plaintext size should be {}".format(l + 1 + BLOCK_SIZE))

# first block is xored with the iv :(
c0 = c[0]
c1 = c[1]
p1 = b'}'
k = []

# bruteforce all the bytes in the block
for j in range(l):
    j += BLOCK_SIZE - l
    # starting filler
    z0 = b'\x00' * (BLOCK_SIZE - j - 1)
    # ending filler
    z1 = b'\x00' * (j - 1)
    print("Round {}".format(j))
    # the plaintext block ends with }
    if j == 0:
        for i in range(256):
            b1 = z0 + bytes([i])
            print(p1, b1 + c1)
            if not oracle(b64encode(b1 + c1)):
                k.append(i)
                print(i ^ ord('}') ^ c0[i])
                p1 = bytes([i ^ ord('}') ^ c0[j]]) + p1
                break
    else:
        for i in itertools.product(range(1, 255), repeat=2):
            if i[1] in k:
                continue
            b1 = z0 + bytes(i) + z1
            print(p1, b1 + c1)
            if not oracle(b64encode(b1 + c1)):
                b1 = bytes([255 if b == 0 else b for b in b1])
                if not oracle(b64encode(b1 + c1)):
                    k.append(i[0])
                    p1 = bytes([i[0] ^ ord('}') ^ c0[BLOCK_SIZE - j - 1]]) + p1
                    break

print(p1)
