---
layout: post
title: "PoliCTF 2015 - Hard Interview"
category: writeups
author: thezero
tags: grabbag polictf-2015
---

## Hard Interview
GrabBag - 50 Points

`interview.polictf.it:80`

### Writeup

This one was pretty funny...for those who have watched the film Swordfish. (not like us)


     fish@sword:~$ cd ./
      cd: command not found
     fish@sword:~$ help
     A very hard interview: Codename Blow...Fish
     Maybe you can help me with something...
     DOD d-base, 128 bit encryption....What do you think?
     Maybe slide in a Trojan horse hiding a worm...
     I have been told that best "crackers" in the world can do it 60 minutes, unfortunately i need someone who can do it in 60 seconds... naturally with the right incentives ;)
     If you know what I mean, tell me how a real cracker accesses to a remote super protected server...

     Possible commands:
     	  hacker: Write code as a real hacker
     	    help: Give informations about the program
     	    hint: Gives a little hint
     	    exit: Loser...bye Bye
     	     ssh: A tiny ssh command
     	    date: A very useful and innovative feature

We checked the hint and the hacker command (just for fun)

     fish@sword:~$ hint
      usage:  ssh username@address
      username: THE username
      address: a not so easily reachable IP address
      Very simple...isn't it?

So we must connect with ssh to a **not so easily reachable IP address**<br/>
We tried

     fish@sword:~$ ssh root@127.0.0.1
      … Username not found
      … Address not reachable

Nothing.
After some hours and some other challenge we searched on google
the "help" quote and the "fish@sword" hosts...<br/>

We got the Swordfish film then.<br/>
Watched the hacking scene [on youtube](https://www.youtube.com/watch?v=zfy5dFhw3ik)

![IP]({{ site.url }}/assets/ipadd.png){: .center-image }
![User]({{ site.url }}/assets/user.png){: .center-image }

Oh, now we got what they mean with **not so easily reachable IP address**<br/>

     fish@sword:~$ ssh admin@312.5.125.233
      flag{H4ll3_B3rry's_t0pl3ss_sc3n3_w4s_4ls0_n0t4bl3}
