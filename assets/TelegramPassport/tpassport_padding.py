import random
import json
import os
import string
from base64 import b64decode, b64encode
from Crypto.Cipher import AES
from hashlib import md5

BLOCK_SIZE = 16
IV = '\x00' * BLOCK_SIZE
key = md5(''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)).encode('utf8')).hexdigest()


def pad2(s):
    len_s = len(s)
    bytes_to_add = 32 + random.randrange(0, 255 - 32 - BLOCK_SIZE)
    bytes_to_add += BLOCK_SIZE - (bytes_to_add + len_s) % BLOCK_SIZE
    return s + chr(bytes_to_add) + os.urandom(bytes_to_add - 1)


def pad(s):
    len_s = len(s)
    bytes_to_add = random.randrange(0, BLOCK_SIZE)
    bytes_to_add += BLOCK_SIZE - (bytes_to_add + len_s) % BLOCK_SIZE
    return s + chr(bytes_to_add) + os.urandom(bytes_to_add - 1)


def unpad(s):
    start = s.find("}") + 1
    print(start, len(s))
    if start <= 0:
        return None
    if start >= len(s):
        print(len(s), True)
        return s
    padding_info = ord(s[start])
    print(len(s[start:]), padding_info, len(s[start:]) == padding_info)
    return s[:start] if len(s[start:]) == padding_info else None


def encrypt(raw):
    praw = pad(str(raw))
    cipher = AES.new(key, AES.MODE_CBC, IV)
    return b64encode(cipher.encrypt(praw)), len(raw)


def decrypt(enc):
    enc = b64decode(enc)
    print(repr(enc))
    cipher = AES.new(key, AES.MODE_CBC, IV)
    unp = cipher.decrypt(enc)
    print(repr(unp))
    unp = unpad(unp)
    return None if unp is None else unp


if __name__ == "__main__":
    msg = {}
    msg["data"] = "ciao"
    msg = json.dumps(msg)
    a = pad(msg)
    m = unpad(a)

    assert(len(a) - len(msg) == ord(a[len(msg)]))
    assert(m is not None)

    print(a, m)
    # print("All Fine")
