#!/usr/bin/python
#############################This script is used to combine splitted tweets files######################
############################remove duplicate records and sort them based on time order#################
import sys
import os
import getopt

root = "/home/twitterBollen/xshuai/science_social_media/twitter/"

def parse_args():
    opts, args = getopt.getopt(sys.argv[1:], "t:f:")
    #####defulat value#####
    tweets_type = 'nature.com'
    file_type = 'ext'    
    #######################
    for o, a in opts:
        if o == "-t":
            tweets_type = a
        elif o == "-f":
            file_type = a
        else:
            print 'Unknown optionts:', o
            exit(2)
    return tweets_type, file_type

def combine_tweets(tweets_dir, file_type, outfile_name):
    #extract all files in the relevant tweets directory
    for r, d, files in os.walk(tweets_dir):
	break

    #specify different types of seperation symbol
    if file_type == 'ext':
	sep = '|'
    else:
	sep = '\t'

    #aggregate all lines from all tweets files
    id_line = {}
    for f in files:
	if file_type not in f:
	    continue
	infile = open(r + '/' + f, 'r')
	for line in infile:
	    content = line.rstrip('\n').split(sep)
	    try:
	        id = int(content[0])
	        id_line[id] = line
	    except:
	        print f
		print line
		id_line[id] = id_line[id].rstrip('\n') + line 
        infile.close()

    #sort tweets according to tweet Ids
    sorted_lines = sorted(id_line.items(), key=lambda x:x[0])
    ranked_lines = [line for id, line in sorted_lines]
   
    #finally write all tweets to a outfile
    outfile = open(outfile_name, 'w')
    outfile.writelines(ranked_lines)
    outfile.close()
	
def main():
    tweets_type, file_type = parse_args()
    tweets_dir = root + 'tweets/' + tweets_type
    outfile_name = root + 'dat/' + tweets_type + "/" + file_type + "_tweets.txt"    
    combine_tweets(tweets_dir, file_type, outfile_name)

    
main()
    
