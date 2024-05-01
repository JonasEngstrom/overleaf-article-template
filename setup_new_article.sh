#!/usr/bin/env bash

# Creates a new GitHub repo using the https://github.com/JonasEngstrom/overleaf-article-template
# template and connects it to an Overleaf repo. Takes two arguments. The first is the project
# name and the second one is the URL to the Overleaf repo. The script only needs to be run once
# and the file can be deleted after the article has been set up.

# Check number of arguments.
if [[ $# -lt 2 ]] ; then
    echo Please provide a project name as the first argument and the URL of the Overleaf git repository as the second argument.
    exit 1
fi

# Create repo from template on GitHub.
gh repo create $1 --template JonasEngstrom/overleaf-article-template --private

# Clone repo from GitHub.
gh repo clone $1 -- --recursive

# Run sync.sh.
cd $1
printf "$2" | ./sync.sh "Initial commit."