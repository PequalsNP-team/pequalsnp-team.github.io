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
This one was a hidden challenge available clicking on the timestamp of the chiptune player. We started by inspecting the sources of the player but we found nothing. So we focused on the audio file "oldmcdonald.flac".
Again, using metaflac, a command-line FLAC metadata editor: no results. 
Being aware of several ways to hide messages in audio files we tried to extract text by LSB-based audio steganography. Failing.  
That's when we opened up the spectogram of the song with sonic-visualizer...  

![The spectogram]({{ site.url }}/assets/mcdonald-spectrum1.png)

then, around 1:08 at ≃ 18'600Hz, we run into this:

![The morse code]({{ site.url }}/assets/mcdonald-spectrum1.png)

Cleary morse! After a few tries this happened.

![The morse message]({{ site.url }}/assets/mcdonald-morse.png)

![The trollface]({{ site.url }}/assets/mcdonald-trollface.png)

Yes, we were frustrated, so we vented on ocean :(

![The trollface]({{ site.url }}/assets/mcdonald-irc.png)

"just listen" said the hint. We figured that we were supposed to listen to the chiptune. At the end we tried writing the notes down and we came up with {% highlight console %}F E D A D E A D B D E{% endhighlight %}, which made no sense.
Alas, turns out we got the notes wrong and they turned out to be {% highlight console %}F E E D D A D E A D{% endhighlight %}, our flag.

![Chiptune notes]({{ site.url }}/assets/mcdonald-notes.png)

:(



