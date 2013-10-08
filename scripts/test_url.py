import re
import urllib2

def get_hyperlinks(source): 

   urlPat = re.compile(r'<a [^<>]*?href=("|\')http:\/\/([^<>"\']*?)("|\')')

   result = re.findall(urlPat, source)

   urlList = []

   for item in result:
       link = item[1]
       urlList.append('http://' + link)
##     if link.startswith("http://") and link.startswith(url):
##         if link not in urlList:
##             urlList.append(link)
##     elif link.startswith("/"):
##         link = url + link
##         if link not in urlList:
##             urlList.append(link)
##     else:
##         link = url + "/" + link
##         if link not in urlList:
##             urlList.append(link)
 
   return urlList

print "Enter the URL: "
url = raw_input("> ")
usock = urllib2.urlopen(url)
data = usock.read()
usock.close()
urlList = get_hyperlinks(data)
for url in urlList:
    if 'pnas' in url:
        print url
