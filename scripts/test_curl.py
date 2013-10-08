import sys
import pycurl
import re

url_pat = re.compile("http://[^\"<>]+")

class Test:
    def __init__(self):
        self.contents = ''

    def body_callback(self, buf):
        self.contents = self.contents + buf


t = Test()
c = pycurl.Curl()
c.setopt(c.URL, 'http://bit.ly/wPf8Y5')
c.setopt(c.WRITEFUNCTION, t.body_callback)
c.perform()
c.close()

url = url_pat.search(t.contents)
print url.group()
