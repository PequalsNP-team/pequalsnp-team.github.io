---
layout: post
title: "sCTF Q1 2016 - Control Panel"
category: writeups
author: phosphore
tags: web sctf-2016
---

## Control Panel
Web - 40 Points

Take control... of the flag on this admin control panel.

### Writeup
We have a website which let you register with a username and a password. Wandering in the code we found this interesting hint, written as html comment:

![The html comment]({{ site.url }}/assets/control-panel1.png){: .center-image }

to read the flag you need admin rights, which you don't have if you register as a normal user. We needed a privilege escalation vulnerability, or something similar.
Maybe just setting `admin=true` in the registration request will do the trick?

![cURL]({{ site.url }}/assets/control-panel2.png){: .center-image }

Yes, it did.


![The flag]({{ site.url }}/assets/control-panel3.png){: .center-image }

