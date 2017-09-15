#!/usr/bin/python
"""
f = open('sbox.txt', 'r')
FLAG = f.read()

enc = ''
for i in xrange(0, len(FLAG), 2):
    enc += '\'' + FLAG[i:i+2] + '\', '

ef = open('sbox_format.txt', 'w')
ef.write(enc)
ef.close()
"""

def invert(S):
    Si = [ [ 'x' for i in range(16) ] for j in range(16) ]
    for i in range(16):
        for j in range(16):
            cell = S[i][j]
            if cell != 'x':
                icell = int(cell[0],16)
                jcell = int(cell[1],16)
                Si[icell][jcell] = ('%x' % i) + ('%x' % j)
    return Si

def verify(S,Si):
    for i in range(16):
        for j in range(16):
            cell = S[i][j] 
            icell = int(cell[0],16)
            jcell = int(cell[1],16)
            if Si[icell][jcell] != ('%x' % i) + ('%x' % j):
                return False
    return True

def get_missing(Si):
    m = []
    for i in range(16):
        for j in range(16):
            cell = Si[i][j] 
            if cell == 'x':
                m.append(('%x' % i) + ('%x' % j))
    return m
    
def matrix_to_array(M):
    array = []
    for row in M:
        array.extend(row)
    return array

def normalize(S):
    S = matrix_to_array(S)
    S = [ int(i,16) for i in S ]
    return S

# Sbox from file
S = [['99', '95', '68', '62', '3a', '67', 'a1', '21', '66', '5a', '48', '0e', '2e', '45', '6e', '0c'],
     ['ad', '8e', 'fb', '4f', '6c', '25', '34', 'f1', '87', '97', 'd6', '7d', 'fe', '3c', 'ac', 'de'], 
     ['c0', 'e9', '10', '12', '74', 'c5', '44', 'c9', 'bf', '1a', 'e7', '17', '9e', '40', '1e', 'f5'],
     ['f4', 'd4', '5b', '86', '1c', '3d', '75', 'd9', 'df', 'be', '51', 'f2', 'd3', 'cb', 'd2', 'd1'], 
     ['16', '8a', 'ef', '41', 'd7', 'c7', '64', 'b8', 'e6', 'c4', '81', '30', 'aa', '0b', 'ed', 'a4'], 
     ['8b', '29', '7e', 'b4', 'b5', 'e3', 'c3', 'af', '1b', '09', '9b', 'bb', '0d', '72', '47', '6a'], 
     ['d0', '3f', '61', '19', '57', '60', '2b', '71', 'f6', '52', '6b', '43', 'd8', 'cf', '2a', '1d'],
     ['e0', 'dc', '2f', '83', '9c', 'a3', '82', '28', 'f0', '98', 'e8', 'e5', '22', 'ea', 'ae', '4c'], 
     ['77', 'ba', '93', '00', '49', '11', '63', '01', '79', 'fd', '80', 'e2', '13', '06', '8f', 'c8'], 
     ['f8', 'b6', '5c', '39', 'ee', '85', '54', '1f', 'ca', '9a', '03', 'ff', '96', '26', 'f3', '33'], 
     ['5d', '05', '37', '76', '5e', '08', '7a', 'eb', 'a7', 'cd', 'f9', '14', '94', 'f7', '4d', '4b'], 
     ['b7', '42', '6d', '36', 'b9', '8d', 'db', '20', '65', '56', '88', '9f', 'b0', 'a2', '18', 'a5'], 
     ['35', '0a', '78', '73', '7b', 'a6', 'fa', 'a9', '27', '4e', '7f', 'b3', '84', 'ce', 'fc', '4a'], 
     ['02', 'c1', 'e1', '53', '6f', 'd5', 'cc', '8c', '92', 'a0', '23', 'b2', 'ab', '07', '15', '58'], 
     ['2c', 'b1', 'da', '38', '24', 'dd', '55', '32', '90', '46', 'c2', 'bd', '91', '9d', 'e4', '3b'], 
     ['ec', '59', '50', '2d', '0f', '70', '7c', '5f']]
    
# Fill the empty spaces
S2 = [row[:] for row in S]
S2[-1].extend(['x','x','x','x','x','x','x','x'])

# Invert the SBox
Si = invert(S2)
         
# Get missing cells
missing = get_missing(Si)
#print(missing)
# missing = [0x04,0x31,0x3e,0x69,0x89,0xa8,0xbc,0xc6]

import itertools
pyaes = __import__('pyaes', globals(), locals(), [], -1)

# A 128 bit (16 byte) key
key = "9f24d4318b92a65f3537a02659b95340".decode('hex')
# 16 bytes
iv = "a072a5b0f4b715bf23b97b1cece817f2".decode('hex')
ciphertext = open('text.enc').read()

f = open('decrypted.txt', 'w')

count = 0
# Calculate all the missing permutation
for i in itertools.permutations(missing, 8):
    #print(count)
    count+=1
    
    Sp = [row[:] for row in S]
    Sp[-1].extend(list(i))
    Spi = invert(Sp)
    
    if count < 500:
        assert(verify(Sp,Spi)==True)
    
    ASp = normalize(Sp)    
    ASpi = normalize(Spi)   
    """
    if count == 1:
        print(ASp)
        print(ASpi)
        exit()
    """
    decryptor = pyaes.new(key, pyaes.MODE_CBC, IV=iv, Sbox=ASp, Sboxi=ASpi)
    decrypted = decryptor.decrypt(ciphertext)
        
    if 'SECT' in decrypted:
        print(decrypted)
        f.write(decrypted)
    
print("Finishing")
f.close()


