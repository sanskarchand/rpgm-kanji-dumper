#!/usr/bin/env python
import requests
import json
import time

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="
POLITENESS_FACTOR = 0.1
INFO_BATCH = 10

def parse_response(response_text, meta):
    resp = json.loads(response_text)

    if resp['data'] == []:
        print("Error: Unable to find any matches for {}".format(meta['word']))
        return (None, None)
    
    data = resp['data'][0]

    if 'reading' not in data['japanese'][0].keys():
        return (None, None)
    if 'english_definitions' not in data['senses'][0].keys():
        return (None, None)

    reading = data['japanese'][0]['reading']
    definition = data['senses'][0]['english_definitions'][0]

    return (reading, definition)

    
def get_definition(word):
    url = JISHO_API + word
    r = requests.get(url)
    if r.status_code == 200:
        meta = {'word':word}
        return parse_response(r.text, meta)

    return None, None

def create_deck(dump_output, out_filename, stream_read=True, range_start=None, range_stop=None):
    data = dump_output
    fi = None

    if not stream_read:
        fi = open(dump_output, 'r')
        data = fi.read()
    
    lines = data.split('\n')
    anki_output = ""
    cur_ind = 0
    
    if range_start:
        lines = lines[range_start:]

    for line in lines:

        if range_stop and cur_ind > range_stop:
            break
        if (cur_ind + 1)% INFO_BATCH == 0:
            print("anki_maker: create_deck: processed {} words".format(cur_ind+1))

        # get only the word, not the frequencies (if present)
        word = line.split("\t")[0]
        reading, defn = get_definition(word)
        if reading:
            anki_output += f'{word};"{reading}\n{defn}"\n'
        else:
            print("Error: failed to get definition for ", word)

        time.sleep(POLITENESS_FACTOR)
        cur_ind += 1



    if fi:
        fi.close()

    with open(out_filename, 'w') as f:
        f.write(anki_output)
        print("Anki file generated at ", out_filename)

