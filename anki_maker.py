#!/usr/bin/env python
import requests
import json
import time

JISHO_API = "https://jisho.org/api/v1/search/words?keyword="
POLITENESS_FACTOR = 0.1
INFO_BATCH = 10
LIMIT = 50000

def parse_response(response_text):
    resp = json.loads(response_text)

    if resp['data'] == []:
        return ("<ERROR>", "<Fault in kanji extraction (likely) or jisho.rog>")
    reading = resp['data'][0]['japanese'][0]['reading']
    definition = resp['data'][0]['senses'][0]['english_definitions'][0]

    return (reading, definition)

    
def get_definition(word):
    url = JISHO_API + word
    r = requests.get(url)
    if r.status_code == 200:
        return parse_response(r.text)

    return None, None

def create_deck(dump_output, out_filename, stream_read=True, num_words=None):
    data = dump_output
    fi = None

    if not stream_read:
        fi = open(dump_output, 'r')
        data = fi.read()
    
    lines = data.split('\n')
    anki_output = ""
    num_processed = 0
    limit = LIMIT
    if num_words:
        limit = int(num_words)

    for line in lines:
        num_processed += 1

        if num_processed > limit:
            break
        if num_processed % INFO_BATCH == 0:
            print("anki_maker: create_deck: processed {} words".format(num_processed))

        # get only the word, not the frequencies (if present)
        word = line.split("\t")[0]
        reading, defn = get_definition(word)
        if reading:
            anki_output += f'{word};"{reading}\n{defn}"\n'
        else:
            print("Error: failed to get definition for ", word)

        time.sleep(POLITENESS_FACTOR)



    if fi:
        fi.close()

    with open(out_filename, 'w') as f:
        f.write(anki_output)
        print("Anki file generated at ", out_filename)

