---
layout: post
title: "DefCamp CTF 2017 - ForgotMyKey"
category: writeups
author: thezero
tags: defcampctf-2017 crypto
---

Crypto - 100 Points

[Challenge source code]({{ site.bloburl }}/assets/DefCamp2017/chall.php)

### Writeup

This challenge was pretty easy (a simple **chained modular addition**), but I want to share the script I wrote that *automagically* solve this type of challenge.  
*Note*: Modular addition behaves the same way as XOR operation, you know. `;)`

The `my_encrypt` function takes as input the `flag` and the `key`, hash the key with **md5** and then append the hash to the flag.
Finally the text is encrypted with the key hash.  
*Note:* the ciphertext is encoded in **little-endian** hex.

What is a **chained modular addition**?  
IDK either.

Anyway, it's a stream cipher that for each character adds together the current plaintext char, the previous ciphertext char and the current key char. All the additions are in modular arithmetic.

We took advantage of the `DCTF{}` flag format as plaintext, the **md5** and the flag (`DCTF{sha256(text)}`) length.  
With this knowledge we successfully retrived the key part by part with successive decryption.

You can see the solver script [here]({{ site.bloburl }}/assets/DefCamp2017/solve.py)

Those known parameters are easily tweakable in the solver script.

 - `klength` is the key length.
 - `llength` is the plaintext length excluding the key appended. (in this case was `DCTF{sha256}|`)
 - `s` is the ciphertext (big-endian hex encoded)
 - `kn` is the known part of the plaintext (in this case was `DCTF{`)
 - `modu` is the module of the addition (given in the source code)
 - `decrypt` function is totally separated from the solver logic, you can do whatever you want here

How the solver works?  
I(really)DK.

In the first step, it takes the known part of the plaintext and retrieves the related part of the key.  
In our case it was the starting piece of the flag format.  
*Note:* If you know another piece of plaintext, and not the starting part, you can tweak the solver script and pass to the `decKey` function the index from the start `:D`

Then the magic happens.  
The script constructs a fake plaintext made of `_`s, decrypts the ciphertext with the retrieved part of the key, and then takes from the end of the plaintext a different part of the key (since the key was appended!).  
Step after step the ciphertext is decrypted and the plaintext is revealed part by part resulting in a **magical** *auto-complete* **effect**.

![Flag]({{ site.url }}/assets/DefCamp2017/flag.png){: .center-image }

Abracadabra.  
`DCTF{0d940de38493d96dc6255cbb2c2ac7a2db1a7792c74859e95215caa6b57c69b2}`