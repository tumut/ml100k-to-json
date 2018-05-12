#!/bin/bash

python3 ../process_ml100k.py
echo ""

python3 ../correct_title.py ml100k.json -o="movies.json"
echo ""

python3 ../get_imdb.py movies.json -o="movies-imdb.json"
echo ""

python3 ../prune.py movies-imdb.json -o="movies-imdb-pruned.json" -t="movies-imdbless.json"