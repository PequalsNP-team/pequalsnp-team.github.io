#!/usr/bin/env python

import struct
import os
from binascii import hexlify
import hashlib
import time

POWLEN = 5

def randint(bound):
    return struct.unpack('<L', os.urandom(4))[0] % bound

def step(lista,mod,l):
    if (lista[l] >= mod):
        if (l>0):
            lista[l]=0
            step(lista,mod,l-1)
        else:
            print("Overflow")
    else:
        lista[l]=lista[l]+1

def brute_with_vibrations(c,r):
    q, n = 8, 6
    ret = 0
    partial = sum([solution[i]*int(c[i]) for i in range(n)]) % q
    for j in range(3):
        vibration = j - 1
        result = (partial + q + vibration) % q
        if result == r:
            ret = 1
            break
    return ret

if __name__ == '__main__':
    lines = [line.rstrip('\n') for line in open('anacleto.txt')]
    solution,ret,index = 0,0,0
    q, n = 8, 6
    solution = [0,0,0,0,0,0]
    while (index<len(lines)):
        l = lines[index]
        coefs = l.split(', ')[0:-1]
        result = int(l.split(', ')[-1:][0])
        if(index>4): print('[%d] %s -> %d' % (index,str(coefs),result))
        while (ret != 1):
            ret = brute_with_vibrations(coefs,result)
            if ret == 0:
                if(index>4): print('Noooo -> %s' % (str(solution)[1:-1]))
                step(solution,q-1,n-1)
                index=0
            else:
                print('Maybe -> %s' % (str(solution)[1:-1]))
                index=index+1
            #time.sleep(1)
        ret = 0
    print('%s' % (str(solution)[1:-1]))
