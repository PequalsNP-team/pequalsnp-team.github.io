---
layout: post
title: "PoliCTF 2015 - It's Hungry"
category: writeups
author: phosphore
tags: forensics polictf-2015
---

## It's Hungry
Forensics - 100 Points

Old McDonald had a farm. Old McDonald liked chiptune. He also needed to remind its daughter to take care about a zombie animal. But he wanted to do it discreetly, so he wrote this song. Can you find the message? (all lowercase, no spaces) N.B. flag is not in format flag{.+}

Hidden/Special Challenge!

### Writeup
This one was a hidden challenge available clicking on the timestamp of the chiptune player.

     phosphore:~$ wget http://polictf.it/tunes/oldmcdonald.flac

We started by inspecting the sources of the player but we found nothing. So we focused on the audio file `oldmcdonald.flac`.  

<br/>
Again, using [metaflac](http://linux.die.net/man/1/metaflac), a command-line FLAC metadata editor: no results. <br/>
Being aware of several ways to hide messages in audio files we tried to extract text by LSB-based audio steganography. Failing.  <br/>
That's when we opened up the spectogram of the song with [sonic-visualizer](www.sonicvisualiser.org)...  

![The spectogram]({{ site.url }}/assets/mcdonald-spectrum1.jpg){: .center-image }

then, around 1:08 at ≃ 18'600Hz, we run into this:

![The morse code]({{ site.url }}/assets/mcdonald-spectrum2.jpg){: .center-image }

Cleary morse! After a few tries this happened.

![The morse message]({{ site.url }}/assets/mcdonald-morse.jpg){: .center-image }

![The trollface]({{ site.url }}/assets/mcdonald-trollface.jpg){: .center-image }

Yes, we were frustrated, so we vented on ocean :(

![The trollface]({{ site.url }}/assets/mcdonald-irc.jpg){: .center-image }

"just listen" said the hint. We figured that we were supposed to listen to the chiptune. At the end we tried writing the notes down and we came up with `f e d a d e a d b d e`, which made no sense.<br/>
Alas, turns out we got the notes wrong and they turned out to be `f e e d d a d e a d b e e f`, our flag.

![Chiptune notes]({{ site.url }}/assets/mcdonald-notes.jpg){: .center-image }

:(



