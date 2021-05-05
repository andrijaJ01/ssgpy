#!/bin/bash
outdir="/home/andrija/websites/danijelina-kuhinjica/" 

cp -rv output/* $outdir
echo "Moved files to $outdir"
echo "Enter branch name"
read branch-name
echo "Enter commit message"
read comm-msg
git branch $branch-name
git add .
git commit -m $comm-msg
