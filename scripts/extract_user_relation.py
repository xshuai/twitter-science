#######################################################################################################This script is used to extract##################################################retweeting relationship in tweets########################################################################################################
#coding: utf-8
import parse_tweet
import re

############define some retweeting patterns###############
rt_pat = re.compile(r"rt[: ]*@(\w+)",re.I)#RT retweeting
via_pat = re.compile(r"via[: ]*@(\w+)",re.I)#via retweeting
retweet_pat = re.compile(r"(rt|via|mt|\"|“)[: ]*@(\w+)", re.I)
reply_pat = re.compile(r"^@[\w]+", re.IGNORECASE)#reply 
mention_pat = re.compile(r"@[\w]+", re.IGNORECASE)#mention
#mention_pat = re.compile(r"(?:rt )?@\S+", re.I)
#symbol = '“@(\w+)'.decode('utf-8')
#symbol_pat = re.compile(symbol, flags=re.U)
##########################################################

def extract_retweet_users(tweet, use_meta=False):
    #user_pos = {}
    #rt_users = rt_pat.findall(tweet)
    #via_users = via_pat.findall(tweet)
    #retweet_users = rt_users + via_users
    t = parse_tweet.Tweet(tweet)
    if use_meta:
	#t = parse_tweet.Tweet(tweet)
        retweet_user = t.retweet_from_user
        if retweet_user:
	    retweet_users = [retweet_user]
	else:
	    retweet_users = []
    else:
        symbol_user = retweet_pat.findall(t.text)
        retweet_users = map(lambda x:x[1], symbol_user)

    if retweet_users:
	#print [t.user] + retweet_users
	#print tweet
        return [t.user] + retweet_users
    else:
	return []
    #if retweet_users == []:
    #	return None
    #else:
    #	return retweet_users

def extract_reply_users(tweet, use_meta=False):
    t = parse_tweet.Tweet(tweet)
    reply_users = []
    if use_meta:
	#t = parse_tweet.Tweet(tweet)
	reply_user = t.reply_to_user
	if reply_user:
            reply_users = [reply_user]
    else:
        tt = t.text
        reply_user = reply_pat.findall(tt)
        while reply_user != []:
	    reply_users.append(reply_user[0].lstrip('@'))
	    tt = reply_pat.sub('', tt).lstrip()
	    reply_user = reply_pat.findall(tt)
    #if reply_users == []:
    #	return ''
    #else:
    if reply_users:
	return [t.user] + reply_users
    else:
        return []

def extract_mention_users(tweet):
    t = parse_tweet.Tweet(tweet)
    mention_users = mention_pat.findall(t.text)
    if mention_users == []:
	return []
    else:
	return [t.user] + map(lambda x:x.lstrip('@'), mention_users)

def extract_user_relation(tweet):
    ##########extract tweet author##################
    try:
        t = parse_tweet.Tweet(tweet)
        user = t.user
        text = t.text
    except:
	text = tweet
	user = ''
    ##########extract retweet users##################
    retweet_users = extract_retweet_users(tweet)
    ##########extract all mention users##############
    mention_users = extract_mention_users(tweet)
    ##########extract reply user#####################
    reply_users = extract_reply_users(tweet)
    #print retweet_users
    #print mention_users
    group_user = {}
    group_user['author'] = user
    group_user['retweet'] = retweet_users
    group_user['reply'] = reply_users
    try:
        group_user['mention'] = list(set(mention_users) - set(retweet_users) - set(reply_users))
	#group_user['mention'] = list(set(mention_users) - set(reply_users))
	#if reply_users == []:
	#    group_user['mention'] = mention_users
	#else:
	#    remain_users = []
	#    for user in mention_users:
	#        if user not in reply_users:
#		    remain_users.append(user)
#	    group_user['mention'] = remain_users
    except:
	group_user['mention'] = []
    return group_user
    

    
def test():
    text = "@canhoto RT:@MyScienceCareer \"@article MT @peter: on planning for your post-PhD career: http://t.co/xyGaxJ3j (via @PhD2Published) #PhD"
    #text = '“@NatureNews: “Without a doubt, we have a discovery.”'
    print text
    r1 = extract_retweet_users(text)
    print r1
    r2 = extract_reply_users(text)
    print r2
    r1 = extract_mention_users(text)
    print r1
    r3 = extract_user_relation(text)
    print r3

#test()
#def parse_tweet_user_relation(tweet_file):
     
