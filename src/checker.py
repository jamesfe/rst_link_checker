# -*- coding: utf-8 -*-

import os
import re
import requests
import time

# target_dir = '~/PersCode/finatra/'
target_dir = '~/PersCode/finatra/doc/src/sphinx/user-guide/logging/'
target_ext = 'rst'


class BadThing:
    status_code = 999


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    NC = '\033[0m'


def print_red(thing):
    print('{}{}{}'.format(bcolors.RED, thing, bcolors.NC))


def print_green(thing):
    print('{}{}{}'.format(bcolors.GREEN, thing, bcolors.NC))


def find_target_files(target_dir, target_ext):
    ret_vals = []
    if '~' in target_dir:
        target_dir = os.path.expanduser(target_dir)
    for root, direc, files in os.walk(target_dir):
        for item in files:
            if item.lower().endswith(target_ext):
                ret_vals.append(os.path.join(root, item))
    return ret_vals


def checkline(line):
    """ Return any non-relative links. """
    links = re.findall('<(http.*?)>', line)
    ret_vals = []
    for item in links:
        if '#' in item:
            ret_vals.append(item.split('#')[0])
        else:
            ret_vals.append(item)
    return ret_vals


def extract_links(filename):
    """ Extract links from a file. """
    links = set()
    with open(filename, 'r') as infile:
        for line in infile:
            vals = checkline(line)
            if len(vals) > 0:
                links.update(set(vals))
    return links


def link_in_set_check(link, tgt_set):
    for item in tgt_set:
        if link in item:
            return True
    return False


file_lookup = dict()
dirs = find_target_files(target_dir, target_ext)
for item in dirs:
    print('Scanning {}'.format(item))
    file_lookup[item] = extract_links(item)

all_links = set()
# Aggregate the links so we only ping them once
for key, vals in file_lookup.items():
    all_links = all_links.union(vals)

print('We are going to be checking {} links for validity.'.format(len(all_links)))
link_statuses = []

for item in all_links:
    # TODO: Create a cache file with these results and when they were collected, then read that and compare against a threshold later.
    try:
        req = requests.get(item)
    except:  # NOQA
        req = BadThing()
    if req.status_code != 200:
        print_red('Checked {} with code {}'.format(item, req.status_code))
    else:
        print_green('Checked {} with code {}'.format(item, req.status_code))
    link_statuses.append([req.status_code, item])
    time.sleep(1)

print("\nWhich files are the bad links in?")

for item in link_statuses:
    if item[0] < 200 | item[0] >= 300:
        for k, v in file_lookup.items():
            if link_in_set_check(item[1], v):
                print_red('{} contains bad link to {}'.format(k, item[1]))
