Unbrowser
========

Unbrowser is a small REST API that provides browser-based rendering of web pages. 
Initially, only a Webkit back-end is supported. Webkit support is provided by
[PhantomJS](http://www.phantomjs.org/).

Installation
------------

The easiest way to get up and running is to use [Vagrant](http://vagrantup.com/). A
Vagrantfile based on Ubuntu 10.04 is provided, as is a Puppet manifest.

Use
---

The only action provided at the moment is /webkit/rasterize/. This action requires a POST. The response will
be a redirect to the rendered output. Example:
   
    http://localhost:5000/webkit/rasterize/?url=http://www.google.com/

### Required parameters

* **url**

### Optional Parameters

* _width_
      
    default: 800

* _height_

    default: 600

* _format_
    
    default: png

* _render_delay_ (ms)
    
    default 10000