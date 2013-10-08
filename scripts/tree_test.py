#########
import networkx as nx
G = nx.DiGraph()
G.add_edge(1,2)
G.add_edge(2,3)
G.add_edge(2,7)
G.add_edge(3,4)
G.add_edge(3,6)
G.add_edge(4,5)
paths = nx.dfs_successors(G, 1)
print paths.keys()
print paths[1]
print paths[2]
print paths[3]
print paths[4]
