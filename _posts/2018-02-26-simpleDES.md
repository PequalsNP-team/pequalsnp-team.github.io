---
layout: post
title: "TAMU CTF 2018 - SimpleDES"
category: writeups
author: thezero
tags: tamu-2018 crypto
---

Crypto - 125 Points

Larry is working on an encryption algorithm based on DES.
He hasn't worked out all the kinks yet, but he thinks it works.
Your job is to confirm that you can decrypt a message, given the algorithm and parameters used.

The organizer gave us a specification about this simpleDES cipher:

```
    His system works as follows:
    - Choose a plaintext that is divisible into 12bit 'blocks'
    - Choose a key at least 8bits in length
    - For each block from i=0 while i<N perform the following operations
    - Repeat the following operations on block i, from r=0 while r<R
    - Divide the block into 2 6bit sections Lr,Rr
    - Using Rr, "expand" the value from 6bits to 8bits.
    Do this by remapping the values using their index, e.g.
    1 2 3 4 5 6 -> 1 2 4 3 4 3 5 6
    - XOR the result of this with 8bits of the Key beginning with Key[iR+r] and wrapping back to the beginning if necessary.
    - Divide the result into 2 4bit sections S1, S2
    - Calculate the 2 3bit values using the two "S boxes" below, using S1 and S2 as input respectively.

    S1  0   1   2   3   4   5   6   7
    0 101 010 001 110 011 100 111 000
    1 001 100 110 010 000 111 101 011

    S2  0   1   2   3   4   5   6   7
    0 100 000 110 101 111 001 011 010
    1 101 011 000 111 110 010 001 100

    - Concatenate the results of the S-boxes into 1 6bit value
    - XOR the result with Lr
    - Use Rr as Lr and your altered Rr (result of previous step) as Rr for any further computation on block i
    - increment r
```

The problem is the following:

```
He has encryped a message using Key="Mu", and R=2.
See if you can decipher it into plaintext.

Submit your result to Larry in the format Gigem{plaintext}.

Binary of ciphertext: 01100101 00100010 10001100 01011000 00010001 10000101
```

### Writeup

While we started reading the implementation for this cipher we noticed that it was based on a [Feistel network](https://en.wikipedia.org/wiki/Feistel_cipher)

A Feistel network is a scheme that let you construct a block cipher efficently since it requires only a round function (that can even be invertible) and itself it involves only XOR operation.

The decryption is pretty straightforward.  
Referring to the simpleDES implementation above:  
On step 3, for every block before starting the rounds iteration, swap L with R.  
Then at the end of the R rounds, swap L and R again.

You will also need to reverse the key schedule for round iteration.  
Let's assume you have 1 block and 3 rounds.

For the encryption you use the keys `K0`, `K1` and `K2`.
For the decryption you will need to use `K2`, `K1` and `K0`.

Why?  
Immagine you start from 1 block of plaintext. You split it into 2 blocks `L0` and `R0`.  
Now you use `K0` and `R0` on the round function `F`.  
This function will spit out "garbage" `Z` that you XOR it with `L0`.
You can now use the result as `R1` and use `R0` as `L1`.

For the decryption you only need to XOR the "garbage" `Z` again with `R1`

```
R1 = L0 ⊕ Z
R1 ⊕ Z = L0 ⊕ Z ⊕ Z = L0
```

So we [implemented it]({{ site.bloburl }}/assets/TAMU2018/simple_des.py) and [got the flag]({{ site.bloburl }}/assets/TAMU2018/feistel_decrypt.py)