#!/usr/bin/python
# coding: utf-8
#############################This module is used for parsing tweet seperated by '|'#####################################
import re

url_pat = re.compile('(http://\S+|https://\S+|www.\S+)',re.I)

class Tweet:
    """
    A Tweet Class contains all information about a tweet, including id, author, date, text, etc.
    """
    def __init__(self, line):
	content = line.rstrip('\n').split('|')
	if len(content) == 14:
	    id, date, text, parsed_urls, user, location, \
	    lang, status_count, followers_count, retweet_count, \
	    retweet_from_id, retweet_from_user, \
	    reply_to_id, reply_to_user = content
	else:
	    id = content[0]
	    date = content[1]
	    reply_to_user = content[-1]
	    reply_to_id = content[-2]
	    retweet_from_user = content[-3]
	    retweet_from_id = content[-4]
	    retweet_count = content[-5]
	    followers_count = content[-6]
	    status_count = content[-7]
	    lang = content[-8]
	    text, parsed_urls, user, location = self.parse_fuzzy_content(content[2:-8])

	if not parsed_urls:
	    parsed_urls = ' '.join(re.findall(url_pat, text))

	self.id = id
	self.date = date
	self.text = text
	self.parsed_urls = parsed_urls
	self.user = user
	self.location = location
	self.lang = lang
	self.status_count = int(status_count)
	self.followers_count = int(followers_count)
	self.retweet_count = int(retweet_count.replace('+',''))
	self.retweet_from_id = retweet_from_id
	self.retweet_from_user = retweet_from_user
	self.reply_to_id = reply_to_id
	self.reply_to_user = reply_to_user

    def parse_fuzzy_content(self, content):
	parsed_urls = ''
	for item in content:
	    if item.startswith('http'):
		parsed_urls = item
		url_index = content.index(item)
		break
	if not parsed_urls:
	    url_index = content.index('')
	user = content[url_index+1]

	text = ' '.join(content[:url_index])
	location = ' '.join(content[url_index+2:])

	return text, parsed_urls, user, location
	
