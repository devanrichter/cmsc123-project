import os
import sys
import sqlite3
import time

print('**** Explore Million Song SQL databases ****')
print('** first database: artist_term **')
dbfile = "artist_term.db"
conn = sqlite3.connect(dbfile)
'''
table names are artist_mbtag, artist_term, artists, mbtags, terms
'''
cursor = conn.execute('select * from artist_mbtag')
colnames = cursor.description
for row in colnames:
    print(row[0]) # artist_id, mbtag
print()

'''
artist_mbtag table is of the form ROWID, artist_id, mbtag
example for line 1: AR002UA1187B9A637D|uk
'''

cursor = conn.execute('select * from artist_term')
colnames = cursor.description
for row in colnames:
    print(row[0]) # artist_id, term
print()

'''
artist_term table is of the form ROWID, artist_id, term
example for line 1: AR002UA1187B9A637D|garage rock
'''

cursor = conn.execute('select * from artists')
colnames = cursor.description
for row in colnames:
    print(row[0]) # artist_id
print()

'''
artist table is of the form ROWID, artist_id
example for line 1: AR002UA1187B9A637D
'''

cursor = conn.execute('select * from mbtags')
colnames = cursor.description
for row in colnames:
    print(row[0]) # mbtag
print()

'''
mbtags table is of the form ROWID, mbtag
example for line 1: 00s
'''

cursor = conn.execute('select * from terms')
colnames = cursor.description
for row in colnames:
    print(row[0]) # term
print()

'''
terms table is of the form ROWID, term
example for line 1: 00s
'''
conn.close()

print('** second database: track_metadata **')
dbfile = "track_metadata.db"
conn = sqlite3.connect(dbfile)
'''
only one table named songs
'''

cursor = conn.execute('select * from songs')
colnames = cursor.description
for row in colnames:
    print(row[0]) # see form below
print()

'''
songs table is of the form ROWID, track_id, title, song_id, release, artist_id,
artist_mbid, artist_name, duration, artist_familiarity, artist_hottttnesss, year,
track_7digital, shs_perf, shs_work
example of line 1:
TRMMMYQ128F932D901|Silent Night|SOQMMHC12AB0180CB8|Monster Ballads X-Mas|
ARYZTJS1187B98C555|357ff05d-848a-44cf-b608-cb34b5701ae5|Faster Pussy cat|
252.05506|0.649822100201|0.394031892714|2003|7032331|-1|0
'''

conn.close()

print('****** end of program ******')
