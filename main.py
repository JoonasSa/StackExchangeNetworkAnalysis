#!/usr/bin/env python
# coding: utf-8

from networkx import networkx as nx
from collections import defaultdict
import matplotlib.pyplot as plt
import os
from datetime import datetime as dt
from data_reader import get_stackoverflow_data
from fix_edge_ids import fix_graphml_edges

BASE_PATH = 'data'

START_DATE = '2017-01-01'

MDG = nx.MultiDiGraph()

edges = dict()
missing_users = set()
nodes = defaultdict(dict)
# The second value indicates if it's numerical
wanted_user_attributes = [('Reputation', True), ('UpVotes', True), ('DownVotes', True)]
user_question_counter = defaultdict(int)

def get_posts_from_last_five_years(posts):
    # post creation dates are in form 2011-08-30T21:12:34.090 but lets only Y-m-d
    def filter_func(post):
        date = post.attrib.get('CreationDate')[:10]
        return dt.strptime(START_DATE, "%Y-%m-%d") < dt.strptime(date, "%Y-%m-%d")

    return list(filter(filter_func, posts))

for directory in os.listdir(BASE_PATH):
    print('Searching', directory)
    question_asker = dict()
    users = defaultdict(dict)
    user_row_ids = dict()
    xml_data = get_stackoverflow_data(os.path.join(BASE_PATH, directory), ['Posts', 'Users'])

    for user in xml_data['Users']:
        account_id = user.attrib.get('AccountId', user.attrib['DisplayName'])
        row_id = user.attrib.get('Id')
        user_row_ids[row_id] = account_id
        # Wanted features
        for attribute, numerical in wanted_user_attributes:
            fetched_attribute = user.attrib.get(attribute)
            if numerical:
                fetched_attribute = int(fetched_attribute)
            users[account_id][attribute] = fetched_attribute

    print(len(xml_data['Posts']))
    xml_data['Posts'] = get_posts_from_last_five_years(xml_data['Posts'])
    print(len(xml_data['Posts']))

    for row in xml_data['Posts']:
        # PostTypeId == 1 indicates that it's a question
        if row.attrib['PostTypeId'] == '1':
            user_id = user_row_ids.get(row.attrib.get('OwnerUserId')) or row.attrib.get('OwnerDisplayName')
            question_asker[row.attrib['Id']] = user_id
            user_question_counter[user_id] += 1

    # There are cases of answers with a lower Id than the question, hence one further loop
    for row in xml_data['Posts']:
        # PostTypeId == 2 is an answer
        if row.attrib['PostTypeId'] == '2':
            # question_asker might not exist if only posts from past X years were used
            if not row.attrib['ParentId'] in question_asker:
                continue
            parent_user_id = question_asker[row.attrib['ParentId']]
            # fetches the id of the OP and links them
            user_id = user_row_ids.get(row.attrib.get('OwnerUserId')) or row.attrib.get('OwnerDisplayName')
            creation_date = row.attrib.get('CreationDate')
            for user in user_id, parent_user_id:
                nodes[user] = users.get(user)

            # setdefault seems to be faster than defaultdict in this case
            edges.setdefault((user_id, parent_user_id), dict())[directory] = []
            edges[(user_id, parent_user_id)][directory].append(creation_date)

    # This will be in the format:
    #   (answerer, questioner, {'site': <name_of_the_site>, 'weight': <number_of_answers>}add_edges_from)
    MDG.add_edges_from([(*k, {'site':k2, 'weight':len(v2)}) for k, v in edges.items() for k2, v2 in v.items()])

    MDG.add_nodes_from(nodes)
    for node in MDG.nodes:
        MDG.nodes[node]['questions'] = user_question_counter[node]

nx.write_graphml(MDG, f"graphml/combination.graphml")
fix_graphml_edges()

#plt.figure(1, figsize=(16,16))
#nx.draw(G, with_labels=True, node_color='skyblue', width=weights)
#plt.show()