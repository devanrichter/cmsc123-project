# import package and load file
import h5py
f = h5py.File('test.h5','r')

# look at database groups
list(f.keys())

# above will give you keys of analysis, metadata, and musicbrainz
analysis = f['analysis']
metadata = f['metadata']
musicbrainz = f['musicbrainz']

# lists the keys within each of the three groups
list(analysis)
list(metadata)
list(musicbrainz)

# useful data parts
list(metadata['artist_terms']) # 12 tags for artist
