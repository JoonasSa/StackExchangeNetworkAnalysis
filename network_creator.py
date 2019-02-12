#!/usr/bin/env python
# coding: utf-8

from itertools import combinations
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import json
import database_handler
from data_reader import get_stackoverflow_data


def page_and_crossposters_network(path):
    filename = 'users.json'
    database_handler.prepare_json_databasis(path, database_handler.__extract_user_count, filename)
    network = defaultdict(list)
    # Each directory represents a site
    for dir1, dir2 in combinations(os.listdir(path), 2):
        users1 = database_handler.load_json_database(path, dir1, filename)
        users2 = database_handler.load_json_database(path, dir2, filename)
        # The weight of the edge is the number of users that have posted in both sites
        weight = len(set(users1) & set(users2))
        network['edges'].append((dir1, dir2, weight))
    network['nodes'] = [site for site in os.listdir(path)]
    return network


## ei toimi vielä!!!
def answers_and_posters_network(path):
    filename = 'answers.json'
    database_handler.prepare_json_databasis(path, database_handler.__extract_answers_as_edges,\
                                                    filename) #, reset=True)
    network = defaultdict(dict)
    for directory in os.listdir(path):
        edges = database_handler.load_json_database(path, directory, filename)
    print(edges)








