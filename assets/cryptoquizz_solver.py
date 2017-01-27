#!/usr/bin/env python3

from pwn import *

a1 = [
    {'n':'Daniel Bleichenbacher','y':1964}, 
    {'n':'Paulo Barreto','y':1965},
    {'n':'Antoine Joux','y':1967},
    {'n':'Ralph Merkle','y':1952},
    {'n':'Shafi Goldwasser','y':1958},
    {'n':'David Chaum','y':1955},
    {'n':'Ross Anderson','y':1956},
    {'n':'Ron Rivest','y':1947},
    {'n':'Ivan Damgard','y':1956},
    {'n':'Paul Kocher','y':1973},
    {'n':'Joan Daemen','y':1965},
    {'n':'Jean-Jacques Quisquater','y':1945},
    {'n':'Don Coppersmith','y':1950},
    {'n':'Bart Preneel','y':1963},
    {'n':'Lars Knudsen','y':1962},
    {'n':'Niels Ferguson ','y':1965},
    {'n':'Ronald Cramer','y':1968},
    {'n':'Ueli Maurer','y':1960},
    {'n':'Dan Boneh','y':1969},
    {'n':'Paul van Oorschot','y':1962},
    {'n':'Nigel P. Smart','y':1967},
    {'n':'Douglas Stinson','y':1956},
    {'n':'Bruce Schneier','y':1963},
    {'n':'Vincent Rijmen','y':1970},
    {'n':'Xuejia Lai','y':1954},
    {'n':'Rafail Ostrovsky','y':1963},
    {'n':'Jim Massey','y':1934},
    {'n':'Oded Goldreich','y':1957},
    {'n':'Yvo Desmedt','y':1956},
    {'n':'Neal Koblitz','y':1948},
    {'n':'Tatsuaki Okamoto','y':1952},
    {'n':'Shai Halevi','y':1966},
    {'n':'Claude Shannon','y':1916},
    {'n':'Victor S. Miller','y':1947},
    {'n':'Taher Elgamal','y':1955},
    {'n':'Jacques Patarin','y':1965},
    {'n':'David Naccache','y':1967},
    {'n':'Kaisa Nyberg','y':1948},
    {'n':'Phil Rogaway','y':1962}, # Phillip Rogaway
    {'n':'Mihir Bellare','y':1962},
    {'n':'Claus-Peter Schnorr','y':1943},
    {'n':'Alan Turing','y':1912},
    {'n':'Horst Feistel','y':1915},
    {'n':'Amit Sahai','y':1974},
    {'n':'Gilles Brassard','y':1955},
    {'n':'Amos Fiat','y':1956},
    {'n':'Silvio Micali','y':1954},
    {'n':'Donald Davies','y':1924},
    {'n':'Scott Vanstone','y':1947},
    {'n':'Michael O. Rabin','y':1931},
    {'n':'Eli Biham','y':1960},
    {'n':'Mitsuru Matsui','y':1961},
    
]

print(len(a1))

r = remote('quizz.teaser.insomnihack.ch', 1031)
r.recv()
#r.send("\n")

while True:
    q = r.recv()
    print("> " + q)

    for p in a1:
        if p['n'] in q:
            r.send(str(p['y']) + "\n")
            print(str(p['y']) + "\n")


'''
52
[+] Opening connection to quizz.teaser.insomnihack.ch on port 1031: Done
~~ What is the birth year of Horst Feistel ?
1915
~~ What is the birth year of Tatsuaki Okamoto ?
1952
~~ What is the birth year of Shafi Goldwasser ?
1958
~~ What is the birth year of Dan Boneh ?
1969
~~ What is the birth year of Ralph Merkle ?
1952
~~ What is the birth year of Lars Knudsen ?
1962
~~ What is the birth year of David Naccache ?
1967
~~ What is the birth year of Alan Turing ?
1912
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ OK, young hacker. You are now considered to be a                ~~
~~ INS{GENUINE_CRYPTOGRAPHER_BUT_NOT_YET_A_PROVEN_SKILLED_ONE}     ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''
