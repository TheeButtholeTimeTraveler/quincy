#!/usr/bin/python3

# quincy: specify a target word then find top n words from
# a dictionary that are closest using Levenshtein distance

import argparse, heapq, string, sys, textwrap
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


parser = argparse.ArgumentParser(description = 'quincy: specify a target word then find the top n words from a\n\
        dictionary that are closest using Levenshtein distance',
        usage = 'python3 %(prog)s [-h] targetword [-d DICTIONARY] [-n NUMWORDS] [-p] [-l] [-s] [-v]',
        formatter_class = argparse.RawTextHelpFormatter)

parser.add_argument('targetword', metavar = 'targetword', type = str, nargs = '+',
                    help = 'target word to analyze')

parser.add_argument('-d', '--dictionary', action = 'store', dest = 'dictionary',
                    default = 'words.txt', help = 'dictionary of words to compare, default words.txt', type = str)

parser.add_argument('-n', '--number', action = 'store', dest = 'numwords',
                    default = 10, help = 'number of matches to return, default 10', type = int)

parser.add_argument('-l', '--lower', action = 'store_true', default = False,
                    dest = 'lower',
                    help = 'convert dictionary to lowercase before analysis')

parser.add_argument('-s', '--strip', action = 'store_true', default = False,
                    dest = 'strip',
                    help = 'strip punctuation from dictionary before analysis')

parser.add_argument('-v', '--verbose', action = 'store_true', default = False,
                    dest = 'verbose',
                    help = 'verbose mode')

results = parser.parse_args()

if results.verbose == True:
    print('word              = ', results.targetword)
    print('dictionary        = ', results.dictionary)
    print('number of matches = ', results.numwords)
    print('lower             = ', results.lower)
    print('strip             = ', results.strip)
    print('verbose           = ', results.verbose)

with open(results.dictionary, 'r') as wordlist:
    wordlist = wordlist.read().splitlines()
    if results.lower == True:
        wordlist = list(map(str.lower, wordlist))

    if results.strip == True:
        table = str.maketrans('', '', string.punctuation)
        wordlist = [w.translate(table) for w in wordlist]

    print()
    print("Results for", results.targetword)
    print()
    h = []
    for line in wordlist:
        heapq.heappush(h, (fuzz.ratio(results.targetword, line), line))

    print(heapq.nlargest(results.numwords, h))
