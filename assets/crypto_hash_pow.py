#!/usr/bin/python

import os
import itertools

# SHA stands for SHA1
from Crypto.Hash import SHA

from pwn import *

HOST = 'ac1.pwn.seccon.jp'
PORT = 31337

POWLEN = 5

conn = remote(HOST, PORT)
conn.recvline()
challenge = '00000'
prefix = conn.recvline().split()[1]
print "[*] Got prefix: " + prefix

# Given a random prefix from the server,
# Compute an hash that verify the following condition
# sha1(prefix+str) starts with '00000'

responsehash = ""
charset = "abcdefghijklmnopqrstuvwxyz0123456789"

for i in itertools.product(charset, repeat=5):
	responsehash = SHA.new(prefix+''.join(i)).hexdigest()

	if responsehash[:POWLEN] == challenge:
		response = ''.join(i)
		break

print "[*] Sending challenge response: " + response
conn.sendline(response)

conn.interactive()

exit()
