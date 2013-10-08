#!/usr/bin/python
###########################This script is used to filter our all short urls that are needed to be further parsed###############################
import sys
import os
import getopt

root = "/home/twitterBollen/xshuai/science_social_media/twitter/"
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
    
    
def extract_short_urls(tweet_file, tweet_type):
    infile = open(tweet_file, 'r')
    for line in infile:
	content = line.rstrip('\n').split('|')
	parsed_url = content[3]
	if tweet_type not in parsed_url:
	    try:
		short_urls_count[parsed_url] += 1
	    except KeyError:
		short_urls_count[parsed_url] = 1
    infile.close()

def main():
    tweet_type = parse_args()  
    tweet_file = root + 'dat/' + tweet_type + '_ext.tweet'
    extract_short_urls(tweet_file, tweet_type)
    sorted_urls = sorted(short_urls_count.items(), key=lambda x:x[1], reverse=True)

    short_file = root + 'dat/' + tweet_type + '.short'
    write_lines = []
    for url, count in sorted_urls:
        newline = url + '\t' + str(count) + '\n'
	write_lines.append(newline)

    outfile = open(short_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

main()

