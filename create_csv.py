import os
import sys
import sqlite3
import time

dbfile = "track_metadata.db"
conn = sqlite3.connect(dbfile)
c = conn.cursor()
c.execute("ATTACH DATABASE 'lastfm_tags.db' AS 'lastfm_tags'")

with open("tracks_with_tag.txt") as f:
    for line in f:
        clean_line = line.strip()
        track_id = clean_line
        c.execute("SELECT songs.title, songs.artist_name, lastfm_tags.tags.tag\
        FROM lastfm_tags.tid_tag, lastfm_tags.tids, lastfm_tags.tags, songs\
        WHERE lastfm_tags.tags.ROWID=lastfm_tags.tid_tag.tag\
        AND lastfm_tags.tid_tag.tid=lastfm_tags.tids.ROWID\
        AND lastfm_tags.tids.tid='%s'\
        AND songs.track_id='%s'" % (track_id,track_id))
        data = c.fetchall()
        for item in data:
            print(item)
conn.close()
