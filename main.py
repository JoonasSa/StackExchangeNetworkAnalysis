#!/usr/bin/env python
# coding: utf-8

from networkx import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import scipy
import os
from data_reader import get_stackoverflow_data

BASE_PATH = 'data'

G = nx.MultiDiGraph()

edges = dict()
missing_users = set()
nodes = defaultdict(dict)
wanted_user_attributes = ['Reputation', 'UpVotes', 'DownVotes']

for directory in os.listdir(BASE_PATH):
    print('Searching', directory)
    posts_dict = dict()
    users = defaultdict(dict)
    user_row_ids = dict()
    xml_data = get_stackoverflow_data(os.path.join(BASE_PATH, directory), ['Posts', 'Users'])
    for user in xml_data['Users']:
        account_id = user.attrib.get('AccountId', user.attrib['DisplayName'])
        row_id = user.attrib.get('Id')
        user_row_ids[row_id] = account_id
        # Wanted features
        for attribute in wanted_user_attributes:
            fetched_attribute = user.attrib.get(attribute)
            users[account_id][attribute] = fetched_attribute
    for row in xml_data['Posts']:
        # PostTypeId == 1 indicates that it's a question
        if row.attrib['PostTypeId'] == '1':
            user_id = user_row_ids.get(row.attrib.get('OwnerUserId')) or row.attrib.get('OwnerDisplayName')
            posts_dict[row.attrib['Id']] = user_id
    # There are cases of answers with a lower Id than the question, hence one further loop
    for row in xml_data['Posts']:
        # PostTypeId == 2 is an answer
        if row.attrib['PostTypeId'] == '2':
            # fetches the id of the OP and links them
            user_id = user_row_ids.get(row.attrib.get('OwnerUserId')) or row.attrib.get('OwnerDisplayName')
            parent_user_id = posts_dict[row.attrib['ParentId']]
            creation_date = row.attrib.get('CreationDate')
            for user in user_id, parent_user_id:
                nodes[user] = users.get(user)

            # setdefault seems to be faster than defaultdict in this case
            edges.setdefault((user_id, parent_user_id), dict())[directory] = []
            edges[(user_id, parent_user_id)][directory].append(creation_date)


#nodes.update({user: None for user in missing_users})
G.add_edges_from([(*k, {'site':k2, 'weight':len(v2)}) for k, v in edges.items() for k2, v2 in v.items()])

G.add_nodes_from(nodes)

#plt.figure(1, figsize=(16,16))
#nx.draw(G, with_labels=True, node_color='skyblue', width=weights)
#plt.show()
