import urllib
import re

doi_pat = re.compile("doi:[^\"]+")

url = urllib.urlopen('http://bit.ly/wPf8Y5')
text = url.read()
print url.geturl()
outfile = open('html.txt','w')
outfile.write(text)
outfile.close()

#doi = doi_pat.search(text).group()
#print doi
print url.geturl()
