#!/bin/bash
cur_dir=$(pwd)
echo "COPYING:--------------------------------------------------------------------------"
cp -rv output/* /home/andrija/website-danijela
cd /home/andrija/website-danijela
echo "COPIED----------------------------------------------------------------------------"
clear
git branch -M updates 
echo "CREATED BRANCH--------------------------------------------------------------------"
git add . && git commit -m "updated-content" && git push -u origin updates
clear
echo "PUSHED CHANGES TO GITHUB"
echo "GO AND MAKE PULL REQUEST MANUALLY"
