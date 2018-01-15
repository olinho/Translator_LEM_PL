#!/bin/bash

remove_tags() {
	result=$(echo $1 | sed -e 's/<[^>]*>//g')
	echo "$result"
}

remove_quotes() {
	result=$(echo $1 | sed -e 's/\&quot;//g')
	echo "$result"
}
# &nbsp; &quot;
remove_special_characters() {
	result=$(echo $1 | sed -e 's/&[^;]*;//g')
	echo "$result"
}
#change >=1 space into one space
remove_multispaces() {
	result=$(echo $1 | sed -e 's/ \+/ /g')
	echo "$result"
}

directory=$(echo "$2")
page_name=$(cat $1 | grep '<title>' | sed -e 's/<[^>]*>//g' | cut -d '|' -f 1 | sed -e "s/\&quot;//g")
echo "$page_name"
content=$(remove_special_characters "$(remove_tags "$(cat $1 | grep '<p style="text-align: justify;">')")")
content=$(remove_multispaces "$(echo $content)")
echo "$content" > "$directory/$page_name.txt"

