#!/bin/bash
outdir="~/websites/bloggy/" 
branch="updates"
comm="making some changes to $outdir"
cur_dir= $(pwd)

cp -rv output/* $outdir
echo "Moved files to $outdir"
cd $outdir
git branch $branch
git add .
git commit -m "$comm"
gh pr create
cd $cur_dir
