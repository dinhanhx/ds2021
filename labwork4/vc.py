# (^._.^)ﾉ Author: Vu Dinh Anh
# vc = verbum comitem = word count

import pprint
import sys
import os

def _map(file):
    word_map = []
    with open(file, 'r') as f:
        for line in f:
            words = line.strip().split()
            word_map += [(word, 1) for word in words]  
    return word_map

def _sort(word_map):
    word_map.sort(key = lambda word: word[0])
    return word_map

def _reduce(word_map):
    word = None
    cur_word = None
    cur_count = 0
    reduced_word_map = []

    for word, count in word_map:
        if cur_word == word:
            cur_count += count
        else:
            if cur_word is not None:
                reduced_word_map += [(cur_word, cur_count)]
            cur_word = word
            cur_count = count

    if cur_word == word:
        reduced_word_map += [(cur_word, cur_count)]

    return reduced_word_map

def map_sort_reduce(file):
    return _reduce(_sort(_map(file)))

if __name__ == '__main__':
    file = sys.argv[1]
    if not os.path.isfile(file):
        print('File not found')
    else:
        pprint.pprint(map_sort_reduce(file))
