---
layout: post
title: "TAMU CTF 2018 - LarryCrypt"
category: writeups
author: thezero
tags: tamu-2018 crypto
---

Reverse - 200 Points

A binary executable called `larrycrypt` were provided.

`./larrycrypt -R 4 -K "V3c70R" flag`


### Writeup

We tried some input for the `larrycrypt` binary and we noticed that it was always using `Mu` as key, no matter what was the `-K` parameter.  
It was likely some bug, but then the [SimpleDES challenge]({{site.url}}/writeups/simpleDES) we just solved came to our minds.

The binary was using the same key as the other challenge's example.  
So we thought it was using the same algorithm maybe but it wasn't the case.

Larrycrypt was using 6bit blocks for the ciphertext.  
The first block of ciphertext was the same as SimpleDES first 6bit of cyphertext when using the same key and the same number of rounds.  
With some more reverse engineering we figured out that larrycrypt was taking the first 12 bits of plaintext, splitting it into `L0` and `R0`, performing the round function and printing only the resulting `L1`.  
So they were using the same round function.

But then the sequence changes, We take the `R` output from the round function and use it as `L` for the next round along with the next block of ciphertext.

This image shows an example on 3 blocks of data, the output cypertext is made of `cypher0`, `cypher1`. `L2` won't be printed.
![larrycrypt scheme]({{site.url}}/assets/TAMU2018/larryscheme.png){: .center-image }

To decrypt this we need to bruteforce all the possible 6bit last blocks (`L2` in the image), decrypt all the blocks and check if the plaintext is good.

We used our previous implementation of the [SimpleDES round function]({{ site.bloburl }}/assets/TAMU2018/simple_des.py) and [bruteforce the plaintext]({{ site.bloburl }}/assets/TAMU2018/larrycrypt.py) with python
