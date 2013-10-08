##################################################################################################Fetch the web page contect and target the ##################################### id or doi information from the webpage#######################################################################################################
####import libraries
import sys
import os
import getopt
import re
from parse_tweet import *
from parse_url import *
from combine_urls import *
import urllib2
import socket
socket.setdefaulttimeout(10)
#################################################################
urls_pat = re.compile(r'<a [^<>]*?href=("|\')http:\/\/([^<>"\']*?)("|\')')
root_pat = re.compile('http\:\/\/[\w\.]+\/?$')
#####different id pattern#######
arxiv_pat = re.compile("\d\d\d\d\.\d\d\d\d")
#pnas_pat = re.compile("10\.1073\/pnas\.[\w]+")
pnas_pat = re.compile("10\.1073\/[\w\.]+")
#scm_pat = re.compile("10\.1126\/science\.[\w\.\-]+")
scm_pat = re.compile("10\.1126\/[\w\.\-]+")
#plos_pat = re.compile("10\.1371\/journal\.[\w\.]+")
plos_pat = re.compile("10\.1371\/[\w\.]+")
nature_pat = re.compile("10\.1038\/[\w\.\-]+")

def parse_args():
    opts, args = getopt.getopt(sys.argv[1:], "t:")
    #####defulat value#####
    tweet_type = 'arxiv'
    #######################
    for o, a in opts:
        if o == "-t":
            tweet_type = a
        else:
            print 'Unknown optionts:', o
            exit(2)
    return tweet_type


def extract_id(url, tweet_type, is_iter=True):
    if tweet_type != 'pnas.org' and tweet_type != 'sciencemag.org':
        url = httplib_expand_url(url)
    #print url
    url = clean_url(url, tweet_type)
    id = extract_id_from_url(url, tweet_type)
    if not id:
	id = parse_page(url, tweet_type, is_iter)
    return id

def parse_page(url, tweet_type, is_iter):
    if tweet_type == 'arxiv' and 'arxiv.org' in url.lower():
	return 'error'
    if (tweet_type == 'pnas.org'  or tweet_type == 'sciencemag.org') and url.endswith('.pdf'):
	url = url.rstrip('.pdf') 
    page = extract_webpage_content(url)
    if not page:
	id = 'error'
    else:
        if tweet_type in page.lower():
            id = extract_id_from_webpage(page, tweet_type)
	    #print 'web page id found:', id
            if not id and is_iter:
		#print 'parsing web page urls...'
	        urls = extract_urls_from_webpage(page, tweet_type)
		#print urls
	        if not urls:
		    id = 'error'
		else:
	            url = max(urls, key=lambda x:len(x))
		    if not root_pat.match(url):
		#print 'find url', url
	                id = extract_id(url, tweet_type, False)
		    else:
		        id = 'error'
	    #else:
	    #	id = 'error'
	    	#print 'web page id found:', id
		#id = 'error'
	    elif not id:
		id = 'error'
    	else:
	    id = 'error'
    #print id
    return id
def extract_urls_from_webpage(webpage, tweet_type):
    #print webpage
    result = urls_pat.findall(webpage)
    url_list = []
    if tweet_type == 'pnas.org':
	tweet_type = 'www.' + tweet_type
    for item in result:
	link = "http://" + item[1]
	if tweet_type in link:
	    url_list.append(link)
    return url_list

def extract_id_from_webpage(webpage, tweet_type):
    if tweet_type == 'arxiv':
	id_pat = arxiv_pat
    elif tweet_type == 'pnas.org':
	id_pat = pnas_pat
    elif tweet_type == 'sciencemag.org':
	id_pat = scm_pat
    elif tweet_type == 'plos':
	id_pat = plos_pat
    elif tweet_type == 'nature.com':
	id_pat = nature_pat
    else:
	print "unknown pattern"
	exit(0)

    id_list = id_pat.findall(webpage)
    if not id_list:
	id = ''
    else:
	id = id_list[0]
    return id

    
def extract_webpage_content(url):
    try:
        web = urllib2.urlopen(url)
        content = web.read()
        web.close()
    except:
	#print 'access denied for', url
	content = ''
    return content
    
	 
def extract_id_unparsed_urls(to_be_parsed_file, id_file, error_file, tweet_type):
    infile = open(to_be_parsed_file, 'r')
    id_lines = []
    error_lines = []
    index = 0
    for line in infile:
	url = line.rstrip('\n').split('\t')[0]
	id = extract_id(url, tweet_type)
	if id == 'error':
	    error_lines.append(url + '\n')
	else:
	    id_lines.append(url + '\t' + id + '\n')
	index += 1
	if not (index % 100):
	    print index
	    #break
    infile.close()

    outfile = open(id_file, 'w')
    outfile.writelines(id_lines)
    outfile.close()

    outfile = open(error_file, 'w')
    outfile.writelines(error_lines)
    outfile.close() 

def main():
    tweet_type = parse_args()
    id_file = os.path.join(dat_dir, tweet_type, 'parsed_url_id.txt')
    error_file = os.path.join(dat_dir, tweet_type, 'parsed_error_urls.txt')
    parse_file = os.path.join(dat_dir, tweet_type, 'to_be_parsed_urls.txt')
    extract_id_unparsed_urls(parse_file, id_file, error_file, tweet_type)
 
def test():
    tweet_type = 'sciencemag.org'
    url = "http://stm.sciencemag.org/cgi/content/short/4/149/149ec155"
    id = extract_id(url, tweet_type)
    print [id]    
#test()

if __name__ == '__main__':
    main()


