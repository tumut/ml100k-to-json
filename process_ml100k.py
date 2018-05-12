import argparse
import csv
import jsonpickle

from argparse import RawTextHelpFormatter

# ---

parser = argparse.ArgumentParser(description='''
Provide me with the ml100k files for movies and their ratings and I'll create a JSON representation of the movies with their average ratings. Each movie will be represented in the JSON file by an entry with the following fields:

movie_title:      The title with its release year (as in the ml100k database)
movie_genres:     A list of strings with the movie's genres
movie_avg_rating: The movie's average rating by the users who saw it

Further processing on this data, like separating the release year in the title into a different field, can be done by providing the resulting JSON file to the other scripts.
''', formatter_class=RawTextHelpFormatter)

default_movies_file       = "u.item"
default_movies_delimiter  = '|'
default_ratings_file      = "u.data"
default_ratings_delimiter = '\t'
default_genres_file       = "u.genre"
default_genres_delimiter  = '|'
default_output_file       = 'ml100k.json'

parser.add_argument('-m', '--movies',
                    help="CSV file with the movie data, in the ml100k format. Defaults to \"{}\"".format(default_movies_file),
					default=default_movies_file)

parser.add_argument('-md', '--movies-delimiter',
                    help="Delimiter of the movie CSV file. Defaults to '{}'".format(default_movies_delimiter),
					default=default_movies_delimiter)

parser.add_argument('-r', '--ratings',
                    help="CSV file with the ratings data, in the ml100k format. Defaults to \"{}\"".format(default_ratings_file),
					default=default_ratings_file)

parser.add_argument('-rd', '--ratings-delimiter',
                    help="Delimiter of the ratings CSV file. Defaults to '{}'".format(default_ratings_delimiter),
					default=default_ratings_delimiter)

parser.add_argument('-g', '--genres',
                    help="CSV file with the ratings data, in the ml100k format. Defaults to \"{}\"".format(default_genres_file),
					default=default_genres_file)

parser.add_argument('-gd', '--genres-delimiter',
                    help="Delimiter of the genres CSV file. Defaults to '{}'".format(default_genres_delimiter),
					default=default_genres_delimiter)

parser.add_argument('-o', '--output',
                    help="Place the output into a file. Defaults to \"{}\"".format(default_output_file),
					default=default_output_file)

args = parser.parse_args()

# ---

movies_filepath   = args.movies
movies_delimiter  = args.movies_delimiter
ratings_filepath  = args.ratings
ratings_delimiter = args.ratings_delimiter
genres_filepath   = args.genres
genres_delimiter  = args.genres_delimiter
output_filepath   = args.output

# ---

class Movie:
	def __init__(self, title, genres):
		self.title         = title
		self.genres        = genres
		self.ratings_total = 0
		self.ratings_count = 0

class MovieEntry:
	def __init__(self, movie):
		self.movie_title  = movie.title
		self.movie_genres = movie.genres
		self.movie_avg_rating = movie.ratings_total / movie.ratings_count

def write_as_json(obj, filepath):
	json = jsonpickle.encode(obj, unpicklable=False)
	
	with open(filepath, 'w') as output_file:
		output_file.write(json)

# ---

print("Reading genres from \"{}\"".format(genres_filepath))

genre_names = []

with open(genres_filepath) as genres_file:
	genres_csv = csv.reader(genres_file, delimiter=genres_delimiter)

	for row in genres_csv:
		if len(row) > 0:
			genre_names.append(row[0])

print("Reading movies from \"{}\"".format(movies_filepath))

movies = []

with open(movies_filepath, encoding='ISO-8859-1') as movies_file:
	movies_csv = csv.reader(movies_file, delimiter=movies_delimiter)
	
	for row in movies_csv:
		if len(row) == 0: continue

		title = row[1]
		genres = []

		genre_booleans = row[5:]

		for column_index, value in enumerate(genre_booleans):
			if value == "1":
				genres.append(genre_names[column_index])
		
		movies.append(Movie(title, genres))

print("All {} movies read".format(len(movies)))
print("Reading ratings from \"{}\"".format(ratings_filepath))

with open(ratings_filepath) as ratings_file:
	ratings_csv = csv.reader(ratings_file, delimiter=ratings_delimiter)
	
	for row in ratings_csv:
		movie_id = int(row[1])
		rating = int(row[2])

		movie = movies[movie_id - 1]
		movie.ratings_total += rating
		movie.ratings_count += 1

print("Preparing the data.")
movie_entries = [ (MovieEntry(m)) for m in movies ]

print("Writing data to file \"{}\"".format(output_filepath))
write_as_json(movie_entries, output_filepath)

print("All done!")