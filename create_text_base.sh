#!/bin/bash

filename=""
# >= 	-ne
if [ $# -ge 1 ]; then
	filename=$(echo $1)
else
	filename="guid_to_100_pl_posts.txt"	
fi
echo $filename
exec 4<$filename
i=1
while read -u4 line; do
	if [ $i -le 20 ]; then
		source ./get_next_article.sh "$line"
	fi
	i=$((i+1))
done