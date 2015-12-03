---
layout: draft
title: "Cheatsheet - Socket Basics in Python NodeJS and Ruby"
category: cheatsheet
author: thezero
---

## Socket Basics in Python NodeJS and Ruby

### Python
{% highlight python %}
from socket import socket

sock = socket()
sock.connect(('1.2.3.4', 3333))
sock.send('Hello world!\n')
print "> " + sock.recv(1024)
sock.close()
{% endhighlight %}

### Ruby
{% highlight ruby %}
require 'socket'

a = TCPSocket.new('127.0.0.1', 3333)
a.write "Hello world!"
puts "> " + a.recv(1024)
a.close
{% endhighlight %}

### NodeJS
{% highlight js %}
var net = require('net');

var client = new net.Socket();
client.connect(3333, '127.0.0.1', function() {
    client.write('Hello world!');
});

client.on('data', function(data) {
    console.log('> ' + data);
    client.destroy();
});

client.on('close', function() {
    console.log('');
});
{% endhighlight %}
