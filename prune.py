import argparse
import json

from argparse import RawTextHelpFormatter

# ---

parser = argparse.ArgumentParser(description='''
Provide me with the movies JSON and I will remove each movie without IMDb data. I expect the movies of this JSON to have acquired their IMDb data by the 'get_imdb.py' script.\n

Movies with the 'imdb_failed' field will be automatically discarded, though this behavior can be disabled.
''', formatter_class=RawTextHelpFormatter)

default_fields = [ 'movie_director', 'movie_cast', 'movie_plot' ]

def list_to_str(strings):
	result = None
	for s in strings:
		s = "'{}'".format(s)
		if not result: result = s
		else: result += ' ' + s
	return result

parser.add_argument('input',
                    help="JSON input file with the movies")

parser.add_argument('-o', '--output',
                    help="Place the output into a file. Defaults to \"<input>.out\"")

parser.add_argument('-t', "--trash-output",
                    help="Place the discarded movies into a separate file")

parser.add_argument('-f', '--obligatory-fields',
                    help="Fields which the movie must have for it to be considered with IMDb data. If even one of them is not found, the entry will be discarded. Default fields: {}".format(list_to_str(default_fields)),
					nargs='+', default=default_fields)

parser.add_argument('--disable-imdb-failed',
                    help="Set it so that the 'imdb_failed' field won't be used to automatically discard movies",
					action="store_true")

args = parser.parse_args()

# ---

input_filename    = args.input
output_filename   = args.output if args.output else input_filename + ".out"
obligatory_fields = args.obligatory_fields
use_imdb_failed   = not args.disable_imdb_failed
trash_filename    = args.trash_output

# ---

print("Input filename  : \"{}\"".format(input_filename))
print("Output filename : \"{}\"".format(output_filename))
print("Fields that will be obligatory:", list_to_str(obligatory_fields))
if use_imdb_failed: print("Movies with 'imdb_failed' will be promptly discarded.")
print("---")

data = None

with open(input_filename) as input_file:
	data = json.load(input_file)

kept_movies = []
trash = []

for movie in data:
	if use_imdb_failed and 'imdb_failed' in movie:
		print("Discarded movie with 'imdb_failed': \"{}\"".format(movie["movie_title"]))
		if trash_filename: trash.append(movie)
		continue
	
	for field in obligatory_fields:
		if field not in movie:
			print("Discarded movie without obligatory fields: \"{}\"".format(movie["movie_title"]))
			if trash_filename: trash.append(movie)
			continue
	
	kept_movies.append(movie)

print("Saving to \"{}\"...".format(output_filename))

with open(output_filename, 'w') as output_file:
	json.dump(kept_movies, output_file)

if trash_filename:
	print("Saving discarded files to \"{}\"...".format(trash_filename))
	with open(trash_filename, 'w') as trash_file:
		json.dump(trash, trash_file)

kept_percent = "{0:.2f}".format((len(kept_movies) * 100) / len(data))

print("---")
print("{} movies ({}%) kept after pruning.".format(len(kept_movies), kept_percent))
