---
layout: post
title: "sCTF Q1 2016 - Verticode"
category: writeups
author: thezero
tags: cryptography sctf-2016
---

## Verticode
Cryptography - 90 Points

Welcome to Verticode, the new method of translating text into vertical codes.

Each verticode has two parts: the color shift and the code.

The code takes the inputted character and translates it into an ASCII code, and then into binary, then puts that into an image in which each black pixel represents a `1` and each white pixel represents a `0`.

For example, A is 65 which is `1000001` in binary, B is 66 which is `1000010`, and C is 67 which is `1000011`, so the corresponding verticode would look like this.
![VertiA]({{ site.url }}/assets/A-code.png){: .center-image }

Except, it isn't that simple.

A color shift is also integrated, which means that the color before each verticode shifts the ASCII code, by adding the number that the color corresponds to, before translating it into binary. In that case, the previous verticode could also look like this.

The table for the color codes is:
```
0 = Red, 1 = Purple, 2 = Blue, 3 = Green, 4 = Yellow, 5 = Orange
```

This means that a red color shift for the letter A, which is 65 + 0 = 65, would translate into 1000001 in binary; however, a green color shift for the letter A, which is 65 + 3 = 68, would translate into 1000100 in binary.
![VertiB]({{ site.url }}/assets/B-code.png){: .center-image }

[Given this verticode]({{ site.url }}/assets/code1.png), read the verticode into text and find the flag.

**Note** that the flag will not be in the typical `sctf{flag}` format, but will be painfully obvious text. Once you find this text, you will submit it in the `sctf{text}` format. So, if the text you find is `adunnaisawesome`, you will submit it as `sctf{adunnaisawesome}``

### Writeup
I started analyzing the problem step by step.

I wrote a script that can read Black/White Verticode from file.<br/>
After that I've added the colors shifts and finally I've glued all together.

The `parse_bin` and `parse_color` function detect Black/White and Colors Shifts.<br/>
In the main cicle the script read the image pixel per pixel (scaled by m=12, because a "block" is 12x12 pixels).<br/>
If we are in the first 7 pixel, detect the Color Shift. Otherwise read the "word" in `data`.<br/>
When it finish reading the current line apply the color shift to `data` char and append to `key`.

{% highlight python %}
#!/usr/bin/env python

import os, sys
import Image

def parse_bin(r,g,b):
	 if r+g+b == 0:
		 return 1
	 else:
	 	return 0 # white is the new black 0

def parse_color(r,g,b):
 	if r == 255 and g == 0 and b == 0: #Red
 		return 0
 	if r == 128 and g == 0 and b == 128: #Purple
 	  return 1
 	if r == 0 and g == 0 and b == 255: #Blue
 		return 2
 	if r == 0 and g == 128 and b == 0: #Green
 		return 3
 	if r == 255 and g == 255 and b == 0: #Yellow
 		return 4
 	if r == 255 and g == 165 and b == 0: #Orange
		 return 5

def main():
	 im = Image.open("code1.png")
	 pix = im.load()
	 m = 12
 	data = ""
 	key = ""
 	for i in xrange(im.size[1]/m): # Row
	 	color = 0
	 	for j in xrange(im.size[0]/m): # Col
	 		if j == 0:
	 			r,g,b = pix[0,i*m]
	 			color = parse_color(r,g,b)
 			if j>=7:			
 				r,g,b = pix[j*m,i*m]
	 			data += str(parse_bin(r,g,b))
 			if j==13:
 				key += chr(int(data, 2)-color)
	 			data = ""
	 print "\n"+key
	 return 0

if __name__ == '__main__':
 	main()
{% endhighlight %}

This will print out a nice story about a man named *Joe Lopo*.<br/>
And suddently...

`iamtheflagalllowercasenojoke`
