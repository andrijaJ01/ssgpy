#!/bin/bash
outdir="~/websites/bloggy" 
branch="updates"
comm="changes to blog"

mkdir /home/andrija/websites/bloggy
cp -rv output/* /home/andrija/websites/bloggy
cd /home/andrija/websites/bloggy
git branch $branch
git add .
git commit -m "$comm"
git push
gh pr create

