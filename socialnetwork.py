# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 14:49:44 2020

@author: feris
"""

from twitter import *
import networkx as nx
import json
import os

# Clear screen
os.system('cls' if os.name=='nt' else 'clear')

graph=nx.DiGraph()

print ""
print "....................................................."
print "RT NETWORK OF AN HASHTAG"
print ""	

hashtag = "#opendesign"

# Log in
OAUTH_TOKEN = 'e5E1w5mimsnmqf4gRM2RJMHwY'
OAUTH_SECRET = 'tQYWigKTckslEBjg0txbvuysYzvXC6e9Tqc3KQaats0GBdTk8n'
CONSUMER_KEY = '251485653-hWoRe8xmHq6mvsLBZlJv5gXEUx6idi3UDoNMdwJm'
CONSUMER_SECRET = 'TulGSPMMfewNj1dbKPdbUY5XlJQnLsuwb4YodGeixSRDf'

auth = OAuth(OAUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
twitter = Twitter(auth = auth)

# search
# https://dev.twitter.com/docs/api/1.1/get/search/tweets
query = twitter.search.tweets(q=hashtag, count=100)

# Debug line
#print json.dumps(query, sort_keys=True, indent=4)

# Print results
print "Search complete (%f seconds)" % (query["search_metadata"]["completed_in"])
print "Found",len(query["statuses"]),"results."

# Get results and find retweets and mentions
for result in query["statuses"]:
	print ""
	print "Tweet:",result["text"]
	print "By user:",result["user"]["name"]
	if len(result["entities"]["user_mentions"]) != 0:
		print "Mentions:"
		for i in result["entities"]["user_mentions"]:
			print " - by",i["screen_name"]
			graph.add_edge(i["screen_name"],result["user"]["name"])
	if "retweeted_status" in result:
		if len(result["retweeted_status"]["entities"]["user_mentions"]) != 0:
			print "Retweets:"
			for i in result["retweeted_status"]["entities"]["user_mentions"]:
				print " - by",i["screen_name"]
				graph.add_edge(i["screen_name"],result["user"]["name"])
	else:
		pass
	
# Save graph
print ""
print "The network of RT of the hashtag was analyzed succesfully."
print ""
print "Saving the file as "+hashtag+"-rt-network.gexf..."
nx.write_gexf(graph, hashtag+"-rt-network.gexf")