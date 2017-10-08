klength = 32
llength = len("DCTF{}")+64+1
s = "65615f6962472d76142d1860006a5c4667024c3e2d7810770f79612b7309213c243d5b485c7612596d352742341f3c29456300701030187b127c145a230b53402d4839283d570c6d0826152a4936536a37562010001f061f67046c0a55384f69543d5b755826122b".decode('hex')
kn = "DCTF{"
modu = 126

key = "_"*klength

def decrypt(kn, cip, enc):
    k = (ord(kn) + ord(enc)) % modu - ord(cip)
    k = (modu-(k%modu))
    p = (ord(kn) + ord(enc) + k) % modu - ord(cip)
    return chr(k)
    
def replaceInPlace(s, s2, index):
    return s[:index] + s2 + s[index+len(s2):]

def decKey(kn, index=0, stop=klength):
    sol = ""
    count = len(kn)
    if stop-index < count:
        count = stop-index
    for i in range(0, count):
        if kn[i] != "_":
            sol += decrypt(kn[i], s[index+i+1], s[index+i])
        else:
            sol += "_"
    return replaceInPlace(key, sol, 0)

def decPlain(key):
    plain = ""
    for j in range(0, len(s)-1, klength):
        plain += decKey(key, j, len(s)-1)
        plain += "_"*(klength-len(key))
    return plain[:len(s)-1]

def mergeKey(plain, key):
    k2 = plain[llength:]
    for i in range(len(key)):
        if key[i] != '_':
            k2 = replaceInPlace(k2, key[i], i)
    return k2, plain[:llength]+k2
     
key = decKey(kn)
print(key)

plain = "_"
while '_' in plain:
    plain = decPlain(key)
    print(plain)
    key, plain = mergeKey(plain, key)
    #print(key)
    
