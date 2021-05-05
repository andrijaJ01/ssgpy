#!/bin/bash
outdir="/home/andrija/websites/danijelina-kuhinjica/" 
branch="updates"
comm="making some changes to $outdir"

cp -rv output/* $outdir
echo "Moved files to $outdir"
cd $outdir
git branch $branch
git add .
git commit -m "$comm"
