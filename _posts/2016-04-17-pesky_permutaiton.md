---
layout: post
title: "sCTF Q1 2016 - Pesky Permutation"
category: writeups
author: thezero
tags: algorithmic sctf-2016
---

## Pesky Permutations
Algorithmic - 170 Points

One of my favorite pastimes is solving my Rubik's Cube. In fact, I've fiddled with it so much that I noticed a pattern: If you repeat the same algorithm on the cube, it will eventually return to its original state.

Can you give me the average number of permutations each algorithm in [perms.dat]({{ site.url }}/assets/perms.dat) takes to return the cube to solved? Round your answer to 2 decimal places and submit without sctf{}.

Good Luck!

### Writeup
I decided to use the Python library PyCuber to solve this challenge and apply every line of moves on a Cube
checking every time if it was solved.

This is the script I wrote

{% highlight python %}
#!/usr/bin/env python

import sys
import os
import pycuber as pc

c_sum = 0
solved = pc.Cube()
cubes = 0

with open("perms.dat") as f:
   content = f.read().splitlines()

for form in content:
   c = pc.Cube()
   alg = pc.Formula(form)
   cubes += 1

   c(alg)
   counter = 1
   while c!=solved:
      c(alg)
      counter+=1
   print(str(cubes)+" -> "+str(counter))
   c_sum += counter

print(c_sum/float(cubes))
{% endhighlight %}

After a lot of time and Distributed Computing, we came up with the following sum (rounded):

`140.13`

This is the file with line numbers and moves numbers if you want to check:
[perm.txt]({{ site.url }}/assets/perm.txt)
