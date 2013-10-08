#!/usr/bin/python
# coding: utf-8
################################################################################
###########filter our all short urls that are needed to be further parsed#######################################################################################
import sys
import os
import getopt
import re
from parse_tweet import *
import urllib2

short_pat = re.compile("http://[\w]+\.[\w]+/[\w]+$")
short_urls_count = {}

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

#def parse_tweets_file(tweet_file):
    
def is_short_url(url):
    """judge whether url is a shortened version"""
    if "twitpic.com" in url:
	return False
    if "//feed" in urllib2.unquote(url):
	return True
    res =  short_pat.match(url)
    if res:
	return True
    else:
	return False
    
        
def extract_short_urls(url_file, tweet_type):
    short_urls = []
    infile = open(url_file, 'r')
    for line in infile:
	content = line.split()
	url = content[0]
	if tweet_type not in url.lower() or "//feed" in urllib2.unquote(url):
	    short_urls.append(url)
	    
    infile.close()
    return short_urls

def main():
    tweet_type = parse_args()  
    url_file = os.path.join(dat_dir, tweet_type, "url_count.txt")
    #url_file = root + 'dat/' + tweet_type + '_ext.tweet'
    short_urls = extract_short_urls(url_file, tweet_type)
    #sorted_urls = sorted(short_urls_count.items(), key=lambda x:x[1], reverse=True)
    short_file = os.path.join(dat_dir, tweet_type, "short_urls.txt")
    #short_file = root + 'dat/' + tweet_type + '.short'
    write_lines = []
    for url in short_urls:
        newline = url +'\n'
	write_lines.append(newline)

    outfile = open(short_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

def test():
    url = 'http://dx.doi.org/10.1038/nature.2012.9751'
    print is_short_url(url)
main()
#test()
