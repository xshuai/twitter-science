#!/usr/bin/python
# coding: utf-8
###########################This script is used to rank all urls###############################
import sys
import os
import getopt

import parse_tweet
target = 'http://t.'
root = "/home/twitterBollen/xshuai/science_social_media/twitter/"
urls_count = {}

def parse_args():
    opts, args = getopt.getopt(sys.argv[1:], "t:")
    #####defulat value#####
    tweet_type = 'nature.com'
    #######################
    for o, a in opts:
        if o == "-t":
            tweet_type = a
        else:
            print 'Unknown optionts:', o
            exit(2)
    return tweet_type

#def parse_tweets_file(tweet_file):
    
    
def extract_urls(tweet_file, tweet_type):
    infile = open(tweet_file, 'r')
    for line in infile:
	try:
	    tweet = parse_tweet.Tweet(line)
	except:
	    print 'error!'
	    print line
	    continue

	if not tweet.parsed_urls:
	    #print line
	    continue
	
	find_urls = tweet.parsed_urls.split()
	for url in find_urls:
	    if url == target:
		print 'found in:', line
	#	exit(0)
	    if not url.startswith("http"):
		url = "http://" + url
	    try:
		urls_count[url] += 1
	    except KeyError:
		urls_count[url] = 1
	    
	#if tweet_type not in parsed_url:
	#    try:
	#	short_urls_count[parsed_url] += 1
	#    except KeyError:
	#	short_urls_count[parsed_url] = 1
    #infile.close()

def main():
    tweet_type = parse_args()  
    tweet_file = root + 'dat/' + tweet_type + '/ext_tweets.txt'
    extract_urls(tweet_file, tweet_type)
    ranked_urls = sorted(urls_count.items(), key=lambda x:x[1], reverse=True)

    url_file = root + 'dat/' + tweet_type + '/url_count.txt'
    write_lines = []
    for url, count in ranked_urls:
        newline = url + '\t' + str(count) + '\n'
    	write_lines.append(newline)

    outfile = open(url_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

main()

