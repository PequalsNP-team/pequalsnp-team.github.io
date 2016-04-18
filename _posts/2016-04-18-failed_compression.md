---
layout: post
title: "sCTF Q1 2016 - Failed Compression"
category: writeups
author: thezero
tags: forensics sctf-2016
---

## Failed Compression
Forensics - 80 Points

I was trying to compress some files, but I think I messed it up?

 [compressed.zip]({{ site.url }}/assets/compressed.zip)

### Writeup
When you try to open the ZIP file, every ZIP programs tells you that it's not a valid archive file.
With an HexEditor we can see that it's not a ZIP file because it don't have known [Magic Byte](https://en.wikipedia.org/wiki/Magic_number_%28programming%29)

{% highlight console %}
$ file compressed.zip
compressed.zip: data
{% endhighlight %}

Also I noticed that there were lot of PNG/IHDR signature and JPG/JFIF signature.
So I excluded the `APNG` option and thought that maybe the archive was a concatenation
of PNG and JPG files.
Unfortunately every file's header was changed so we extraced with Binwalk the
start position and end position of every PNG file (based on IHDRpos -12byte and IENDpos +5byte)
and JPEG file (based on JFIFpos -6byte and `0xFF 0xD9`)

So I wrote a script to extract with `dd` every single image fixing the Magic Byte (loaded from a file).

{% highlight python %}
#!/usr/bin/env python

import sys
import os
import subprocess

def our_dd(i,e,ff):
	  print i," ",e
	  n = "src/immagine"+str(i)
	  h = subprocess.check_output("dd if=compressed.zip of="+n+"1."+ff+" bs=1 skip="+str(i)+" count="+str(e-i), shell=True)
	  print h
	  h = subprocess.check_output("cat "+ff+"_magic "+n+"1."+ff+" > "+n+"."+ff+"; rm "+n+"1."+ff, shell=True)
	  print h


with open("JFIFpos.txt") as f:
	  jfifpos = f.read().splitlines()
with open("EOFJFIFpos.txt") as f:
	  eofjfifpos = f.read().splitlines()

c=0
for line in jfifpos:
	  while True:
		    start = int(line)-2
		    end = int(eofjfifpos[c])+2
		    if end-start > 0:
			      our_dd(start,end,"jpg")
			      break
		    c+=1

with open("IHDRpos.txt") as f:
	  ihdrpos = f.read().splitlines()
with open("IENDpos.txt") as f:
	  iendpos = f.read().splitlines()

c=0
for line in ihdrpos:
	  our_dd(int(line)-8,int(iendpos[c])+5+3,"png")
	  c+=1
{% endhighlight %}

![Meme]({{ site.url }}/assets/immagine1848790.jpg){: .center-image }

And finally I found a flag, in the sea of memes
![Flag]({{ site.url }}/assets/flag.jpg){: .center-image }
