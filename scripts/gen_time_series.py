####################################################################################################generate time series data###################################################################################################################
###########import modules################
import sys, os
from parse_tweet import *
from datetime import *
########################################

def aggregate_date_frequncy(date_file, tweet_type='all'):
    """aggregate tweet mention frequency for different journal"""
    date_freq = {}
    if tweet_type == 'all':
	all_journals = ['arxiv', 'plos', 'pnas.org', 'sciencemag.org', 'nature.com']
	for journal in all_journals:
	    print journal
	    fname = os.path.join(dat_dir, journal, 'id_dates.txt')
	    infile = open(fname, 'r')
	    for line in infile:
		content = line.rstrip('\n').split('\t')
		dates = content[-1].split('|')
		for date in dates:
		    d, f = date.split(',')
		    try:
			date_freq[d] += int(f)
		    except KeyError:
			date_freq[d] = int(f)
	    infile.close()
    else:
	fname = os.path.join(dat_dir, journal, 'id_dates.txt')
	print fname
	infile = open(fname, 'r')
        for line in infile:
            content = line.rstrip('\n').split('\t')
            dates = content[-1].split('|')
            for date in dates:
                d, f = date.split(',')
                try:
                    date_freq[d] += int(f)
                except KeyError:
                    date_freq[d] = int(f)
        infile.close()

    write_lines = []
    sorted_dates = sorted(date_freq.items(), key=lambda x:datetime.strptime(x[0], "%Y-%m-%d"))
    for date, freq in sorted_dates:
	newline = date + '\t' + str(freq) + '\n' 
	write_lines.append(newline)
    outfile = open(date_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

def count_date_frequency(date_file, tweet_type='all'):
    """count date frequency based on raw tweets file"""
    date_freq = {}
    if tweet_type == 'all':
        all_journals = ['arxiv', 'plos', 'pnas.org', 'sciencemag.org', 'nature.com']
        for journal in all_journals:
            print journal
            fname = os.path.join(dat_dir, journal, 'ext_tweets.txt')
            infile = open(fname, 'r')
	    for line in infile:
		try:
		    tweet = Tweet(line)
		except:
		    continue
		date = tweet.date.split('T')[0]
		try:
		    date_freq[date] += 1
		except KeyError:
		    date_freq[date] = 1
	    infile.close()
    else:
	fname = os.path.join(dat_dir, tweet_type, 'ext_tweets.txt')
	print fname
        infile = open(fname, 'r')
        for line in infile:
	    try:
                tweet = Tweet(line)
	    except:
		continue
            date = tweet.date
            try:
                date_freq[date] += 1
            except KeyError:
                date_freq[date] = 1
        infile.close()

    write_lines = []
    sorted_dates = sorted(date_freq.items(), key=lambda x:datetime.strptime(x[0], "%Y-%m-%d"))
    for date, freq in sorted_dates:
        newline = date + '\t' + str(freq) + '\n'
        write_lines.append(newline)
    outfile = open(date_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

def main():
    tweet_type = parse_args()
    #if tweet_type == 'all':
    date_file = os.path.join(dat_dir, 'date_freq1.txt')
    count_date_frequency(date_file)

main()
