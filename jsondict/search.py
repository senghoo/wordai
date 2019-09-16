#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json


with open('dict.json', 'r') as f:
    dictionary = json.load(f)

def search(word):
    try:
        return dictionary[word]
    except:
        return None

def format(item):
    res = "{word}\tStar:{star}\n".format(**item)
    for desc in item['descriptions']:
        res += "\t{description}\n".format(**desc)
        for ex in desc['examples']:
            res += "\t\tEN:\t{en}\n\t\tCN:\t{cn}\n".format(**ex)
        res +="\n"
    return res

def description(word):
    item = search(word)
    if item is None:
        return ""
    return "\n".join([x['description'] for x in item['descriptions']])

def search_string(word):
    res = search(word)
    if res is None:
        return ""
    return format(res)

if __name__ == '__main__':
    res = search(sys.argv[1])
    if res is not None:
        print(format(res))
