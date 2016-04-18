---
layout: draft
title: "Cheatsheet - Socket Basics for CTFs"
category: cheatsheet
author: thezero
---

## Socket Basics for CTFs

When playing CTFs, sometimes you may find a Challenge that runs on a Server,
and you must use sockets (or netcat `nc`) to connect.

I will show you some little snippet of code for deal with sockets in Challenge

### Python (or Sage)
{% highlight python %}
from socket import socket
from telnetlib import Telnet

sock = socket()
sock.connect(('1.2.3.4', 3333))
sock.send('Hello world!\n')
print "> " + sock.recv(1024)
#interactive mode
t = new Telnet()
t.sock = sock
t.interact()
sock.close()
{% endhighlight %}

### Python Pwntools
{% highlight python %}
from pwn import *

r = remote('1.2.3.4', 3333)
r.send("Hello world!\n")
print "> " + r.recv()
print r.recvuntil("END\n")
#interactive mode
r.interactive()
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
