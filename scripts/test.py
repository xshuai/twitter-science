# coding: utf-8
import parse_tweet
tweet_line = "246876853086867456|2012-09-15T07:43:23|RT @grahamfarmelo: Astronomers vote unanimously to fix their unit, the Earth-Sun distance, to be precisely 149,597,870,700 metres: http: ...||shantideva77|Valencia|en|2700|299|8|246711424062222336|grahamfarmelo||"
print tweet_line.rstrip('\n').split('|')
tweet = parse_tweet.Tweet(tweet_line)
print tweet.id
print tweet.date
print tweet.text
print tweet.parsed_urls
print tweet.location
