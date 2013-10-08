#!/usr/bin/python
# coding: utf-8
###########################################################################################    This module is used to expand all urls using curl###############################################################################################
import sys
import pycurl
import re
import urllib2, urllib
import urlparse
import httplib
import socket

socket.setdefaulttimeout(15)


url_pat = re.compile("http://[^\"<>]+")

class URL:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf
class URLExpander:
  # known shortening services
  shorteners = ['tr.im','is.gd','tinyurl.com','bit.ly','snipurl.com','cli.gs',
                'feedproxy.google.com','feeds.arstechnica.com','ow.ly','t.co','fb.me','goo.gl']
  twofers = [u'\u272Adf.ws']
  # learned hosts
  learned = []
    
  def resolve(self, url, components):
    """ Try to resolve a single URL """
    c = httplib.HTTPConnection(components.netloc)
    c.request("GET", components.path)
    r = c.getresponse()
    l = r.getheader('Location')
    if l == None:
      return url # it might be impossible to resolve, so best leave it as is
    else:
      return l
  
  def query(self, url, recurse = True):
    """ Resolve a URL """
    components = urlparse.urlparse(url)
    # Check weird shortening services first
    if (components.netloc in self.twofers) and recurse:
      return self.query(self.resolve(url, components), False)
    # Check known shortening services first
    if components.netloc in self.shorteners:
      return self.resolve(url, components)
    # If we haven't seen this host before, ping it, just in case
    if components.netloc not in self.learned:
      ping = self.resolve(url, components)
      if ping != url:
        self.shorteners.append(components.netloc)
        self.learned.append(components.netloc)
        return ping
    # The original URL was OK
    return url

def curl_expand_url(url):
    """expand a short url using curl"""
    u = URL()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEFUNCTION, u.body_callback)
    c.perform()
    c.close()
    match = url_pat.search(u.contents)
    if match != None:
	long_url = match.group()
    else:
	long_url = ''
    return long_url

def httplib_expand_url(url):
    """expand a short url using httplib"""
    try:
        expander = URLExpander()
        long_url = expander.query(url)
    except:
	long_url = ''
    return long_url

def urllib_expand_url(url):
    """expand url using urllib2"""
    try:
        html = urllib2.urlopen(url)
        #text = html.read()
        org_url = html.geturl()
    except:
	org_url = ''
    return org_url

def test():
    url = "http://www.pnas.org/content/110/6/2070"
    print urllib_expand_url(url)
    print httplib_expand_url(url)
    #print curl_expand_url(url)

#test()
 
