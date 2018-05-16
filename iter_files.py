import os
import json
import time

start_time = time.time()
artist_dictionary = {}
dirpath = os.getcwd()
for subdir, dirs, files in os.walk(dirpath):
    for file in files:
        full_fname = subdir + os.sep + file
        if full_fname.endswith(".json"):
            with open(full_fname,'r') as f:
                song = json.load(f)
                artist = song['artist']
                tags = song['tags']
                for tag in tags:
                    if artist not in artist_dictionary:
                        artist_dictionary[artist] = []
                    artist_dictionary[artist].append(tag[0])
                    
for artist in artist_dictionary:
    print(artist)
    print(artist_dictionary[artist])
print("Length : %d" % len (artist_dictionary))
print("--- %s seconds ---" % (time.time() - start_time))
