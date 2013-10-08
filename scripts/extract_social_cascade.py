#####################################################################################################generate social cascades based on###############################################user relations#############################################################################################################################
import os, sys


dat_dir = "/home/twitterBollen/xshuai/science_social_media/twitter/dat/nature.com"
index_seq = range(1, 361)
for i in index_seq:
    infile = open(os.path.join(dat_dir, 'doi_tweets', 'user_relation', str(i) + '.rel'), 'r')
    all_lines = infile.readlines()
    all_lines.pop(0)
    write_lines = []
    for line in all_lines:
	content = line.rstrip('\n').split(',')
	date = content[0]
	user = content[1]
	retweet = content[2].split('|')
	newline = date + '\t'
	newline += user + ','
	newline += ','.join(retweet)
	newline = newline.rstrip(',') + '\n'
	write_lines.append(newline)
	outfile = open(os.path.join(dat_dir, 'doi_tweets', 'social_cascade', str(i) + '.cas'), 'w')
	outfile.writelines(write_lines)
        outfile.close()

