#!/usr/bin/python3

p1 = open('rule86.txt', 'rb').read()
c1 = open('rule86.txt.enc', 'rb').read()
c2 = open('super_cipher.py.enc', 'rb').read()
c3 = open('hint.gif.enc', 'rb').read()

# get the first part of the keystream
keystream = []
for a, b in zip(p1, c1):
  keystream.append(a ^ b)

# decrypt the gif file
p3 = []
for a, b in zip(keystream, c3):
  p3.append(a ^ b)
    
with open('hint2.gif', 'wb') as f:
  f.write(bytes(p3))

# run giffer.py to generate hint_full.gif

# get another keystream part
keystream = []
gif = open('hint_full.gif', 'rb').read()
for a, b in zip(c3, gif):
  keystream.append(a ^ b)

# decrypt the full python script
p2 = []
for a, b in zip(keystream, c2):
  p2.append(a ^ b)
print(bytes(p2).decode())
    
with open('super_cipher1.py', 'w') as f:
  f.write(bytes(p2).decode())
