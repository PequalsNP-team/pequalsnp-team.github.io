---
layout: post
title: "Cheatsheet - Steganography 101"
category: cheatsheet
author: phosphore
---

## Steganography 101

First things first, always use [binwalk](https://github.com/devttys0/binwalk) or [foremost](http://foremost.sourceforge.net/) to isolate files from any other embedded stuff.

{% highlight console %}
      $ binwalk -e flag.png
	
	#Useful options
	-e, --extract                Automatically extract known file types
	-B, --signature              Scan target file(s) for common file signatures
	-E, --entropy                Calculate file entropy, use with -B (see the quickstart guide - https://goo.gl/JPKAIQ)
	-z, --carve                  Carve data from files, but don't execute extraction utilities
	-r, --rm                     Cleanup extracted / zero-size files after extraction
	-M, --matryoshka             Recursively scan extracted files
{% endhighlight %}

And of course use `strings` (ASCII, UTF8, UTF16) or `hexdump -C` on the file, before anything advanced.

* Check plaintext sections, comments (`cat`, `strings`)
* Use [exiftool](http://www.sno.phy.queensu.ca/~phil/exiftool/) for [EXIF](https://it.wikipedia.org/wiki/Exchangeable_image_file_format) data
* Use [TinEye](http://www.tineye.com/) to upload and search for the image. Select “best match” and hopefully you get the original image. [XORing](https://github.com/hellman/xortool) should do the rest of the job. Also use `compare a.png b.png result.png` from the ImageMagick suite, plenty of params available here.
* Use [pngcheck](http://www.libpng.org/pub/png/apps/pngcheck.html) for PNGs to check for any corruption or anomalous sections `pngcheck -v`  PNGs can contain a variety of data 'chunks' that are optional (non-critical) as far as rendering is concerned.
 * bKGD gives the default background color. It is intended for use when there is no better choice available, such as in standalone image viewers (but not web browsers; see below for more details)
 * cHRM gives the chromaticity coordinates of the display primaries and white point
 * gAMA specifies gamma
 * hIST can store the histogram, or total amount of each color in the image
 * iCCP is an ICC color profile
 * iTXt contains UTF-8 text, compressed or not, with an optional language tag. iTXt chunk with the keyword
 * pHYs holds the intended pixel size and/or aspect ratio of the image
 * sBIT (significant bits) indicates the color-accuracy of the source data
 * sPLT suggests a palette to use if the full range of colors is unavailable
 * sRGB indicates that the standard sRGB color space is used
 * sTER stereo-image indicator chunk for stereoscopic images
 * tEXt can store text that can be represented in ISO/IEC 8859-1, with one name=value pair for each chunk
 * tIME stores the time that the image was last changed
 * tRNS contains transparency information. For indexed images, it stores alpha channel values for one or more palette entries. For truecolor and grayscale images, it stores a single pixel value that is to be regarded as fully transparent
** zTXt contains compressed text with the same limits as tEXt


* If the image is relatively small check the palette (use `convert input.png output.xpm`). Be aware that sometimes colors are not preserved. In this case use the extra parameter.
* If there are large portions of the image that look the same colour check with a Bucket Fill (in gimp also remember to set the threshold to 0 when filling) for anything hidden, or play with the curves. Use [Grain extract](http://www.wikihow.com/Create-Hidden-Watermarks-in-GIMP) to check for watermarks.
* Use the [steganabara](http://www.freewebs.com/quangntenemy/steganabara/) tool and amplify the LSB of the image sequentially to check for anything hidden. Remember to zoom in and also look at the borders of the image. If similar colours get amplified radically different data may be hidden there.
* [Stegsolve](https://www.wechall.net/forum/show/thread/527/Stegsolve_1.3/page-1) (a simple jar `java -jar stegosolve.jar`) is also pretty useful to extract data (based on bitplanes) and analyze images, allowing you to go through dozens of color filters to try to uncover hidden text.

* Outguess
{% highlight console %}
      $ ./outguess [options] [<input file> [<output file>]]

	 #Useful options
	 -[kK] <key>  key
	 -[eE]        use error correcting encoding
	 -r           retrieve message from data
	 -m           mark pixels that have been modified
{% endhighlight %}

* [OpenStego](http://www.openstego.info/) is another GUI tool used for Random LSB.
* [StegHide](http://steghide.sourceforge.net/), to extract embedded data from stg.jpg: `steghide extract -sf stg.jpg`.
* [StegSpy](http://www.spy-hunter.com/stegspydownload.htm) will detect steganography and the program used to hide the message, checking for classical steganographical schemes.


## Scripts
* _(Python)_ Pixel color inverting example:
{% highlight python %}
import Image
if __name__ == '__main__':
	img = Image.open('input.png')
	in_pixels = list(img.getdata())
 	out_pixels = list()
 
	for i in range(len(in_pixels)):
		r = in_pixels[i][0]
		g = in_pixels[i][1]
		b = in_pixels[i][2]
		out_pixels.append( (255-r, 255-g, 255-b) )
 
	out_img = Image.new(img.mode, img.size)
	out_img.putdata(out_pixels)
	out_img.save("output_inverted.png", "PNG")
{% endhighlight %}

* _(Python)_ Change the palette (or colormap) of a PNG: [link to the script]({{ site.url }}/assets/change_palette.py) - [example of usage](https://github.com/ctfs/write-ups-2014/tree/master/plaid-ctf-2014/doge-stege) // [Ruby version](http://pastebin.com/46VmzrRU)

* _(PHP)_ If the image looks like it’s just a random noise we should make sure of it. We can, in fact, measure its randomness. Pixels of each color can appear in each place of the image with equal chance. If it’s false for some colors, we certainly want to look at them. [Here]({{ site.url }}/assets/detectrandomness.php) is a script for that, and the results appears below:
{% highlight console %}
$ php solve.php image.png
MAX disp: 1492.41; AVG: 92.82
GAP: 351.61 ± 200
DONE.
{% endhighlight %}

![Flag]({{ site.url }}/assets/beforeafterstegorandom.png){: .center-image }


## Audio Steganography
* Check the comments
* Load in any tool and check the frequency range and do a spectrum analysis.
* Use [sonic-visualiser](http://www.sonicvisualiser.org/) and look at the spectrogram for the entire file (both in log scale and linear scale) with a good color contrast scheme. See [this challenge]({{ site.url }}/writeups/its-hungry/) from the PoliCTF 2015 we solved with this method.

