#!/usr/bin/python
# coding: utf-8
#######################################################################################################extract nature.com news id###############################################################################################################
from parse_url import *
from parse_tweet import *
import os, sys
from combine_urls import *
from extract_id_from_webpage import * 

url_id = {}
#####################################
def extract_parsed_url_id(old_url_file):
    infile = open(old_url_file, 'r')
    for line in infile:
	content = line.rstrip('\n').split('\t')
	url = clean_url(content[1], 'nature.com')
	try:
	    id = content[2]
	except:
	    continue
	if 'doi:' in id:
	    url_id[url] = id.replace('doi:', '')

def is_nature_news_url(url):
    if 'nature.com/news' in url:
	url_parts = url.split('/')
	key_part = url_parts[-1]
	key_part = key_part.replace('.html', '')
	words = key_part.split('-')
	last = words[-1]
	try:
	    float(last)
	    return True
	except:
	    return False
    else:
	return False  

def filter_nature_news_url(url_dir, parsed_url_file, unparsed_url_file, tweet_type='nature.com/news'):
    for r,d,files in os.walk(url_dir):
        break
    parsed_lines = []
    unparsed_lines = []
    #raw_inner = {}
    for f in files:
        if 'parsed_error_urls' in f:
            infile = open(os.path.join(r, f), 'r') 
	    index = 0
    	    for line in infile:
		url = line.rstrip('\n')
		raw_url = url
		if not is_nature_news_url(url):
		    ##########first parse the url itself#####
		    url = httplib_expand_url(url)
    		    url = clean_url(url, tweet_type)
		    #########then parse the url web page######
		    if not is_nature_news_url(url):
			webpage = extract_webpage_content(url)
		        urls = extract_urls_from_webpage(webpage, tweet_type)
			is_found = False 
			for url in urls:
			    url = httplib_expand_url(url)
                    	    url = clean_url(url, tweet_type)
		    	    if is_nature_news_url(url):
				is_found = True
				#print raw_url, url
				break
			if not is_found:
			    #try:
			    #	raw_inner[url].append(raw_url)
			    #except KeyError:
			    #	raw_inner[url] = [raw_url]
			#else:
			    continue 
			    
			
		    else:
			pass
		else:
		    pass
			    
		try:
		    id = url_id[url]
		    newline = raw_url + '\t' + id + '\n'
		    parsed_lines.append(newline)
		except KeyError:
		    if url == raw_url:
		        newline = raw_url + '\n'
		    else:
			newline = raw_url + '\t' + url + '\n'
		    unparsed_lines.append(newline)
		index += 1
		if not (index % 100):
		    print index
		#if index > 20:
		#    break
    	    infile.close()
		    		 
    ############save results###############
    outfile = open(parsed_url_file, 'w')
    outfile.writelines(parsed_lines)
    outfile.close()

    outfile = open(unparsed_url_file, 'w')
    outfile.writelines(unparsed_lines)
    outfile.close()
    ########################################

def main():
    old_url_file = os.path.join(dat_dir, 'nature.com.old', 'final_parsed_urls.txt')
    url_id = extract_parsed_url_id(old_url_file)
    url_dir = os.path.join(dat_dir, 'nature.com')
    parsed_url_file = os.path.join(dat_dir, 'nature.com', 'old_parsed_url_id.txt')
    unparsed_url_file = os.path.join(dat_dir, 'nature.com', 'to_be_parsed_news_url.txt')
    filter_nature_news_url(url_dir, parsed_url_file, unparsed_url_file)

main()
    
