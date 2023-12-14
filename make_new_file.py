#!/usr/bin/env python3

# This script creates a new R Markdown file and sets it up to create a LaTeX
# file in the overleaf directory. The name is specified by a command line
# argument when calling the script. File extensions are added by the script.

import sys
import requests
import os

# Check whether a file name has been been supplied as a command line argument.
assert len(sys.argv) > 1, ('You need to provide a command line argument with the desired name of the file to be created, e.g. */make_new_file.py new_file.')

# Download main.Rmd from GitHub.
downloaded_file = requests.get('https://raw.githubusercontent.com/JonasEngstrom/overleaf-article-template/main/main.Rmd')

# Replace main with the new file name and write file to disk.
with open(sys.argv[1] + '.Rmd', 'w') as output_file:
    output_file.write(downloaded_file.text.replace('main', sys.argv[1]))

# Add the new file to .gitignore in the overleaf repository.
os.system('/usr/bin/env bash -c "echo ' + sys.argv[1] + '.pdf >> overleaf/.gitignore"')
