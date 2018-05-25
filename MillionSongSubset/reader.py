#!/usr/bin/env python3
import sys
import os
import sqlite3

def sanitize(tag):

	tag = tag.replace("'", "''")

	return tag

dbfile = "lastfm_tags.db"

conn = sqlite3.connect(dbfile)

d = []
tags = {}
def read():
	file = str(sys.argv[1])

	with open(file) as f:
		lines = [line.strip().lower() for line in f]
		for l in lines:
			segs = l.split("<sep>")
		
			d.append((segs[3],segs[2]))
	print(d)

	return 

def sync():
	for tup in d:
		artist, tid = tup
		tid = tid.upper()
		print("TUP is: " + str(tup))
		print("tid is: " + tid)
		sql = "SELECT tags.tag, tid_tag.val FROM tid_tag, tids, tags WHERE tags.ROWID=tid_tag.tag AND tid_tag.tid=tids.ROWID and tids.tid='%s'" % tid
		res = conn.execute(sql)
		data = res.fetchall()
		print(data)


read()
sync()