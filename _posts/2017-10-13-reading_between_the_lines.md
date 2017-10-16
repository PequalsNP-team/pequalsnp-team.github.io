---
layout: post
title: "Square CTF 2017 - Reading between the lines"
category: writeups
author: thezero
tags: squarectf-2017 crypto
---

Forensics - 100 Points

Find the secret in the archive

Evil Robot Corp accidently made their S3 bucket public and we were able to grab this backup archive before we were kicked out. We think there might be a secret in here, but we can't find it. Can you help us?

### Writeup

I really enjoyed this Forensics challenge.

You start with a `zip` archive.  
If you open it you can extract 3 `jpg` files with photos of cats.  

Time to study the PKZIP format!

([This](https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip.html) is a nice start)  

![ZIP64](https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/ZIP-64_Internal_Layout.svg/400px-ZIP-64_Internal_Layout.svg.png){: .center-image }

A ZIP file is made of several entries, compressed and concatenated together.  
Each entry is preceded by a **local header** and *can be* followed by a **data descriptor**.  

At the end of the ZIP file we have the **central directory** that contains the references to each entry in the file.  

By opening our zip file with an Hex editor we noticed that there were 4 `PK\x04\x05` signatures.  
Those bytes are the **local header** signature, so we actually have 4 entries in the zip file.

Then we looked at the **central directory** entries (signature `PK\x01\x02`) but only 3 are listed here.

MUAHAHAHAHAH.

Ok easy, we only need to add the missing entry to the central directory.

This is the central entry header  
![central file header](https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip-images/central-file-header.png){: .center-image }

We need to fill all these fields for the missing entry.  
We can get them from the local entry header

![local file header](https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip-images/local-file-header.png){: .center-image }

But...

Compressed and uncompressed sizes are zero-ed in the local file header 😢

Don't you worry, don't you worry child...

In this zip archive the data descriptor flag is set for every entry so the compressed and uncompressed sizes are at the end of each entry.

![local file header](https://users.cs.jmu.edu/buchhofp/forensics/formats/pkzip-images/data-descriptor.png){: .center-image }

We fixed the zip file and retrieved the flag.

--- 

**BONUS**

Since I love automation and working with hex editors is the farther thing from it,  
I've decided to create a [script](https://github.com/TheZ3ro/zipfix) to extract zip entries that are not present in the central directory.  

The script was first written by **ejrh**, I've added data descriptor support to make it work for this challenge :)

You can read [here](https://ejrh.wordpress.com/2012/05/15/fixing-a-zip-file/) how the script works 