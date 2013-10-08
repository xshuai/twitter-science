#!/usr/bin/python
# coding: utf-8
##################################################################################################Count the occurrence of paper ids in tweets###################################################################################################

############import modules#######################
from parse_tweet import *
import os, sys
import getopt
from datetime import *
from extract_id_from_webpage import *
#################################################

url_count = {}
url_id = {}
id_freq_tweets = {}
id_freq_dates = {}
nature_id = {}
def get_url_count(url_file):
    """get counts of all urls"""
    #url_count = {}
    infile = open(url_file, 'r')
    for line in infile:
	content = line.rstrip('\n').split('\t')
        url = content[0]
	count = int(content[1])
	url_count[url] = count
    infile.close()

def get_id_url(url_id_dir, url_file, tweet_type):
    """get the mapping between url and paper id"""
    #raw_parsed = {}

    parsed_id = {}
    for r,d,files in os.walk(url_id_dir):
        break
    for f in files:
	if 'url_id' in f:
	    infile = open(os.path.join(r, f), 'r')
	    for line in infile:
		content = line.rstrip('\n').split('\t')
		parsed_url = content[0]
		id = content[1]
		id = id.rstrip('.')
		if root_pat.match(parsed_url) and tweet_type in parsed_url.lower():
            	    print parsed_url, id
            	    continue
		if tweet_type == 'nature.com':
		    if id == 'error':
			continue
		    uniq_id = id.replace('.', '')
		    if uniq_id.startswith('101038') and '-' not in uniq_id and uniq_id[7].isalpha() and uniq_id[-1].isalpha():
			uniq_id = uniq_id[:-1] 
		    try:
			nature_id[uniq_id].add(id)
		    except KeyError:
			nature_id[uniq_id] = set([id])
		    id = uniq_id
		parsed_id[parsed_url] = id 
    	    infile.close()

    infile = open(url_file, 'r')
    for line in infile:
        content = line.rstrip('\n').split('\t')
        parsed_url = content[0]
	raw_urls = content[1].split('~@~')
	try:
	    id = parsed_id[parsed_url]
	except KeyError:
	    continue
        for url in raw_urls:
	    url_id[url] = id
            

    infile.close()


def count_id_freq(tweet_file, id_tweet_file, id_date_file, tweet_type):
    """count the occurrence frequency of paper id in archived tweets"""
    infile = open(tweet_file, 'r')
    for line in infile:
        try:
            tweet = Tweet(line)
        except:
            continue

        if not tweet.parsed_urls:
            continue

        date = tweet.date.split('T')[0]
	t = line.rstrip('\n')
        find_urls = tweet.parsed_urls.split()
        for url in find_urls:
            if not url.startswith("http"):
                url = "http://" + url
	    ####see if the url contains paper id#####
	    try:
		id = url_id[url]
		if tweet_type == 'nature.com':
		    for iid in list(nature_id[id]):
			id = iid
			if iid.count('.') > 1:
			    break
		    #id = max(list(nature_id[id]), key=lambda x:len(x))
	    except KeyError:
		continue
            ######record tweet for each paper id######
	    #print id
	    t = t.replace('\t', ' ')
            try:
		id_freq_tweets[id].add(t)
	    except KeyError:
		id_freq_tweets[id] = set([t])	
	    #####record date for each paper id########
	    try:
		id_freq_dates[id][date].add(t)
	    except KeyError:
		try:
		    id_freq_dates[id][date] = set([t])
		except KeyError:
		    id_freq_dates[id] = {}
		    id_freq_dates[id][date] = set([t])
    infile.close()

    #############save the result###########
    #write_lines = []
    #for id, dates in id_freq_dates.items():
    #    sorted_dates = sorted(dates.items(), key=lambda x:datetime.strptime(x[0], "%Y-%m-%d"))
    #	newline = id + '\t'
    #	for d in sorted_dates:
    #	    newline += d[0] + ',' + str(d[1]) + '|'
    #	newline = newline.rstrip('|') + '\n'
    #	write_lines.append(newline)
    #outfile = open(id_date_file, 'w')
    #outfile.writelines(write_lines)
    #outfile.close()
    #################
    sorted_freq_tweets = sorted(id_freq_tweets.items(), key=lambda x:len(x[1]), reverse=True)
    write_lines = []
    for id, tweets in sorted_freq_tweets:
	tweets = list(tweets)
	sorted_tweets = sorted(tweets, key=lambda x:int(x.split('|')[0]))
	newline = id + '\t' + str(len(sorted_tweets)) + '\t' + '&&&'.join(sorted_tweets) + '\n'
	write_lines.append(newline)
    outfile = open(id_tweet_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

    ####################
    #sorted_freq_dates = sorted(id_freq_dates.items(), key=lambda x:sum(x[1].values()), reverse=True)
    write_lines = []
    for id, tweets in sorted_freq_tweets:
	dates = id_freq_dates[id]
        sorted_dates = sorted(dates.items(), key=lambda x:datetime.strptime(x[0], "%Y-%m-%d"))
	#print dates
        sum_dates = 0
	for d, t in sorted_dates:
	    sum_dates += len(t)
        newline = id + '\t' + str(sum_dates) + '\t'
        for d in sorted_dates:
            newline += d[0] + ',' + str(len(d[1])) + '|'
        newline = newline.rstrip('|') + '\n'
        write_lines.append(newline)
    outfile = open(id_date_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

    if tweet_type == 'nature.com':
	write_lines = []
	for uniq_id, id_list in nature_id.items():
	    if len(id_list) > 1:
		newline = uniq_id + '\t' + '|'.join(id_list) + '\n'
		write_lines.append(newline)
	outfile = open(os.path.join(dat_dir, 'nature.com', 'root_ids.txt'), 'w')
	outfile.writelines(write_lines)
	outfile.close()


def main():
    tweet_type = parse_args()
    url_file = os.path.join(dat_dir, tweet_type, 'url_count.txt')
    tweet_file = os.path.join(dat_dir, tweet_type, 'ext_tweets.txt')
    url_id_dir = os.path.join(dat_dir, tweet_type)
    clean_url_file = os.path.join(dat_dir, tweet_type, 'final_cleaned_urls.txt')
    id_tweet_file = os.path.join(dat_dir, tweet_type, 'id_tweets.txt')
    id_date_file = os.path.join(dat_dir, tweet_type, 'id_dates.txt')
    get_url_count(url_file)
    get_id_url(url_id_dir, clean_url_file, tweet_type)
    count_id_freq(tweet_file, id_tweet_file, id_date_file, tweet_type) 
	
    
main()
 
    
    
     


