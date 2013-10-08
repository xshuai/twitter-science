#!/usr/bin/python
#############################This script is used to combine splitted tweets files######################
############################remove duplicate records and sort them based on time order#################
import sys
import os
import getopt
from parse_tweet import *
import urllib, simplejson
import time
from tweepy import *

#root = "/home/twitterBollen/xshuai/science_social_media/twitter/"

def twitter_api_oauth_setup():
    consumer_key="uOP3KGfsgwbxlovRv0tRwA"
    consumer_secret="fnGGqqeRbRdlJ4n8aofj2DNCk1HQnKgjOcmfrmw"
    access_token="157518326-KQsGswR32zipRn1E8xThkW3pNkrUigoXPezLf0"
    access_token_secret="JCoPnbmntVVJ8OhnJEsvtM48qhnGT9FFZrEPNXtik"
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = API(auth)
    return api
 
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

def parse_error_tweets(api, error_file):
    """re-parse the error tweets"""
    extended_lines = []
        ################################################################
    index = 0
    infile = open(error_file, 'r')
    for line in infile:
	#if '|' in line:
        #    content = line.rstrip('\n').split('|')
	#else:
	content = line.rstrip('\n').split('\t')
	try:
            id = content[0]
            date = content[1]
            user = content[2]
            text = content[3].replace('|', ' ')
	except:
	    print line
	    exit(0)

        ############check api rating limit###########
        index += 1
        if not (index%180):
            print 'parsed',index,'waiting...'
            time.sleep(15 * 60)##wait for 15 minitues
        #############################################

        #########begin to parse tweets status#################
        try:
            status = api.get_status(int(id),include_entities=True)
        except:
            print line.rstrip('\n')
                #error_lines.append(line)
            continue

            ##########must contain url####################
        urls = status.entities['urls']
            #if not urls:
            #   continue

        expand_urls = []
        for url in urls:
            if url['expanded_url']:
                add_url = url['expanded_url'].encode('utf-8')
                expand_urls.append(add_url)
            else:
                add_url = url['url'].encode('utf-8')
		expand_urls.append(add_url)
        parsed_urls = ' '.join(expand_urls)

	##############reply info##################################
        reply_to_id = status.in_reply_to_status_id_str
        reply_to_user = status.in_reply_to_screen_name
        if not reply_to_id:
            reply_to_id = ''
            reply_to_user = ''
        else:
            reply_to_id = str(reply_to_id)
            reply_to_user = str(reply_to_user)

        ###############retweet info###############################
        retweet_count = str(status.retweet_count)
        try:
            retweet_from_id = str(status.retweeted_status.id_str)
            retweet_from_user = str(status.retweeted_status.author.screen_name)
        except:
            retweet_from_id = ''
            retweet_from_user = ''

        ###############author info#################################
        lang = str(status.author.lang)
        status_count = str(status.author.statuses_count)
        followers_count = str(status.author.followers_count)
        location = status.author.location            
	if location:
            location = location.encode('utf-8').replace('|', ' ')
        else:
            location = ''
            ###########################################################

            ###################save the result#######################
        newline = id+'|'+date+'|'+text+'|'+parsed_urls+'|'+user+'|'+location+'|'+lang+'|'+status_count+'|'+followers_count+'|'+ retweet_count+'|'+retweet_from_id+'|'+retweet_from_user+'|'+reply_to_id+'|'+reply_to_user
        newline = newline.replace('\n', '') + '\n'
        #    raw_lines.append(line)
        extended_lines.append(newline)

    fname = error_file.replace('all_err', 'all_err_ext')
    outfile = open(fname, 'w')
    outfile.writelines(extended_lines)
    outfile.close()
    infile.close()

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
    
    #api = twitter_api_oauth_setup()
    #q = 'sciencemag.org'
    #err_file = os.path.join(tweets_dir, q, 'all_err.' + q)
    #parse_error_tweets(api, err_file)
    
main()
    
