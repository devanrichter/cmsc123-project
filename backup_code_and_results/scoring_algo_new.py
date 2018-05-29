import json
import math
import numpy as np
import pandas as pd

#Simplest, without counts
#
#with open('test.json') as f:
#	data = json.load(f)

#info = data["data"]
#for artist in info:
#	artist["tags"] = [t.lower() for t in artist["tags"]]

#pairs = []
#for i, artist1 in enumerate(info):
#	for j, artist2 in enumerate(info[i + 1 :]):
#		tags1 = artist1["tags"]
#		tags2 = artist2["tags"]
#		pairs.append((len(set(tags1) & set(tags2)) / min(len(tags1), len(tags2)), (artist1["artist"], artist2["artist"])))

#pairs.sort(reverse=True)

#Cosine similarity, with counts

with open('small_output.txt') as f:
	data = json.load(f)

info = [{"artist": key, "tags": val} for key, val in data.items()]

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
