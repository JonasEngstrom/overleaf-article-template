#!/usr/bin/env bash

# Stages, commits, and pushes files to both Overleaf and GitHub.
# Sets up sync with GitHub and Overleaf on first run.

if [ $# -lt 1 ]
  then
    echo "Error: You must enter a commit message. (E.g. ./sync.sh \"This commit will surely fix all the bugs.\") Exiting." 1>&2
    exit 1
fi

if [ ! -d ./.git/refs/remotes ]
  then
    echo "GitHub not set up."
    echo "Enter GitHub SSH or HTTPS address:"
    read GITHUB_ADDRESS
    git add -A
    git commit -m "$1"
    git branch -M main
    git remote add origin $GITHUB_ADDRESS
    git push -u origin main
fi

if [ ! -d ./overleaf ]
  then
    echo "Overleaf not set up."
    echo "Enter Overleaf SSH or HTTPS address:"
    read OVERLEAF_ADDRESS
    git submodule add $OVERLEAF_ADDRESS overleaf
    git -C overleaf checkout master
    git -C overleaf pull
    cat << EOF >> overleaf/.gitignore
main.pdf
**/.DS_Store
EOF
fi

if [ ! -f .git/modules/overleaf/hooks/pre-commit ]
  then
    cp hooks/overleaf/pre-commit.py .git/modules/overleaf/hooks/pre-commit
fi

if [ $(git symbolic-ref --short -q HEAD) != "main" ]
  then
    echo "Not on main. Make sure the branch main is checked out before running sync.sh."
    exit 1
fi

echo "Checking out master branch on Overleaf."
git -C overleaf checkout master

echo "Pulling from Overleaf."
git -C overleaf pull

echo "Pulling from GitHub."
git pull

echo "Staging Overleaf files."
git -C overleaf add -A

echo "Committing Overleaf files."
git -C overleaf commit -m "$1"

echo "Pushing files to Overleaf."
git -C overleaf push -u origin master

echo "Staging GitHub files."
git add -A

echo "Committing GitHub files."
git commit -m "$1"

echo "Pushing files to GitHub."
git push -u origin main
