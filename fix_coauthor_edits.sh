#!/usr/bin/env bash

# In case a coauthor has made edits instead of comments on Overleaf, so that git fails to push, this script can be run to overwrite changes to main.tex on Overleaf with the local version.

# Check that user really intends to overwrite remote repo.
echo "Warning! This will overwrite the file main.tex on Overleaf with the local couterpart."
echo "Do you wish to continue? (Type YES to continue.)"
read CONFIRMATION

case "$CONFIRMATION" in
  YES)
    git -C overleaf fetch origin
    git -C overleaf rebase origin/master
    git -C overleaf checkout --ours main.tex
    git -C overleaf add main.tex
    git -C overleaf rebase --continue
    git -C overleaf push
    echo "You can now re-knit main.tex in RStudio and run sync.sh to up update Overleaf."
    exit 0
    ;;
  *)
    echo "User did not type YES."
    exit 1
    ;;
esac
