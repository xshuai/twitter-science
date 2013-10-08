#!/usr/bin/python
################################################################################
################parse url and extract doi information#####################################
import urllib2
import re
import socket

socket.setdefaulttimeout(20)

doi_pat = re.compile("doi:[^\"<>]+")
root = "/home/twitterBollen/xshuai/science_social_media/twitter/"
url_info = {}
write_lines = []

input_file = root + 'dat/' + 'nature.com' + '/url_count1.txt'
output_file = root + 'dat/' + 'nature.com' + '/parsed_urls1.txt'

index = 0
infile = open(input_file, 'r')
for line in infile:
    url, count = line.split()
    url_info[url] = {}

    try:
        html = urllib2.urlopen(url)
	text = html.read()
        org_url = html.geturl()
    except:
	newline = url + '\terror\terror\n'
	write_lines.append(newline)
	continue
    
    
    doi = ''
    match = doi_pat.search(text)
    if match != None:
	doi = match.group()

    if doi:
	newline = url + '\t' + org_url + '\t' + doi + '\n'
    elif 'blogs.nature.com' in org_url:
	newline = url + '\t' + org_url + '\tblog\n'
    else:
	newline = url + '\t' + org_url + '\tirrelevant\n'

    write_lines.append(newline)
    index += 1
    if (index % 100) == 0:
	print index
	outfile = open(output_file, 'w')
        outfile.writelines(write_lines)
        outfile.close()


	
outfile = open(output_file, 'w')
outfile.writelines(write_lines)
outfile.close()    

