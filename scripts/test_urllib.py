import urllib
import re

doi_pat = re.compile("doi:[^\"]+")

url = urllib.urlopen('http://j.mp/HiggsParticle')
text = url.read()
doi = doi_pat.search(text).group()
print doi
print url.geturl()
outfile = open('html.txt','w')
outfile.write(text)
outfile.close()
