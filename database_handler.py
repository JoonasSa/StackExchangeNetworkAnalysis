#!/usr/bin/env python
# coding: utf-8

from collections import defaultdict
from contextlib import suppress
import os
import json
from data_reader import get_stackoverflow_data


def __extract_users(posts_xml):
    '''Counts how many times each user id has posted a question or answer'''
    user_counter = defaultdict(int)
    for post in posts_xml:
        user_id = post.attrib.get('OwnerUserId', post.attrib.get('OwnerDisplayName'))
        user_counter[user_id] += 1
    return user_counter


def __dump_json(data, filepath):
    '''Saves the data into a json file'''
    with open(filepath, 'w') as outfile:
        json.dump(data, outfile)


def remove_user_json(path, filename='users.json'):
    '''Removes the json database. If necessary'''
    with suppress('FileNotFoundError'):
        for dirname in os.listdir(path):
            os.remove(os.path.join(path, dirname, filename))


def prepare_json_databases(path, filename='users.json'):
    '''Per-directory handling of data: requests feature extraction and saving'''
    for dirname in os.listdir(path):
        print('Extracting data from', dirname)
        dirpath = os.path.join(path, dirname)
        filepath_json = os.path.join(dirpath, filename)
        # Skips in case the database already exists
        if os.path.isfile(filepath_json):
            continue
        xml_data = get_stackoverflow_data(dirpath, ['Posts'])
        user_counter = __extract_users(xml_data['Posts'])
        __dump_json(user_counter, filepath_json)


def load_json_database(path, dirname, filename='users.json'):
    '''Handles over the json database file'''
    filepath = os.path.join(path, dirname, filename)
    with open(filepath) as json_file:
        return json.load(json_file)

