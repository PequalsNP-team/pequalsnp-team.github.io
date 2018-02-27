#!/usr/bin/env python

import simple_des

class SimplerDES(simple_des.SimpleDES):
    def encrypt(self, data):
        if len(data[0]) == 8:
            data = simple_des.to_twelve(data)
        result = []
        for block in data:
            a,b = self.split_block(block)
            result.extend([a,b])
        data = result
        result = []
        self.schedule_key(len(data))
        Lr = data[0]
        for i in range(0,len(data)-1):
            Rr = data[i+1]
            for r in range(self.rounds):
                sk = self.subkeys[i][r]
                Lr, Rr = self.round(sk, Lr, Rr)
            result.append(Lr)
            Lr = Rr
        return result
    
    def decrypt(self, data, last):
        self.invert_key(len(data))
        result = []
        Lr = last
        for i in range(len(data),0,-1):
            i -=1 # hotfix
            Rr = data[i]
            for r in range(self.rounds):
                sk = self.subkeys[i][r]
                Lr, Rr = self.round(sk, Lr, Rr)
            result.append(Lr)
            Lr = Rr
        result.reverse()
        return result


import itertools

#fi = open('flags.txt','w')

ciphertext = ['000101','000000','100111','011001','101110','011101','001110','101111','010001','101111','110000','001001','110010','111011','110111','010001','000100','101011','100010','100010','000001','010100','001111','010010','111110','001110','000111']
key = simple_des.ascii_to_bin("Mu")

f = SimplerDES(key, rounds=4)

for i in itertools.product('01', repeat=6):
    decrypted = f.decrypt(ciphertext, ''.join(i))
    l = ''.join(decrypted)
    #fi.write(l+'\n')
    if simple_des.bin_to_ascii(l[-8:]) == '}':
        l = '010001'+l # fix the starting G  :D
        print(simple_des.bin_to_ascii(l))
    
#fi.close()    

