#!/usr/bin/python
# coding: utf-8
##################################################################################################combine long and short urls###################################################################################################################
###import libraries####
import os, sys
import re
from parse_tweet import *
import urllib2
import getopt
from short_url_expander import *
#######################
#url_pat = re.compile()

######################
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

def clean_url(url, tweet_type):
    """clean the url"""

    ####first, decode the url##########
    k = 3###make sure the url is fully decoded
    i = 0
    while True:
	url = urllib2.unquote(url)
	i += 1
	if i >= k:
	    break
    ###################################
    #####second, split multiple urls and pick up one###
    if url.count('http:') > 1:
	url_splits = []
	#for m in re.finditer('http', url):
	#    u = url[m.start() : m.end()]
	#    urls.append(u)
	index = 0
	while index < len(url):
	    index = url.find('http:', index)
	    if index == -1:
		break
	    url_splits.append(index)
	    index += len('http:')		
        
	max_url_len = 0
        max_url = ''
        target_url = ''
        for i in range(len(url_splits)):
	    #print i
	    try:
	        cur_url = url[url_splits[i] : url_splits[i+1]]
	    except:
	        cur_url = url[url_splits[i] : ]
	    #print tweet_type
	    if tweet_type in cur_url:
	        #print 'we found:', cur_url
	        target_url = cur_url
	        break
	    else:
	        if len(cur_url) >= max_url_len:
		    max_url = cur_url
		    max_url_len = len(cur_url)
        if not target_url:
	    target_url = max_url
	try:
	    url = target_url[ : target_url.index('&')]
	except:
	    url = target_url
	
    url = url.replace(':/', '://').replace(':///', '://')

    ###########third, try to find to original url################
    #iter = 0
    #max = 3
    #while iter < max:
    #    url = httplib_expand_url(url)
    #    iter += 1
    

    ###########finally, extract the main part from the url#######
    parsed_url = urllib2.urlparse.urlparse(url)
    clean_url = "http://" + parsed_url.netloc + parsed_url.path
    clean_url = clean_url.rstrip('/')
    return clean_url

def combine_urls(raw_url_file, parsed_url_file, combined_url_file, tweet_type):
    """aggregate urls that actually refer to the same sites"""
    short_long = {}
    uniq_multi = {}
    infile = open(parsed_url_file, 'r')
    for line in infile:
	content = line.rstrip('\n').split('\t')
	short = content[0]
	long = content[1]
	long = clean_url(long, tweet_type)
	short_long[short] = long
	try:
	    uniq_multi[long].append(short)
	except KeyError:
	    uniq_multi[long] = [short]
    infile.close()

    infile = open(raw_url_file, 'r')
    for line in infile:
	content = line.rstrip('\n').split('\t')
	raw_url = content[0]
	if tweet_type in raw_url.lower():
	   url = clean_url(raw_url, tweet_type)
	   try:
		uniq_multi[url].append(raw_url)
	   except KeyError:
		uniq_multi[url] = [raw_url]
	else:
	    try:
		short_long[raw_url]
	    except KeyError:
		print raw_url 
    infile.close()

    ############recombine urls############################
##   all_uniq_urls = uniq_multi.keys()
##    parsedurl_url = {}
##    print "being to recombine urls:", len(all_uniq_urls)
##    index = 0
##    for url in all_uniq_urls:
##	iter = 0
##        max = 3
##        raw_url = url
##        while iter < max:
##            cur_url = httplib_expand_url(url)
##	    if cur_url == url:
##	        #print url
##		#url_parsedurl[raw_url] = url
##		break
##	    else:
##		iter += 1
##		if 'http://' not in cur_url:
##                    break
##		#cur_url = clean_url(cur_url, tweet_type)
##		#url_parsedurl[raw_url] = cur_url
##		url = cur_url
##	if url == raw_url:
##	    print index
##	    print raw_url, 'becomes:', url
##        url = clean_url(url, tweet_type)
##	try:
##	    parsedurl_url[url].append(raw_url)
##	except KeyError:
##	    parsedurl_url[url] = [raw_url]
##	index += 1
##	if not (index % 100):
##	    print index
##    #for url, parsedurl in url_parsedurl.items():
##    #	cleaned_url = clean_url(parsedurl, tweet_type)
##    new_uniq_multi = {}
##    for parsed_url, url_list in parsedurl_url.items():
##	new_uniq_multi[parsed_url] = []
##	for u in url_list:
##	    new_uniq_multi[parsed_url] += uniq_multi[u]
##	
##	
##
##
    ######################################################

    write_lines = []
    for uniq, multi in uniq_multi.items():
	newline = uniq + '\t' + '~@~'.join(multi) + '\n'
	write_lines.append(newline)
    outfile = open(combined_url_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()
    
    
	

def test_clean_url(url, tweet_type):
    print url
    print [clean_url(url, tweet_type)]     


#main()
#url = "http://www.google.com/url?sa%3DX%26q%3Dhttp://www.nature.com/nnano/journal/v6/n12/full/nnano.2011.219.html%26ct%3Dga%26cad%3DCAcQARgAIAEoATAAOABAp-6E9wRIAlgAYgVlbi1BVQ%26cd%3DeFtbXPffPcY%26usg%3DAFQjCNFb3cJ9RwDKTf65mvU7VXbdSQTtfg"
#tweet_type = "nature.com"
#test_clean_url(url, tweet_type)
#exit(0)
#tweet_type = "pnas.org"
def print_urls(tweet_type):
    url_file = os.path.join(dat_dir, tweet_type, "final_parsed_short_urls.txt")
    infile = open(url_file, 'r')
#count = 0
    all_lines = infile.readlines()
    infile.close()
#print "all lines:", len(all_lines)
    for line in all_lines:
        content = line.rstrip('\n').split('\t')
        parsed_url = content[-1]
	url = content[0]
        if parsed_url.count('http') >= 2 and '=http' not in parsed_url:
#    if parsed_url.count('http') > 2:
	    print url, parsed_url

#    if tweet_type in parsed_url:
#	count += 1
#print "target lines:", count

def main():
    tweet_type = parse_args()
    #print_urls(tweet_type)
    #exit(0)
    raw_url_file = os.path.join(dat_dir, tweet_type, 'url_count.txt')
    parsed_url_file = os.path.join(dat_dir, tweet_type, 'final_parsed_short_urls.txt')
    combined_url_file = os.path.join(dat_dir, tweet_type, 'final_cleaned_urls.txt')
    combine_urls(raw_url_file, parsed_url_file, combined_url_file, tweet_type)


if __name__ == "__main__":
    main()
 
#main()
