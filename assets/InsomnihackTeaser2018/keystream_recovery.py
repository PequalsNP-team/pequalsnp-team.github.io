#!/usr/bin/env python3

import sys

RULE = [86 >> i & 1 for i in range(8)]
N_BYTES = 32
N = 8 * N_BYTES

def next(x):
  x = (x & 1) << N+1 | x << 1 | x >> N-1
  y = 0
  for i in range(N):
    y |= RULE[(x >> i) & 7] << i
  return y

p = open('rule86.txt','rb')
c = open('rule86.txt.enc','rb')

plaintext = p.read(N_BYTES)
ciphertext = c.read(N_BYTES)

# print the full keystream
while plaintext:
  x = int.from_bytes(plaintext,'little') ^ int.from_bytes(ciphertext,'little')
  print(x)
  plaintext = p.read(N_BYTES)
  ciphertext = c.read(N_BYTES)
  

  
