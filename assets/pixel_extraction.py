import binascii
from PIL import Image

new = Image.open('cat_with_secrets.png').load()
old = Image.open('cat_with_secrets_original.jpg').load()

width = 512

in_hex = ''

for y in range(3):
    for x in range(width):
        if (y, x) <= (2, 125) and new[x, y] != old[x, y]:
            in_hex += '%x' % (x % 16)

print(binascii.unhexlify(in_hex))