---
layout: post
title: "InsomniHack Teaser CTF 2016 - Bring The Noise"
category: writeups
author: thezero
tags: crypto insomnihack-teaser-2015
---

## Bring The Noise
Crypto - 200 Points

realized by veorq

Quantum computers won't help you

[Source](https://github.com/ctfs/write-ups-2016/blob/master/insomnihack-teaser-2016/crypto/bring-the-noise-200/server-bd6a6586808ab28325de37276aa99357.py)<br/>
Running on: bringthenoise.insomnihack.ch:1111

### Writeup
Reading the Source we see that the program is made up of 2 problems.

 - A Proof-of-Work with the pre-image of 5 characters of MD5 ([From line 35 to 41](https://github.com/ctfs/write-ups-2016/blob/master/insomnihack-teaser-2016/crypto/bring-the-noise-200/server-bd6a6586808ab28325de37276aa99357.py#L35-L41))
 - A problem of linear equations with mod q ([The `learn_with_vibration` function, From line 17 to 27](https://github.com/ctfs/write-ups-2016/blob/master/insomnihack-teaser-2016/crypto/bring-the-noise-200/server-bd6a6586808ab28325de37276aa99357.py#L17-L27))

We solved the 2 problems separately.

----------

Connecting on the server return the PoW challenge:
```sh
> nc bringthenoise.insomnihack.ch 1111
# Challenge = 8268c
```

We write a simple script based on [TheZ3ro/combinator](https://github.com/TheZ3ro/combinator)

```js
var crypto = require('crypto');
var bruteForce = require("jscombinator").comb;
var dict = require("jscombinator").dict;

var hash = "8268c"; // The connection returned this hash

bruteForce(dict.lower_alpha_numeric, Array.range(1,8), function(value){
  var string = value;
  var cry = crypto.createHash("md5").update(string).digest("hex");
  console.log(cry+" "+value);
  if( cry.indexOf(hash) == 0 ) {
    console.log("Correct value of the hash was: " + value);
    return true;
  }
  return false;
});
```

![Combinator]({{ site.url }}/assets/combinator.png){: .center-image }

----------

After completing the PoW, the script print out the 40 equations.

But we previously had reversed the source script to take the 40 equations as input and bruteforce vibration to find the solution

You can download and read the reversed script here:
[anacleto.py]({{ site.url }}/assets/anacleto.py)

And our 40 equations:
[anacleto.txt]({{ site.url }}/assets/anacleto.txt)

This was our solution<br/>
![Vibration]({{ site.url }}/assets/vibration.png){: .center-image }

And a wild flag appeared!

`INS{ErrorsOccurMistakesAreMade}`
