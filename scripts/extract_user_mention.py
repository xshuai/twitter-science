########################extract all users and mention users#####################################################################################################################################################################################
import parse_tweet
import re

mention = re.compile("@[\w]+", re.IGNORECASE)

cutoff = 360
infile = open("doi_tweets.txt", 'r')
all_lines = infile.readlines()
target_lines = all_lines[:360]
infile.close()

users = set([])
mentions = set([])

for line in all_lines:
    content = line.rstrip('\n').split('\t')
    doi = content[0]
    freq = int(content[1])
    tweets = content[2].split('&&&')
    for tweet in tweets:
	rel_users = extract_user_relation(tweet)
	
	
     
doi_index = 2
target_line = all_lines[doi_index]
content = target_line.rstrip('\n').split('\t')
doi = content[0]
number = content[1]
tweets = content[2].split('&&&')
outfile = open("./doi_tweets/" + str(doi_index) + ".txt", 'w')
write_lines = [doi + '\n' + number + '\n']
for tweet in tweets:
    write_lines.append(tweet + '\n')
outfile.writelines(write_lines)
outfile.close()

