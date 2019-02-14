#!/usr/bin/env python
# coding: utf-8

from networkx import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import scipy
import os
from data_reader import get_stackoverflow_data

BASE_PATH = 'data'

G = nx.Graph()

edges = dict()
missing_users = set()
nodes = defaultdict(dict)
for directory in os.listdir(BASE_PATH):
    print('Searching', directory)
    posts_dict = dict()
    users = defaultdict(dict)
    xml_data = get_stackoverflow_data(os.path.join(BASE_PATH, directory), ['Posts', 'Users'])
    for user in xml_data['Users']:
        account_id = user.attrib.get('AccountId', user.attrib.get('DisplayName'))
        # Wanted features
        reputation = user.attrib.get('Reputation')
        users[account_id]['Reputation'] = reputation
    for found_user in missing_users & set(users):
        nodes[found_user] = users[found_user]
        missing_users.remove(found_user)
    for row in xml_data['Posts']:
        user_id = row.attrib.get('OwnerUserId', row.attrib.get('OwnerDisplayName'))
        # PostTypeId == 1 indicates that it's a question
        if row.attrib['PostTypeId'] == '1':
            posts_dict[row.attrib['Id']] = user_id
        # otherwise it's an answer to an existing question
        elif row.attrib['PostTypeId'] == '2':
            # fetches the id of the OP and links them
            parent_user_id = posts_dict.get(row.attrib['ParentId'])
            creation_date = row.attrib.get('CreationDate')
            for user in user_id, parent_user_id:
                if not user:
                    break
                try:
                    # Checking the specific value in order not to trigger defaultdict
                    nodes[user]['Reputation'] = users[user]['Reputation']
                except KeyError:
                    if user not in nodes:
                        missing_users.add(user)
            # in case both user ids are known, add an edge
            else:
                # setdefault seems to be faster than defaultdict in this case
                edges.setdefault((user_id, parent_user_id), dict())[directory] = []
                edges[(user_id, parent_user_id)][directory].append(creation_date)


nodes.update({user: None for user in missing_users})
G.add_edges_from([(k[0], k[1], {k2:','.join(i for i in v2)}) for k, v in edges.items() for k2, v2 in v.items()])
#G.add_edges_from(edges)
G.add_nodes_from(nodes)

#plt.figure(1, figsize=(16,16))
#nx.draw(G, with_labels=True, node_color='skyblue', width=weights)
#plt.show()
