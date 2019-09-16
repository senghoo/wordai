# -*- coding: utf-8 -*-

import os
import json
from itertools import chain
from translate.storage.tmx import tmxfile

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def data_file(filename):
    return os.path.join(DATA_DIR, filename)

def load_dict():
    with open(data_file("dict.json"), "r") as f:
        return json.load(f)


def load_sentence(*typ):
    files = {
        'talks': ['日常口语_20190906111009_1.tmx', '日常口语_20190906111009_2.tmx', '日常口语_20190906111009_3.tmx'],
        'dictexams': ['词典例句汇集1.tmx', '词典例句汇集3.tmx', '词典例句汇集5.tmx', '词典例句汇集7.tmx',
                      '词典例句汇集2.tmx', '词典例句汇集4.tmx', '词典例句汇集6.tmx', '词典例句汇集8.tmx']
    }
    iters = {}
    for t, fs in files.items():
        if len(typ) == 0 or t in typ:
            type_iterns = []
            for fname in fs:
                with open(data_file(fname), 'rb') as fin:
                    tmx = tmxfile(fin, 'en', 'cn')
                    type_iterns.append(tmx.unit_iter())
            iters[t] = chain(*type_iterns)
    return iters
