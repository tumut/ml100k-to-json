import argparse
import csv
import json
import re

from argparse import RawTextHelpFormatter

# ---

parser = argparse.ArgumentParser(description='''
Provide me with the movies JSON and I'll fix the ml100k titles, which include the movie's release year. I'll remove this year from the title and put it in a separate field 'movie_year'.

Movies without a release year in the title will be discarded, though this behavior can be disabled.
''', formatter_class=RawTextHelpFormatter)

parser.add_argument('input',
                    help="JSON input file with the movies")

parser.add_argument('-o', '--output',
                    help="Place the output into a file. Defaults to \"<input>.out\"")

parser.add_argument('-a', '--include-all',
                    help="Set it to not discard movies without a release year in the title",
					action="store_true")

args = parser.parse_args()

# ---

input_filename  = args.input
output_filename = args.output if args.output else input_filename + ".out"
include_all     = args.include_all

filtered = []
yearless = 0

with open(input_filename) as f:
	data = json.load(f)

	for movie in data:
		title = movie["movie_title"]
		m = re.search(r"(?P<title>.*)\((?P<year>\d*)\)", title)
		
		try:
			movie["movie_year"] = int(m.group("year"))
			movie["movie_title"] = m.group("title").strip()

			filtered.append(movie)
		except AttributeError:
			yearless += 1
			print("Title without a year:", title)
			if include_all: filtered.append(movie)

print(len(filtered), "movies processed.")

if not include_all:
	print(yearless, "movies didn't have a release year and were discarded.")

print("Saving to \"{}\"...".format(output_filename))

with open(output_filename, 'w') as output_file:
	json.dump(filtered, output_file)

print("Filtering finished.")