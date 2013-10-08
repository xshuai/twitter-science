#!/usr/bin/python
# coding: utf-8
####################################################################################################parse url string and extract article id#####################################################################################################
import sys
import os
import getopt
import re
from parse_tweet import *

############build patterns###############
arxiv_pat = re.compile("(\d\d\d\d\.\d\d\d\d|\W\d\d\d\d\d\d\d)")
scm_pat = re.compile("science\.\d+\D?", re.I)
#digit_pat =  
#########################################

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

def parse_arxiv(url):
    if 'arxiv' in url.lower():
        id_pat = arxiv_pat.search(url)
        if id_pat:
	    return id_pat.group().strip('/')
        else:
	    return ''
    else:
	return ''

def parse_plos(url):
    url = url.rstrip('/')
    if 'ploscollections' in url and 'issue' in url:
	id = 'error'
    elif '10.1371' in url:
	pos = url.index('10.1371')
        id = url[pos:]
    elif 'blogs.plos.org' in url:
	url_parts = url.split('/')
        key_part = url_parts[-1]
        key_part = key_part.replace('.html', '')
        if key_part.isdigit():
            id = ''
        else:
            id = key_part
    else:
	id = ''

    return id
	
def parse_science(url):
    url = url.rstrip('/')	
    if '10.1126' in url:
	pos = url.index('10.1126')
	id = url[pos:]
    elif 'scjobs' in url:
	id = 'error'
    elif scm_pat.search(url):
	part = scm_pat.search(url).group().rstrip('.')
	id = '10.1126/' + part
    elif 'blogs.sciencemag.org' in url or 'news.sciencemag.org' in url or 'feeds.feedburner.com' in url:
	if 'html' in url:
	    url_parts = url.split('/')
            key_part = url_parts[-1]
            key_part = key_part.replace('.html', '')
            if key_part.replace('-', '').isdigit():
                id = ''
	    else:
		id = key_part
        else:
	    if 'feeds' in url:
                id = ''
	    else:
		id = 'error'
    else:
	id = ''
	
    return id
		
def parse_pnas(url):
    url = url.rstrip('/')
    if '10.1073' in url:
        pos = url.index('10.1073')
        id = url[pos:]
    elif 'early' in url:
	url_parts = url.split('/')
        key_part = url_parts[-1]
	id = key_part.split('.')[0]
	id = '10.1073/pnas.' + id
    elif 'cgi' in url:
	url_parts = url.split('/')
        key_part = url_parts[-1]
	if 'v' in key_part:
	    id = '10.1073/pnas.' + key_part.split('v')[0]
	else:
	    id = '' 
    else:
        id = ''

    return id	

def parse_nature(url):
    url = url.rstrip('/')
    if '10.1038' in url:
	pos = url.index('10.1038')
	id = url[pos:]
    elif 'naturejobs' in url.lower():
	id = 'error'
    elif 'www.nature.com' in url.lower():
# or 'feeds.nature.com' in url.lower():
	if 'journal' in url or 'news' in url or '/full/' in url  or 'nchina' in url or 'nindia' in url or 'nmiddleeast' in url or 'srep' in url or '/links/' in url or '/pdf/' in url:
	    url_parts = url.split('/')
	    if '/box/' in url and '/full/' in url:
		key_part = url_parts[-3]
	    else:
	        key_part = url_parts[-1]
		#if '_BX' in key_part:
		#    key_part = key_part.split('_BX')
	#if '-' not in key_part:	
 	        key_part = key_part.replace('.html', '').replace('.pdf', '')
		#key_part = key_part.rstrip('l')
	    if 'embor' in url:
		key_part = 'sj.embor.' + key_part
	    elif 'bonekey' in url:
		key_part = 'bonekey.2012' + key_part.replace('bonekey2012', '')

	    #if key_part.isdigit():
	    #	id = "error"
	    if key_part.count('-') < 2:
	        if re.search('\d', key_part) and not key_part.replace('-', '').isdigit():
	            id = '10.1038/' + key_part
	        else:
		    id = ''
	#se:
	#    id = 'error'
	    else:
	        words = key_part.split('-')
	        last = words[-1]
	        try:
	            float(last)
	            id = ''
	        except:
		    id = key_part
	else:
	    id = 'error'

    elif 'feeds.nature.com' in url.lower():
	url_parts = url.split('/')
        key_part = url_parts[-1]
        #if '-' not in key_part:        
        key_part = key_part.replace('.html', '').replace('.pdf', '')
	#key_part = key_part.rstrip('.l')
	if key_part.isdigit():
	    id = 'error'
        elif key_part.count('-') < 2:
            if re.search('\d', key_part):
                id = '10.1038/' + key_part
            else:
                id = ''
        #se:
        #    id = 'error'
        else:
            words = key_part.split('-')
            last = words[-1]
            try:
                float(last)
                id = ''
            except:
                id = key_part

	#else:
	#    id = ''
    elif 'blogs.nature.com' in url.lower() or 'newsblog' in url:
	url_parts = url.split('/')
	key_part = url_parts[-1]
	key_part = key_part.replace('.html', '')
	if '/stories/' in url:
	    id = 'error'
	elif key_part.isdigit():
	    if url.endswith('.html'):
		id = ''
	    else:
	        id = 'error'
	else:
	    id = key_part

    else:
	id = ''
    if '10.1038' in id and ('_' in id):
	id = id.split('_')[0]
    return id
		

def extract_id_from_url(url, tweet_type):
    if tweet_type == 'arxiv':
	id = parse_arxiv(url)
    elif tweet_type == 'nature.com':
	id = parse_nature(url)
    elif tweet_type == 'plos':
	id = parse_plos(url)
    elif tweet_type == 'sciencemag.org':
	id = parse_science(url)
    elif tweet_type == 'pnas.org':
	id = parse_pnas(url)
    else:
	exit(0)
    return id

def parse_urls(url_file, id_file, error_file, parse_file, tweet_type):
    id_lines = []
    error_lines = []
    parse_lines = []
    infile = open(url_file, 'r')
    for line in infile:
	content = line.rstrip('\n').split('\t')
	url = content[0]
	id = extract_id_from_url(url, tweet_type)
	id = id.rstrip('.')
	if id:
	    if id == 'error':
		error_lines.append(url + '\n')
	    else:
		id_lines.append(url + '\t' + id + '\n')
	else:
	    parse_lines.append(url + '\n')
		
	#if not id:
	#if id == 'error':
	  #  newline = url + '\n'
	  #  write_lines.append(newline)
    infile.close()

    outfile = open(id_file, 'w')
    outfile.writelines(id_lines)
    outfile.close()

    outfile = open(error_file, 'w')
    outfile.writelines(error_lines)
    outfile.close()

    outfile = open(parse_file, 'w')
    outfile.writelines(parse_lines)
    outfile.close()

def main():
    tweet_type = parse_args()
    url_file = os.path.join(dat_dir, tweet_type, 'final_cleaned_urls.txt')
    id_file = os.path.join(dat_dir, tweet_type, 'url_id.txt')
    error_file = os.path.join(dat_dir, tweet_type, 'error_urls.txt')
    parse_file = os.path.join(dat_dir, tweet_type, 'to_be_parsed_urls.txt')
    parse_urls(url_file, id_file, error_file, parse_file, tweet_type)
    

    


	    
if __name__ == "__main__":
    main()  
