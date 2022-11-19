# TEST DATA
# Creates Random Generated Graph with single clique
# ---------------------------------------------------------
# N = total number of nodes in graph (default 75)
# Cn = number of nodes in clique (default 12)
# Cp = probability node in clique is connected to other node in clique (default 0.35)
# Op = probability node NOT in clique is connected to other node NOT in clique (default 0.1)
# q = probability node in clique is connected to other node NOT in clique (default 0.1)
# s = seed for reproducibility (default 3)
# clique = graph of clique nodes and edges
# outer = graph of outer nodes and edges
# combined = combined graph of clique and edges (with random edges base on q)
# clique_nodes = ground_truth list of clique nodes
# outer_nodes = ground_truth list of outer nodes



from random import random
from random import seed
import pandas as pd
import networkx as nx
import numpy as np
from itertools import product
import pickle
import json


def create_rand_graphs(N, Cn, Cp, Op, q, s):
    # make clique
    cliq_graph = nx.gnp_random_graph(Cn, Cp, seed=s) # red
    # make outside of clique
    out_graph = nx.gnp_random_graph(N-Cn, Op, seed=s) # blue

    # save seperate graphs as files
    pickle.dump(cliq_graph, open('data/test/raw/cliq_graph.pickle', 'wb'))
    pickle.dump(out_graph, open('data/test/raw/out_graph.pickle', 'wb'))





def create_combined(N, Cn, Cp, Op, q, s):
    # load in seperate graphs
    clique = pickle.load(open('data/test/raw/cliq_graph.pickle', 'rb'))
    outer = pickle.load(open('data/test/raw/out_graph.pickle', 'rb'))
    
    
    clique_nodes = clique.nodes()
    
    # rename the outer nodes
    outer_dict_relabel = dict(zip(range(N-Cn), range(Cn, N)))
    nx.relabel_nodes(outer, outer_dict_relabel, False)
    outer_nodes = outer.nodes()
    
    # create ground truth JSON
    ground_truths = {
        "clique_nodes": clique_nodes,
        "outer_nodes": outer_nodes
    }
    
    with open("data/test/temp/ground_truth.json", "w") as outfile:
        json.dump(dictionary, outfile)
    
    
    # create and save combined graph
    combined = nx.Graph()
    combined.add_nodes_from(clique_nodes)
    combined.add_edges_from(clique.edges())
    combined.add_nodes_from(outer_nodes)
    combined.add_edges_from(outer.edges())
    
    pickle.dump(combined, open('data/test/raw/combined_separated.pickle', 'wb'))
    

    





def create_combined_edges(N, Cn, Cp, Op, q, s):
    combined = pickle.load(open('data/test/raw/combined_separated.pickle', 'rb'))
    
    with open('data/test/temp/ground_truth.json', 'r') as openfile:
        ground_truth = json.load(openfile)
    
    seed(s)
    combined.add_edges_from([ (u, v) for u, v in product(ground_truth['clique_nodes'], ground_truth['outer_nodes']) if random() < q ])
    pickle.dump(combined, open('data/test/temp/combined.pickle', 'wb'))






def plot_graph(combined, clique_nodes, outer_nodes):
    combined = pickle.load(open('data/test/temp/combined.pickle', 'rb'))
    
    with open('data/test/temp/ground_truth.json', 'r') as openfile:
        ground_truth = json.load(openfile)
    
    
    pos = nx.spring_layout(combined)
    
    nx.draw_networkx_nodes(combined, pos=pos, nodelist=ground_truth['clique_nodes'], node_color='r', node_size=50)
    nx.draw_networkx_nodes(combined, pos=pos, nodelist=ground_truth['outer_nodes'], node_color='b', node_size=50)
    nx.draw_networkx_edges(combined, pos=pos)
    return plt.show() 
    