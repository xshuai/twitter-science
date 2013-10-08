#########################count the number and types of #################################################social cascades#########################################################################################################################
import os
cas_dir = "/home/twitterBollen/xshuai/science_social_media/twitter/dat/nature.com/doi_tweets/cascade_size/"

index = 1
infile = open(os.path.join(cas_dir, str(index) + '.size'), 'r')
user_count = {}
for line in infile:
    users = line.rstrip('\n').split(',')
    for user in users:
	try:
	    user_count[user] += 1
	except KeyError:
	    user_count[user] = 1

user_count = sorted(user_count.items(), key=lambda x:x[1], reverse=True)
write_lines = []
for user, count in user_count:
    newline = user + '\t' + str(count) + '\n'
    write_lines.append(newline)
outfile = open('temp.txt', 'w')
outfile.writelines(write_lines)
outfile.close()
