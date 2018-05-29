from mrjob.job import MRJob
import os
import sys
import sqlite3
import time
import os.path


class MRTagBag(MRJob):

	def configure_options(self):
		super(MRTagBag, self).configure_options()
		self.add_file_option('--database1')
		self.add_file_option('--database2')
	
	def mapper_init(self):
		self.sqlite_conn = sqlite3.connect(self.options.database1)
		self.c = self.sqlite_conn.cursor()
		self.c.execute("ATTACH DATABASE 'lastfm_tags.db' AS 'lastfm_tags'")
		

	def mapper(self, _, line):
		clean_line = line.strip()
		track_id = clean_line

		queryResult = self.c.execute("SELECT songs.title, songs.artist_name, lastfm_tags.tags.tag\
        FROM lastfm_tags.tid_tag, lastfm_tags.tids, lastfm_tags.tags, songs\
        WHERE lastfm_tags.tags.ROWID=lastfm_tags.tid_tag.tag\
        AND lastfm_tags.tid_tag.tid=lastfm_tags.tids.ROWID\
        AND lastfm_tags.tids.tid='%s'\
        AND songs.track_id='%s' "% (track_id,track_id))

		while 1:
			item = queryResult.fetchone()
			if item == None:
				break
			tn, an, tag = item

			yield an, tag

	def combiner(self, artist, tags):
		v = set(tags)
		l = list(v)


		yield artist, l

	def reducer(self, artist, tags):
		
		v = set(tags)
		l = list(v)
		yield artist, l


if __name__ == '__main__':
	MRTagBag.run()