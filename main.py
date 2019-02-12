#!/usr/bin/env python
# coding: utf-8

from networkx import networkx as nx
from itertools import combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import scipy
import os
import json
import network_creator
#from data_reader import get_stackoverflow_data

BASE_PATH = 'data'

#G=nx.Graph()
#g_network = network_creator.page_and_crossposters_network(BASE_PATH)
#G.add_weighted_edges_from(g_network['edges'])
#G.add_nodes_from(g_network['nodes'])
## Drawing edge thickness according to width
#plt.figure(1, figsize=(16,16))
#raw_weights = [w/500 for w in nx.get_edge_attributes(G, 'weight').values()]
#max_weight = max(raw_weights)
#weights = [w*10/max_weight for w in raw_weights]
#nx.draw(G, with_labels=True, node_color='skyblue', width=weights)
#plt.show()

#H=nx.Graph()
#h_network = network_creator.answers_and_posters_network(BASE_PATH)
