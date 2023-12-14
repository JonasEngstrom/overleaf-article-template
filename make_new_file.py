#!/usr/bin/env python3

# This script creates a new R Markdown file and sets it up to create a LaTeX
# file in the overleaf directory. The name is specified by a command line
# argument when calling the script. File extensions are added by the script.

import sys
import requests

assert len(sys.argv) > 1, ('You need to provide a command line argument with the desired name of the file to be created, e.g. */make_new_file.py new_file.')

downloaded_file = requests.get('https://raw.githubusercontent.com/JonasEngstrom/overleaf-article-template/main/main.Rmd')

with open(sys.argv[1] + '.Rmd', 'w') as output_file:
    output_file.write(downloaded_file.text.replace('main', sys.argv[1]))
