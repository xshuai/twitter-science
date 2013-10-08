#! /usr/bin/python
# coding: utf-8
#######################################################################################################build up retweeting relation#############################################################################################################
from parse_tweet import *
import sys, os
from extract_user_relation import *
import networkx as nx
####################################################

class RetweetGraph:
    """retweet graph"""
    def __init__(self, graph_file):
	f = open(graph_file, 'r')
        G = nx.read_gpickle(f)
        f.close()
        self.graph = G

    def export_to_format(self, format_file, format="csv"):
	G = self.graph
	if format == 'csv':
	    nx.write_edgelist(G, format_file, data=False)

    def find_largest_component(self):
	G = self.graph
	list_Graphs = nx.weakly_connected_component_subgraphs(G)
	max_component = list_Graphs[0]
	for g in list_Graphs:
    	    if nx.number_of_nodes(g) > nx.number_of_nodes(max_component):
                max_component = g

        return  max_component
    
    #def draw_graph(self, use_largest=True):
    # 	G = self.graph
def convert_graph_to_csv(G, cvs_file):
    write_lines = []
    for n, nbrs in G.adjacency_iter():
        for nbr in nbrs.keys():
            newline = n + ',' + nbr + '\n'
            write_lines.append(newline)

    outfile = open(cvs_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

def add_edge_to_graph(G, tweet, method='retweet'):
    #t = Tweet(tweet)
    #author = t.user
    #author = 'a'
    relation_users = []
    if method == 'retweet':
        relation_users = extract_retweet_users(tweet, use_meta=True)
    if relation_users:###find retweet users#####
        nodes = relation_users
	#if len(nodes) < 2:
	#    return
        for i in range(len(nodes) - 1):
            node1 = nodes[i]
            node2 = nodes[i+1]
            if node1 == node2 or (node1, node2) in G.edges():##does not allow reverse propagation or self propagation
                continue
            try:
                G[node2][node1]['weight'] += 1
            except KeyError:
                G.add_edge(node2, node1, weight=1)

def gen_retweet_graph(tweet_file, graph_dir, tweet_type='arxiv', use_id=None):
    """generate a retweet graph"""
    infile = open(tweet_file, 'r')
    if not use_id:
	G = nx.DiGraph()
    index = 0
    for line in infile:
	content = line.rstrip('\n').split('\t')
	id = content[0]
	freq = int(content[1])
	tweets = content[2].split('&&&')
	if not use_id:#####generate all retweet network##########
	    for tweet in tweets:
		try:
		    add_edge_to_graph(G, tweet, method='retweet')
		except:
		    print tweet
		    exit(0)
		
			    
	elif use_id == 'total':
	    if freq < 5:####filter low mentioned ids
		continue
	    print 'current id:', id
	    G = nx.DiGraph()
            for tweet in tweets:
                add_edge_to_graph(G, tweet, method='retweet')
	    gpath = os.path.join(graph_dir, id + '.gpickle')
	    nx.write_gpickle(G, gpath)
	    #csv_file = os.path.join(graph_dir, tweet_type + '.csv')
            #mG = g.find_largest_component()
            #nx.write_edgelist(G, csv_file, data=False)
	    
	else:
	    if id == use_id:
	        G = nx.DiGraph()
	        for tweet in tweets:
		    add_edge_to_graph(G, tweet, method='retweet')
		gpath = os.path.join(graph_dir, id + '.gpickle')
                nx.write_gpickle(G, gpath)  
	index += 1
	if not (index % 1000):
	    print index
    if not use_id:
	gpath = os.path.join(graph_dir, tweet_type + '.gpickle')
        nx.write_gpickle(G, gpath)
	print len(G.nodes())
	print len(G.edges())

def main():
    tweet_type = parse_args()
    tweet_file = os.path.join(dat_dir, tweet_type, 'id_tweets.txt')
    graph_dir = os.path.join(dat_dir, tweet_type, 'retweet_graphs')
    use_id = 'total'
    gen_retweet_graph(tweet_file, graph_dir, tweet_type, use_id)
    for r, d, files in os.walk(graph_dir):
	break
    for f in files:
	if '.gpickle' in f:
	    gpath = os.path.join(r, f)
            g = RetweetGraph(gpath)
    	    csv_file = os.path.join(graph_dir, f.rstrip('.gpickle') + '.csv')
    	    #G = g.find_largest_component()
    	    #nx.write_edgelist(G, csv_file, data=False)
    	    g.export_to_format(csv_file)
	    
if __name__ == "__main__":
    main() 
			

		
	     

      
