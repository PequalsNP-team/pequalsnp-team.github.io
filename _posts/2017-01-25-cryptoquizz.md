---
layout: post
title: "InsomniHack Teaser CTF 2017 - cryptoquizz"
category: writeups
author: thezero
tags: insomnihack-teaser-2017 crypto
---

## randBox
Crypto - 120 Points

Hello, young hacker. Are you ready to fight rogue machines ? Now, you'll have to prove us that you are a genuine cryptographer.

Running on `quizz.teaser.insomnihack.ch:1031`


### Writeup
I've started connecting to the service with netcat

`nc quizz.teaser.insomnihack.ch 1031`

The server reply with this text:

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~ Hello, young hacker. Are you ready to fight rogue machines ?    ~~
    ~~ Now, you'll have to prove us that you are a genuine             ~~
    ~~ cryptographer.                                                  ~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~ What is the birth year of Ralph Merkle ?
    Connection closed by Host

Wow, this server have very very low timeout!

So I've searched up for Ralph Merkle birthyear (**1952**) and made a little script that open the connection
and reply with that printing the response. This was the output

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~ Hello, young hacker. Are you ready to fight rogue machines ?    ~~
    ~~ Now, you'll have to prove us that you are a genuine             ~~
    ~~ cryptographer.                                                  ~~
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ~~ What is the birth year of Alan Turing ?
	1952
    Connection closed by Host

Oh! The name is randomized so I can't reply directly with Merkle's birthyear.
So I have to read the question, check the date and reply.

I've wrote a script that open the connection read the question and store the cryptographer's name.
Once I had many cryptographers birthyears I've develop this script that reply accordingly.

**Here you can download the [cryptoquizz_solver.py]({{ site.url }}/assets/cryptoquizz_solver.py)**

And here the final session with the **52** stored cryptographers
{% highlight console %}
[+] Opening connection to quizz.teaser.insomnihack.ch on port 1031: Done
~~ What is the birth year of Horst Feistel ?
1915
~~ What is the birth year of Tatsuaki Okamoto ?
1952
~~ What is the birth year of Shafi Goldwasser ?
1958
~~ What is the birth year of Dan Boneh ?
1969
~~ What is the birth year of Ralph Merkle ?
1952
~~ What is the birth year of Lars Knudsen ?
1962
~~ What is the birth year of David Naccache ?
1967
~~ What is the birth year of Alan Turing ?
1912
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~ OK, young hacker. You are now considered to be a                ~~
~~ INS{GENUINE_CRYPTOGRAPHER_BUT_NOT_YET_A_PROVEN_SKILLED_ONE}     ~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
{% endhighlight %}
