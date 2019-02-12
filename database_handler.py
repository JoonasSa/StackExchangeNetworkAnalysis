#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
from contextlib import suppress
import os
import json
from data_reader import get_stackoverflow_data


def __extract_user_count(posts_xml):
    '''Counts how many times each user id has posted a question or answer'''
    user_counter = defaultdict(int)
    for post in posts_xml:
        user_id = post.attrib.get('OwnerUserId', post.attrib.get('OwnerDisplayName'))
        user_counter[user_id] += 1
    return user_counter

def __extract_answers_as_edges(posts_xml):
    posts_dict = dict()
    edges = defaultdict(list)
    for row in posts_xml:
        user_id = row.attrib.get('OwnerUserId', row.attrib.get('OwnerDisplayName'))
        # PostTypeId == 1 indicates that it's a question
        if row.attrib['PostTypeId'] == '1':
            posts_dict[row.attrib['Id']] = user_id
        # otherwise it's an answer to an existing question
        elif row.attrib['PostTypeId'] == '2':
            # fetches the id of the OP and links them
            parent_user_id = posts_dict.get(row.attrib['ParentId'])
            creation_date = row.attrib.get('CreationDate')
            if not user_id or not parent_user_id:
                continue
            edges[','.join((user_id, parent_user_id))].append(creation_date)
    return edges


def __dump_json(data, filepath):
    '''Saves the data into a json file'''
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)


def __remove_user_json(path, filename='users.json'):
    '''Removes the json database'''
    with suppress('FileNotFoundError'):
        for dirname in os.listdir(path):
            os.remove(os.path.join(path, dirname, filename))


def prepare_json_databasis(path, function, filename, reset=False):
    '''Per-directory handling of data: requests feature extraction and saving
       Resets databaset if _reset_ is True'''
    if reset:
        __remove_user_json(path, filename)
    for dirname in os.listdir(path):
        print('Extracting data from', dirname)
        dirpath = os.path.join(path, dirname)
        filepath_json = os.path.join(dirpath, filename)
        # Skips in case the database already exists
        if os.path.isfile(filepath_json):
            continue
        xml_data = get_stackoverflow_data(dirpath, ['Posts'])
        network = function(xml_data['Posts'])
        __dump_json(network, filepath_json)


def load_json_database(path, dirname, filename='users.json'):
    '''Handles over the json database file'''
    filepath = os.path.join(path, dirname, filename)
    with open(filepath) as json_file:
        return json.load(json_file)

