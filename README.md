This repository contains a collection of scripts that help convert some of the data from the [MovieLens 100k Dataset](https://grouplens.org/datasets/movielens/100k/), commonly abbreviated as _ml100k_, into JSON files that are easier to handle.

## How to use

Each script has a `--help` (alt. `-h`) command that should help with using it. Ideally, you'll find that the scripts will be used in the following order:

 - `process_ml100k.py` - Generates the initial JSON file.
 - `correct_title.py` - Separates the release year from the movies' titles, putting it in a separate `movie_year` field.
 - `get_imdb.py` - Enriches each movie entry with a few IMDb data; requires an internet connection and may take a while.
 - `prune.py` - Removes movies for which the IMDb data couldn't be retrieved.

## Dependencies

 - [IMDbPY](https://github.com/alberanid/imdbpy/)
 - [jsonpickle](https://github.com/jsonpickle/jsonpickle)

## License

These scripts are released under the terms of the GNU GPL v2 license.
