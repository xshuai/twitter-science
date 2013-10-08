import datetime
from tweepy import *
import time
import urllib, simplejson
query = ['plos','arxiv','nature.com','sciencemag.org']
since_id = {'sciencemag.org':0,'nature.com':0,'arxiv':142763321249107970, 'plos':142672894063951872}#initial values
delay_days = 1
while True: #collect tweets every day
    ################################################################
    for q in query:
        ################do api rating limit status check################
        api_status = urllib.urlopen('http://api.twitter.com/1/account/rate_limit_status.json')
        f = api_status.read()
        d = simplejson.loads(f)
        api_status.close()
        remain = d['remaining_hits']
        if remain < 150:
            print 'sorry, remain', remain, 'need to wait one hour'
            time.sleep(3600)
        ################################################################

	##################first step, collect raw tweets using search API###############
        write_lines = []
        page = 1
        while True:
            results = api.search(q='"'+q+'"',page=page,rpp=150,since_id=since_id[q])
            if results:
                for result in results:
                    tweet = result.text.encode('utf-8')
                    tweet = tweet.replace('\n', ' ')
                    tweet = tweet.replace('\r', ' ')
                    tweet = tweet.replace('\r\n', ' ')
                    date = result.created_at.isoformat()
                    id = str(result.id_str)
                    user = str(result.from_user)
                    newline = id+'\t'+ date+'\t' + user + '\t'+ tweet + '\n'
                    write_lines.append(newline)
            else:
       # All done
                break
           # print page
            if page >= 15:
                break
            page += 1  # next page
    
	#since_id = id##record the last id
        print q, date
        print 'total items:',len(write_lines)
           # outfile = open(date+'_raw.'+q, 'w')
           # outfile.writelines(write_lines)
	   # outfile.close()

	##################second step, further collect metadata using status API#################
        extended_lines = []
        raw_lines = []
        error_lines = []
        index = 0
	################################################################
        for line in write_lines:
            content = line.rstrip('\n').split('\t')
            id = content[0]
            if index == 0:############update the most recent id#
                since_id[q] = id
            date = content[1]
            user = content[2]
            text = content[3]

            ############check api rating limit###########
	    index += 1
	    if not (index%150):
                print 'parsed',index,'waiting...'
                time.sleep(3600)##wait for an hour
	    #############################################

	    #########begin to parse tweets status#################
	    try:
	        status = api.get_status(int(id),include_entities=True)
	    except:
       	   	print line.rstrip('\n')
	   	error_lines.append(line)
	   	continue

	    ##########must contain url####################
    	    urls = status.entities['urls']
            if not urls:
        	continue

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
		location = location.encode('utf-8')
	    else:
		location = ''
	    ###########################################################
	
	    ###################save the result#######################		
   	    newline = id+'|'+date+'|'+text+'|'+parsed_urls+'|'+user+'|'+location+'|'+lang+'|'+status_count+'|'+followers_count+'|'+ retweet_count+'|'+retweet_from_id+'|'+retweet_from_user+'|'+reply_to_id+'|'+reply_to_user+'\n'
	    raw_lines.append(line)
	    extended_lines.append(newline)

	#############################third step, write to files###################################
	outfile = open('./tweets/'+q+'/'+date+'_raw.'+q,'w')
	outfile.writelines(raw_lines)
	outfile.close()

	outfile = open('./tweets/'+q+'/'+date+'_ext.'+q, 'w')
	outfile.writelines(extended_lines)
	outfile.close()

	if error_lines:
	    outfile = open('./tweets/'+q+'/'+date+'_err.'+q, 'w')
            outfile.writelines(error_lines)
            outfile.close()
	#print 'wait for next query...'
    	#time.sleep(3600)
    ##################wait for another process of search and parse####################################
    print 'waiting to collect tweets next time....'
    time.sleep(delay_days*3600*24)
	
