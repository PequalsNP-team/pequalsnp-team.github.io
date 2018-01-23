#!/usr/bin/python3

l1=[b'\x00', b'\x2b', b'\x55', b'\x80', b'\xaa', b'\xd5', b'\xff']
l2=[b'\x00', b'\x33', b'\x66', b'\x99', b'\xcc', b'\xff']

header = b'\x47\x49\x46\x38\x39\x61\x67\x02\xE6\x00\xF7\x00\x00'

ary = b'' + header
for i in l2:
    for j in l1:
        for k in l2:
            ary += i + j + k

gne = open('hint_full.gif', 'wb')
gne.write(ary)
gne.close()

# l1 l2 l1 l1 l2 l1 l1 l2 l1 l1 l2 l1 l1 l2 l1 l1 l2 l1
# 00 00 00 00 00 33 00 00 66 00 00 99 00 00 CC 00 00 FF
# 00 2B 00 00 2B 33 00 2B 66 00 2B 99 00 2B CC 00 2B FF
# 00 55 00 00 55 33 00 55 66 00 55 99 00 55 CC 00 55 FF

