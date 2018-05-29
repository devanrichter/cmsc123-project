from mrjob.job import MRJob
import os
import sys
import sqlite3
import time
import os.path
import json
from mrjob.step import MRStep
import math
import pandas as pd 
import numpy as np


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
			tn = item[0]
			an = item[1]
			tag = item[2]
			yield an, tag

	def combiner(self, artist, tags):
		for tag in tags:
			yield artist, tag.lower()

	def reducer_init(self):
		self.output_dictionary = {}

	def reducer1(self, artist, tags):
		artist_dictionary = {}
		for tag in tags:
			artist_dictionary[tag] = artist_dictionary.get(tag,0) + 1
		self.output_dictionary[artist] = artist_dictionary
		yield None, None

	def reducer2(self, _, __):
		
		info = [{"artist": key, "tags": val} for key, val in self.output_dictionary.items()]
		tag_artist_count = {}
		tag_total_freqs = {}
		for artist in info:
			for tag, count in artist["tags"].items():
				#ltag = tag.lower()
				#artist["tags"][ltag] = artist["tags"].pop(tag)
				tag_total_freqs[tag] = tag_total_freqs.get(tag, 0) + count
				tag_artist_count[tag] = tag_artist_count.get(tag, 0) + 1
		all_tags = tag_artist_count.keys()
		num_artists = len(info)
		tf_idf_vecs = []
		for artist in info:
			vec = []
			for tag in all_tags:
				if tag in artist["tags"]:
					n_d = artist["tags"][tag]
					numerator = num_artists
					denominator = tag_artist_count[tag]
					w_d = n_d * math.log(numerator / denominator)
					vec.append(w_d)
				else:
					vec.append(0)
			tf_idf_vecs.append((artist["artist"], vec))

		pairs = []
		for i, tup1 in enumerate(tf_idf_vecs):
			for j, tup2 in enumerate(tf_idf_vecs[i + 1 :]):
				pairs.append([tup1[0], tup2[0], np.dot(tup1[1], tup2[1]) / (np.linalg.norm(tup1[1]) * np.linalg.norm(tup2[1]))])
		df = pd.DataFrame(pairs, columns = ["Artist 1", "Artist 2", "Cosine Similarity"])
		df = df.sort_values(by="Cosine Similarity", ascending = False)
		df.to_csv("results.csv", index=False)



		yield None, None

	def steps(self):
		return [ 
		MRStep(mapper_init = self.mapper_init, mapper=self.mapper,
		combiner=self.combiner,reducer_init = self.reducer_init, reducer=self.reducer1),
		MRStep(reducer=self.reducer2)]

if __name__ == '__main__':
	MRTagBag.run()
