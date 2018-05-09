# import package and load file
import json
with open('test.json','r') as f:
	song = json.load(f)

# view keys of dictionary
list(song)

'''
Results are:
artist, timestamp, similars, tags, track_id, title
artist is artist as string
timestamp is y-m-d and time song was published I believe
tags is list of lists giving a tag and a number?
track_id is string of the track id in million song database
title is song title as a string
'''

