---
layout: post
title: "PoliCTF 2015 - John the Traveller"
category: writeups
author: phosphore
tags: web polictf-2015
---

## John The Traveller
Web - 100 Points

Holidays are here! But John still hasn't decided where to spend them and time is running out: flights are overbooked and prices are rising every second. Fortunately, John just discovered a website where he can book last second flight to all the European capitals; however, there's no time to waste, so he just grabs his suitcase and thanks to his new smartphone he looks the city of his choice up while rushing to the airport. There he goes! Flight is booked so... hauskaa lomaa!<br/>
`traveller.polictf.it`

### Writeup

    hauskaa lomaa!

Extremely suspicious. Our friend, Google Translate, found the greet to be finnish (happy vacation!). Let's keep in mind this for later.  
In this 'Last second flights' website you were able to search for some of the european capitals flights. Nothing strange so far.
We tried to set John's destination to 'Helsinki' and we noticed that the prices that previously were in 'EUR' now were in 'px'.  
Inspecting the page we found that just in this particular page there were some class attributes of the table rows, named progressively as w + tr number + 2 characters (e.i. w00vh, w01fc ... w20XJ, w21Kj) .
We tried to concatenate the last 2 characters hoping to find a valid hash but with no success.  
At the end we read again the challenge description: we forgot that John... 

    thanks to his new smartphone he looks the city of his choice up while rushing to the airport
  
was on his smartphone! That's the reason behind this 'px' currency. So we opened up the developer tool, emulated the viewport of a Nexus 5 and tried the width sizes in px. Then, a QR code with our flag popped out!

     flag{run_to_the_hills_run_for_your_life}

![Our QR code]({{ site.url }}/assets/johnthetraveller-QR.jpg){: .center-image }

