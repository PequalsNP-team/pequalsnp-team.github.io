#!/usr/bin/python

from socket import *
from time import sleep
import telnetlib, struct
baseAlpha = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f']

def cesar(alpha,cy):
    cipherAlpha = []
    for cipherChar in alpha:
        cipherAlpha.append(cipherChar)
    key = []
    for cipherChar in cy:
        pkey = cipherAlpha.index(cipherChar.lower())
        key.append(format(pkey,"x"))
    return ''.join(key)

def shift(i,s):
    i=i+1
    p1 = s[0:i]
    p2 = s[i:32]
    return p2+p1

def vige(p,c):
    key=[]
    i=0
    for plainTextChar in p:
        pkey = int(plainTextChar,16)
        ckey = int(c[i],16)
        s = ckey-pkey
        if s<0:
            s=s+16
        key.append(format(s,"x"))
        i=i+1
    return ''.join(key)

def xorPrev(const,c):
    const=int(const,16)
    key = []
    k=const^int(c[0],16)
    for x in range(1, len(c)):
        n = int(c[x],16)
        nk = k^n
        key.append(format(k,"x"))
        k = nk
    key.append(format(nk,"x"))
    return ''.join(key)

def sumPrev(const,c):
    const=int(const,16)
    key = []
    k=int(c[0],16)-const
    if k<0:
        k=k+16
    key.append(format(k,"x"))
    for x in range(1, len(c)):
        n = int(c[x],16)
        p = int(c[x-1],16)
        nk = n-p
        if nk<0:
            nk=nk+16
        key.append(format(nk,"x"))
    return ''.join(key)

def xorSwap(const,c):
    const=int(const,16)
    key = []
    for x in range(0, len(c)):
        n = int(c[x],16)
        nk = n^const
        key.append(format(nk,"x"))
    for x in range(0, len(key)/2):
        tmp=key[x*2]
        key[x*2]=key[x*2+1]
        key[x*2+1]=tmp
    return ''.join(key)

s=socket(AF_INET, SOCK_STREAM)
host = 'localhost' #'randBox-iw8w3ae3.9447.plumbing';
port = 9447

try:
    remote_ip = gethostbyname(host)

except gaierror:
    #could not resolve
    print '- Hostname could not be resolved. Exiting'
    sys.exit()
s.connect((remote_ip, port))

# try to beat the game
lvl = 1
print "Round "+str(lvl)
workinglvl = 7

while 1:
    data = s.recv(1024).rstrip()
    if data:
        if lvl > workinglvl:
            print '> ' +data

        if "You got it!" in data:
            lvl=lvl+1
            print "Round "+str(lvl)
            if lvl > workinglvl-1:
                print '> ' +data

        # get the cipher string
        if "You need to" in data:
            cipher = data.split("'")[1]
            if lvl == 1 or lvl == 2 or lvl == 3 or lvl == 4:
                s.send("0123456789abcdef"+"\n")
                data = s.recv(1024).rstrip()
                s.recv(1024)
                s.send(cesar(data,cipher)+"\n")
            elif lvl == 5:
                s.send("00000000000000000000000000000000"+"\n")
                p = s.recv(1024).rstrip()
                s.recv(1024)
                s.send(vige(p,cipher)+"\n")
            elif lvl == 6:
                s.send("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1"+"\n")
                ind = s.recv(1024).index('1')
                s.recv(1024)
                s.send(shift(ind,cipher)+"\n")
            elif lvl == 7:
                s.send("0"+"\n")
                c = s.recv(1024).rstrip()
                s.recv(1024)
                s.send(xorPrev(c,cipher)+"\n")
            elif lvl == 8:
                s.send("0"+"\n")
                c = s.recv(1024).rstrip()
                s.recv(1024)
                s.send(sumPrev(c,cipher)+"\n")
            elif lvl == 9:
                s.send("0"+"\n")
                c = s.recv(1024).rstrip()
                s.recv(1024)
                s.send(xorSwap(c,cipher)+"\n")
            elif lvl == 10:
                s.send("0"+"\n")
                c = s.recv(1024).rstrip()
                s.recv(1024)
                s.send(xorPrev(c,cipher)+"\n")
            else:
                t = telnetlib.Telnet()
                t.sock = s
                t.interact()

s.close()
