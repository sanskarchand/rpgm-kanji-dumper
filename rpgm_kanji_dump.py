#!/usr/bin/env python
import nagisa
import argparse
import json
import os
import sys
import collections
import anki_maker

KANJI_RANGE = (0x4E00, 0x9FBF)


PARAM_DICT_MV = {
    'parameters': 'parameters',
    'code': 'code',
    'events': 'events',
    'list': 'list'
}

PARAM_DICT_VX_ACE = {
    'parameters': '@parameters',
    'code': '@code',
    'events': '@events',
    'list': '@list'
}

_param_dict = PARAM_DICT_MV

parser = argparse.ArgumentParser(description="Extract sentences from RPGM MV data directories")
parser.add_argument("datadir", help="data directory (contains .json files)")
parser.add_argument("--vxace", action='store_true', help="RPGM VX Ace mode")
parser.add_argument("--verbose", action='store_true', help="Print filenames as they are processed")
parser.add_argument("--skip", action='store_true', help="Skip the word frequencies")
parser.add_argument("--out",  help="Name of the output file. Default is stdout")
parser.add_argument("--anki", help="Name of the text file to generate Anki-readable cards")
parser.add_argument("--alimit", type=int, help="Cutoff for the anki text file (number of words)")

# finds k,v pairs (at all levels, with _parent_ as root) for a given k
# puts that node (consider the json a tree) into _nodeList_
def get_nodes_by_name(parent, keyName, nodeList):
    for key in parent.keys():
        if key == keyName:
            nodeList.append(parent[key])
        else:
            # in RPGMV, a 'list' cannot be inside another one of the same
            newParent = parent[key]
            if type(newParent) == dict:
                get_nodes_by_name(newParent, keyName, nodeList)
            elif type(newParent) == list:
                for novaParent in newParent:
                    if type(novaParent) == dict: 
                        get_nodes_by_name(novaParent, keyName, nodeList)

def is_kanji(character):
    return ord(character) >= KANJI_RANGE[0] and ord(character) <= KANJI_RANGE[1]

def get_kanji(nodeList, kanjiCounter):
    #filter out only text events
    textEvents = [event for node in nodeList for event in node if event[ _param_dict['code'] ] == 401]
    
    for each in textEvents:
        japText = each[ _param_dict['parameters'] ][0]
        words = nagisa.tagging(japText)

        for word in words.words:
            for char in  word:
                if not (is_kanji(char)):
                    continue
                
                # add to list of kanji
                kanjiCounter[word] += 1

        

def process_file(filePath, kanjiCounter, verbose):
    if verbose:
        print(f"Processing file  {filePath}")
    nodeList = [] 
    with open(filePath, 'r') as f:
        mapData = json.loads(f.read())
        
        if type(mapData) == dict and _param_dict['events'] in mapData.keys():
            get_nodes_by_name(mapData, _param_dict['list'], nodeList)
            get_kanji(nodeList, kanjiCounter)



def main():
    kanjiCounter = collections.Counter()
    args = parser.parse_args()
    datadir = args.datadir

    if args.vxace:
        global _param_dict
        _param_dict = PARAM_DICT_VX_ACE
    
    #process only one level in the directory tree
    _, _, filenames = next(os.walk(datadir))    
    

    for fname in filenames:
        filePath = os.path.join(datadir, fname)
        process_file(filePath, kanjiCounter, args.verbose)

    outFile = sys.stdout
    if args.out:
        outFile = open(args.out, "w")
    
    freqSortedKanji = kanjiCounter.most_common()
    output = ''
    for pair in freqSortedKanji:

        if not args.skip:
            line = pair[0] + "\t" + str(pair[1])
        else:
            line = pair[0]
        output += line + "\n"
        outFile.write(line + "\n")

    if outFile != sys.stdout:
        outFile.close()

    if args.anki:
        anki_maker.create_deck(output, args.anki, stream_read=True, num_words=args.alimit)

    

if __name__ == '__main__':
    main()
