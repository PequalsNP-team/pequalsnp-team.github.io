#!/usr/bin/env python

import base64
import sys
import requests
import binascii
from urllib import parse

def block_print(c,size):
    lenc = len(c)
    i = 0
    while i < lenc:
        print(c[i:i+size])
        i += size

def decode(c):
    return binascii.hexlify(base64.b64decode(parse.unquote(c)))
    
def encode(c):
    return parse.quote(base64.b64encode(binascii.unhexlify(c)))
    
def crypt(payload):
    post = requests.post('http://url:9090/index.php', data={'cc': payload})
    c = post.cookies['pci_crypt']
    resp = requests.get('http://url:9090/index.php', cookies={'pci_crypt': c})
    s = binascii.hexlify(base64.b64decode(parse.unquote(c)))
    r = resp.text[:-len(payload)-1]    
    return s,r
    
def decrypt(ciphertext):
    ciphertext = encode(ciphertext)
    resp = requests.get('http://url:9090/index.php', cookies={'pci_crypt': ciphertext})
    print(resp.text)
    
c,p = crypt(sys.argv[1])
block_print(c,32)
block_print(p,16)
# decrypt(c)
