#!/usr/bin/env python

import simple_des

ciphertext = ['01100101', '00100010', '10001100', '01011000', '00010001', '10000101']
key = simple_des.ascii_to_bin("Mu")

f = simple_des.SimpleDES(key)

flag = simple_des.bin_to_ascii(''.join(f.decrypt(ciphertext)))
print("Gigem{" + ''.join(flag) + "}")


