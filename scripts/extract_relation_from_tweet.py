########################extract all users and mention users#####################################################################################################################################################################################
import parse_tweet
import re
import extract_user_relation
import os, sys
#mention = re.compile("@[\w]+", re.IGNORECASE)

dat_dir = "/home/twitterBollen/xshuai/science_social_media/twitter/dat/nature.com"
infile = open(os.path.join(dat_dir, "doi_tweets.txt"), 'r')
all_lines = infile.readlines()
infile.close()

#users = set([])
#mentions = set([])

#for line in all_lines:
#    content = line.rstrip('\n').split('\t')
#    doi = content[0]
#    freq = int(content[1])
#    tweets = content[2].split('&&&')
#    for tweet in tweets:
	
index_seq = range(1, 361)#####parse all doi that receives greater than 100
     
for index in index_seq:
    target_line = all_lines[index - 1]
    content = target_line.rstrip('\n').split('\t')
    doi = content[0]
    number = content[1]
    tweets = content[2].split('&&&')
    ##############extract relationship###################
#outfile = open("./doi_tweets/" + str(doi_index) + ".txt", 'w')
#write_lines = [doi + '\n' + number + '\n']
    write_lines = ['user,retweet,reply,mention\n']
    for tweet in tweets:
	time = parse_tweet.Tweet(tweet).date
	user_relation = extract_user_relation.extract_user_relation(tweet)
	newline = time + ','
	newline += user_relation['author'] + ','
        newline += '|'.join(user_relation['retweet']) + ','
	newline += '|'.join(user_relation['reply']) + ','
	newline += '|'.join(user_relation['mention']) + '\n'
        write_lines.append(newline)
	outfile = open(os.path.join(dat_dir, 'doi_tweets', 'user_relation', str(index) + '.rel'), 'w')
	
	outfile.writelines(write_lines)
	outfile.close()

