#!/usr/bin/env python2
from pwn import * # https://pypi.python.org/pypi/pwntools
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('host', nargs='?', default='107.170.122.6')
parser.add_argument('port', nargs='?', default=7765, type=int)
args = parser.parse_args()

header = 'ENCRYPT:'
def query(s):
    with remote(args.host, args.port) as p:
        log.info('try: ' + repr(header + s))
        p.recvuntil('Send me some hex-encoded data to encrypt:\n')
        p.sendline(s.encode('hex'))
        p.recvuntil('Here you go:')
        t = p.recvline().strip()
        u = []
        while t:
            u.append(t[:32])
            t = t[32:]
        log.info(repr(u))
        return u

import string
flag = ''
while True:
    padding = '#' * ((- len(header + flag + 'A')) % 16)
    assert len(header + padding + flag + 'A') % 16 == 0
    i =    len(header + padding + flag + 'A') // 16 - 1
    correct = query(padding)[i]
    for c in list(string.printable):
        if query(padding + flag+ c)[i] == correct:
            flag += c
            log.success('flag updated: ' + repr(flag))
            break
    else:
        break
log.success('flag: ' + repr(flag))
