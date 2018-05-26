import os
import sys
import sqlite3
import time

print('****  Acquire list of songs with tags ****')
fname = 'tracks_with_tag.txt'
songs_w_tags = []
with open(fname) as f:
    for line in f:
        track_id = line.strip()
        songs_w_tags.append(track_id)
print(len(songs_w_tags)) # 505216 songs w/ tags <- verified by website test code

print('**** Explore LastFM Tags SQL database ****')
dbfile = "lastfm_tags.db"
conn = sqlite3.connect(dbfile)
cursor = conn.execute('select * from tags')
colnames = cursor.description
for row in colnames:
    print(row[0]) # tag
print()

'''
tags table is of the form ROWID, tag
example for line 1: classic rock
'''

cursor = conn.execute('select * from tids')
colnames = cursor.description
for row in colnames:
    print(row[0]) # tid

'''
tids table is of the form ROWID, tid
example for line 1: TRCCCYE12903CFF0E9
'''

cursor = conn.execute('select * from tid_tag')
colnames = cursor.description
for row in colnames:
    print(row[0]) # tid, tag, val
print()

'''
tid_tag table is where things all come together
the columns are ROWID, tid, tag, val
tid and tag are index numbers from the tags and tids table
value is the value associate with the tag
example for line 1: 1|1|100.0
'''
