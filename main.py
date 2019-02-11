#!/usr/bin/env python
# coding: utf-8

from networkx import networkx as nx
from itertools import combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import scipy
import os
import json
import database_handler
#from data_reader import get_stackoverflow_data

BASE_PATH = 'data'

G=nx.Graph()

#xml_dict = get_stackoverflow_data(f"{BASE_PATH}/bitcoin")

# example on how to use the xml
#for row in xml_dict['Users'][:2]:
#    # row objects have tag & attrib
#    print(row.tag, row.attrib)

# Extraction of features into individual json files for each directory
database_handler.prepare_json_databases(BASE_PATH)

G.add_nodes_from(os.listdir(BASE_PATH))

edges = defaultdict(lambda:defaultdict(int))
# Each directory represents a site
for dir1, dir2 in combinations(os.listdir(BASE_PATH), 2):
    users1 = database_handler.load_json_database(BASE_PATH, dir1)
    users2 = database_handler.load_json_database(BASE_PATH, dir2)
    # The weight of the edge is the number of users that have posted in both sites
    for user in set(users1).intersection(set(users2)):
        edges[(dir1, dir2)]['weight'] += 1
# Networkx doesn't seem to handle defaultdicts, hence the following generator
G.add_weighted_edges_from((k[0], k[1], v['weight']) for k, v in edges.items())

# Drawing edge thickness according to width
plt.figure(1, figsize=(12,12))
weights = [G[i][j]['weight']/500 for i, j in edges]
nx.draw(G, with_labels=True, node_color='skyblue', width=weights)
plt.show()
