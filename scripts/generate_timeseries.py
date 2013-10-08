#!/usr/bin/python
#######################################################################################################aggregate time serios for doi############################################################################################################
import parse_tweet

root = "/home/twitterBollen/xshuai/science_social_media/twitter/"
doi_file = root + "dat/" + "nature.com/" + "parsed_nature_urls.doi" 
tweet_file = root + "dat/" + "nature.com/" + "ext_tweets.txt"
url_doi = {}
doi_date = {}
doi_tweets = {}
def gen_url_doi_dict(doi_file):
    infile = open(doi_file, 'r')
    for line in infile:
	content = line.split()
	url = content[0]
	doi = content[-1]
	url_doi[url] = doi
	if 'http' not in url:
	    print line
    infile.close()

def extract_urls(tweet_file):
    infile = open(tweet_file, 'r')
    for line in infile:
        try:
            tweet = parse_tweet.Tweet(line)
        except:
            print 'error!'
            print line
            continue

        if not tweet.parsed_urls:
            print line
            continue

        find_urls = tweet.parsed_urls.split()
        date, time = tweet.date.split('T')
	datetime = date + ' ' + time[:2] + ':00:00' 
        for url in find_urls:
            if not url.startswith("http"):
                url = "http://" + url
            try:
                doi = url_doi[url]
		try:
		    doi_date[doi].append(datetime)
		except KeyError:
		    doi_date[doi] = [datetime]
		try:
		    doi_tweets[doi].append(line.rstrip('\n'))
		except KeyError:
		    doi_tweets[doi] = [line.rstrip('\n')]
            except KeyError:
                pass

def output(doi_date_file, doi_tweet_file):
    write_lines = []
    sorted_doi_date = sorted(doi_date.items(), key=lambda x:len(x[1]), reverse=True)
    for doi, date in sorted_doi_date:
	newline = doi + '\t' + str(len(date)) + '\t' + '|'.join(date) + '\n'
	write_lines.append(newline)
    outfile = open(doi_date_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

    write_lines = []
    sorted_doi_tweets = sorted(doi_tweets.items(), key=lambda x:len(x[1]), reverse=True)
    for doi, tweet in sorted_doi_tweets:
	#tweet = tweet.replace('\t', ' ')
        newline = doi + '\t' + str(len(tweet)) + '\t' + '&&&'.join(tweet).replace('\t', ' ') + '\n'
        write_lines.append(newline)
    outfile = open(doi_tweet_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()


	
def main():
    gen_url_doi_dict(doi_file)
    extract_urls(tweet_file)
    doi_date_file = root + "dat/" + "nature.com/" + "doi_timeseries.txt"
    doi_tweet_file = root + "dat/" + "nature.com/" + "doi_tweets.txt"
    output(doi_date_file, doi_tweet_file)
main()
