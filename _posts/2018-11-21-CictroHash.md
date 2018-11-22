---
layout: post
title: "RITSEC CTF 2018 - CictroHash"
category: writeups
author: thezero
tags: ritsec-2018 crypto
---

Crypto - 150 Points

See the [attached PDF]({{site.bloburl}}/assets/RITSEC2018/CictroHash.pdf) for an amazing new Cryptographic Hash Function called CictroHash.  
For this challenge you must implement the described Hash Function and then find a collision of two strings.  
Once a collision is found send both strings to fun.ritsec.club:8003 as a HTTP POST request like below:

```
curl -X POST http://fun.ritsec.club:8003/checkCollision \
--header "Content-Type: application/json" \
--data '{"str1": "{{INSERT_STR1}}", "str2": "{{INSERT_STR2}}"}'
```
If the strings are a valid collision then the flag will be returned.

NOTE: requests to this server are being rate-limited for obvious reasons.

Author: Cictrone

### Writeup

This crypto challenge was really original and very interesting.

We started writing the implementation for the CictroHash sponge function, after some ranting for the incomplete specification and the incorrect text vector.  
Then we based our output on the hashes returned by the server.

Once our implementation was exact, we noticed that the permutation function only acted on some bits and didn't provide enough [diffusion](https://en.wikipedia.org/wiki/Confusion_and_diffusion) so the [avalanche effect](https://en.wikipedia.org/wiki/Avalanche_effect) was minimum in some cases.

For example you can see how "HELLOWORLD" and "HELLOWORLD0" only differs by 2 bit in the 3rd byte
```
>>> CictroHash.hash("HELLOWORLD")
"91f1c05e"
>>> CictroHash.hash("HELLOWORLD0")
"91f1005e"
>>>
>>> '{:08b}'.format(0x00)
'00000000'
>>> '{:08b}'.format(0xc0)
'11000000'
```

So we tried to bitflip one bit at a time the pre-image searching for a collision and finally we found one:

```
91f1405e - HENLOWORLD - HELLOWGRLD
```

Here it is our implementation [CictroHash.py]({{site.bloburl}}/assets/RITSEC2018/cictrohash.py)