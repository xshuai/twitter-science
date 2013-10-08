######################################################################################################Construct the diffusion network###########################################################################################################
import networkx as nx
import os
cas_dir = "/home/twitterBollen/xshuai/science_social_media/twitter/dat/nature.com/doi_tweets/social_cascade/"

def convert_graph_to_csv(G, cvs_file):
    write_lines = []
    for n, nbrs in G.adjacency_iter():
        for nbr in nbrs.keys():
            newline = n + ',' + nbr + '\n'
            write_lines.append(newline)

    outfile = open(cvs_file, 'w')
    outfile.writelines(write_lines)
    outfile.close()

#def find_diffusion_paths(G):
def generate_graph(cas_file):
    infile = open(cas_file, 'r')
    G = nx.DiGraph()
    for line in infile:
        content = line.rstrip('\n').split()
        nodes = content[1].split(',')
	nodes = map(lambda x:x.lower(), nodes)
        if len(nodes) == 1:###only a single node
            G.add_node(nodes[0])
        else:
            for i in range(len(nodes) - 1):
                node1 = nodes[i]
                node2 = nodes[i+1]
		if (node1, node2) in G.edges():##does not allow reverse propagation
		    continue
                try:
                    G[node2][node1]['weight'] += 1
                except KeyError:
                    G.add_edge(node2, node1, weight=1)
    infile.close()
    return G
    
	    
##############analyze diffusion graph#####################
index = 1
cas_file = os.path.join(cas_dir, str(index) + '.cas')
G = generate_graph(cas_file)
graphs =  nx.weakly_connected_component_subgraphs(G)
sorted_graphs = sorted(graphs, key=lambda x:len(x.nodes()), reverse=True)
convert_graph_to_csv(sorted_graphs[0], 'temp_file')
paths = nx.bfs_successors(G, 'cgseife')
print paths.keys()
print paths['rogerhighfield']
#print paths['berry_k']['trimetilsilyl']

#print paths
