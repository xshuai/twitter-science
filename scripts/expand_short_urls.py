#!/usr/bin/python
# coding: utf-8
################################################################################
############################expand short urls###################################################################################################################
import sys
import os
import getopt
import time

from parse_tweet import *
from short_url_expander import *
from filter_short_urls import * 

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

def expand_short_urls(short_file, long_file):
    short_long = {}
    index = 0
    infile = open(short_file, 'r')
    for line in infile:
        url = line.rstrip('\n')
	long_url = httplib_expand_url(url)
	short_long[url] = long_url
	index += 1
	#if not long_url:
	#    print url
	if not (index % 1000):
	    print index
	    #break
	    time.sleep(60*2)
    infile.close()
    
    outfile = open(long_file, 'w')
    write_lines = []
    for short, long in short_long.items():
	newline = short + '\t' + long + '\n'
        write_lines.append(newline)
    outfile.writelines(write_lines)
    outfile.close()
	
   
def reexpand_short_urls(parsed_file, null_file, final_file, tweet_type):
    """re-expand short urls""" 
    infile = open(parsed_file, 'r')
    null_lines = []
    final_lines = []
    parsed_short_long = {}
    unparsed_short_long = {}
    for line in infile:
	content = line.rstrip('\n').split('\t')
	short_url = content[0]
	long_url = content[1]
	####get rid of non-ascii code###
	long_url = long_url.replace('”', '')
	#if 'rMAwgpQNBi' in long_url:
	#    print short_url, long_url
	#    exit(0) 
	################################
	if not long_url or is_short_url(long_url):
	    unparsed_short_long[short_url] = long_url
	else:
	    parsed_short_long[short_url] = long_url
    infile.close()
    print "total:", len(unparsed_short_long)
    index = 0    
    for short, long in unparsed_short_long.items():
	try:###already parsed
	    new_long = parsed_short_long[long]
	    parsed_short_long[short] = new_long
	    del unparsed_short_long[short]
	except KeyError:
	    if not long:
	        new_long = httplib_expand_url(short)
	    else:
		new_long = httplib_expand_url(long)
	    iter = 1
	    max = 10
	    while not new_long or is_short_url(new_long):
		new_long = httplib_expand_url(new_long)
		iter += 1
		if iter >= max:
		    break

	    if not new_long or is_short_url(new_long):
		if '//feed' in new_long:
		    parsed_short_long[short] = new_long
		    del unparsed_short_long[short]
		    print 'feed:', [short], [new_long]
		elif 'bit.ly' in new_long or 'bit.ly' in short:
                    print 'bitly:', [short], [new_long]
	    else:
		parsed_short_long[short] = new_long
                del unparsed_short_long[short]
		
 
	    #if not new_long or is_short_url(new_long):
	    #    if not new_long:
	    #	    new2_long = urllib_expand_url(short)
	    #	else:
	    #	    new2_long = urllib_expand_url(new_long)
    
	    #	if not new2_long or is_short_url(new2_long):
	    #	    if 'bit.ly' in new2_long or 'bit.ly' in short:
	    #	        print [short], [new_long], [new2_long]
	    #	else:
	    #	    parsed_short_long[short] = new2_long
            #        del unparsed_short_long[short]
	    #else:
	    #	parsed_short_long[short] = new_long
            #    del unparsed_short_long[short]
    	index += 1
	if not (index % 100):
	    print index
    #####save results#####
    write_lines = []
    for short, long in parsed_short_long.items():
	newline = short + '\t' + long + '\n'
	write_lines.append(newline)
    outfile = open(final_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()
   ##########################
    write_lines = []
    for short, long in unparsed_short_long.items():
        newline = short + '\t' + long + '\n'
        write_lines.append(newline)
    outfile = open(null_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

	
	        
	    
	
	#if not long_url:
	#    continue
	#if tweet_type not in long_url:
	#    print long_url
    	#    index += 1
    #print index

def main():
    tweet_type = parse_args()  
    short_file = os.path.join(dat_dir, tweet_type, "short_urls.txt")
    #url_file = root + 'dat/' + tweet_type + '_ext.tweet'
    long_file = os.path.join(dat_dir, tweet_type, "parsed_short_urls.txt")
    #expand_short_urls(short_file, long_file)
    #exit(0)
    null_file = os.path.join(dat_dir, tweet_type, "null_urls.txt")
    final_file = os.path.join(dat_dir, tweet_type, "final_parsed_short_urls.txt")
    reexpand_short_urls(long_file, null_file, final_file, tweet_type)
    #sorted_urls = sorted(short_urls_count.items(), key=lambda x:x[1], reverse=True)
    #short_file = os.path.join(dat_dir, tweet_type, "short_urls.txt")
    #short_file = root + 'dat/' + tweet_type + '.short'

main()

