---
layout: post
title: "CodeBlue CTF 2017 - Common Modulus 1,2,3"
category: writeups
author: thezero
tags: codebluectf-2017 crypto
---

<script type="text/javascript" async
  src="https://cdn.rawgit.com/mathjax/MathJax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML">
</script>
<script type="text/x-mathjax-config">
MathJax.Hub.Config({
  TeX: { equationNumbers: { autoNumber: "AMS" } },
  tex2jax: {
    inlineMath: [['$','$'], ['\\(','\\)']],
    processEscapes: true
  }
});
</script>

Crypto - 100 Points

Common Modulus 1: Simple Common Modulus Attack  
Common Modulus 2: Common Modulus Attack with common exponent divisor  
Common Modulus 3: Common Modulus Attack with common exponent divisor + message padding  

### Writeup

The challenge title was pretty self explanatory.

textbook RSA is vulnerable to [Common Modulus Attack](https://crypto.stackexchange.com/a/16285).

RSA works like the following $c = m^e \mod N$

If you encrypt the same message with the same $N$ like:  
$C_1 = M^{e_1} \mod N$  
$C_2 = M^{e_2} \mod N$  

Then $\gcd(e_1, e_2)=d$, this means that $a$ and $b$ exists such that $e_1a + e_2b=d$.

This is usefull since:
$$
\begin{align}
C_1^{a}*C_2^{b}&=(M^{e_1})^{a}*(M^{e_2})^{b}\\
&=M^{e_1a}*M^{e_2b}\\
&=M^{e_1a+e_2b}\\
&=M^d
\end{align}
$$


In the case where $e_1$ and $e_2$ don't share any factor, $\gcd(e_1, e_2)=1$ so $M^d = M^1 = M$.  
In the case where $e_1$ and $e_2$ share some factors, we end up with $M^d$.

Common Modulus 1 was the first easy case.

In Common Modulus 2 both the exponents were multiplied by $3$, so $d=3$ then $M^d=M^3$  
Luckily our $M^3$ is smaller than our $N$ so we can retrive the flag by applying the cube-root.

In Common Modulus 3, the greatest common divisor is $17$ and unfortunately $M^{17}>N$.  
We need to remove the padding from $M$ until $M^{17}<N$ then take the 17th-root as before.

The message/flag is padded with the following code:
```python
flag = key.FLAG.encode('hex')

while len(flag) * 4 < 8192:
  flag += '00'

FLAG = long(flag[:-2], 16)
```

`len(FLAG)` should be `2046`, the previous flags were `CBCTF{<32_char_here>}`  so converted in hex we have `len(flag) = 78`.

$2046-78=1968$

Adding `00` to an hex number it's the same as multiplying by $2^4$,  
so we need to multiply the padded $M$ by $2^{-4}$ to remove all the `00`

Let $d=17$ and $i=1968$, retrive $M$ with

$$
\begin{align}
M''&=C_1^{a}*C_2^{b}\\
M'&=M''*2^{-d*4*i}\\
M&=\sqrt[d]{M'}\qquad
\end{align}
$$

The complete python script is available [here]({{ site.bloburl }}/assets/CodeBlue2017/common_modulus.py)

```
CBCTF{6ac2afd2fc108894db8ab21d1e30d3f3}
CBCTF{d65718235c137a94264f16d3a51fefa1}
CBCTF{b5c96e00cb90d11ec6eccdc58ef0272d}
```