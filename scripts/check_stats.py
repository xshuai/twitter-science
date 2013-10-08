#!/usr/bin/python
#################check some basic statistics about tweets###############################################################################################################
import parse_tweet
author_count = {}
root = "/home/twitterBollen/xshuai/science_social_media/twitter/"

infile = open(root + 'dat/nature.com/ext_tweets.txt', 'r')
for line in infile:
    tweet = parse_tweet.Tweet(line)
    author = tweet.user
    try:
	author_count[author] += 1
    except KeyError:
	author_count[author] = 1

outfile = open(root + 'dat/nature.com/author_count.txt', 'w')
write_lines = []
sorted_author_count = sorted(author_count.items(), key=lambda x:x[1], reverse=True)
for author, count in sorted_author_count:
    newline = author + '\t' + str(count) + '\n'
    write_lines.append(newline)

outfile.writelines(write_lines)
outfile.close()

