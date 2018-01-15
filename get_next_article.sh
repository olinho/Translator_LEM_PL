#!/bin/bash
remove_quotes() {
	result=$(echo $1 | sed -e 's/\&quot;//g')
	echo "$result"
}

# remove slash from the end
lem_fm_url="http:\/\/www.lem.fm\/"
url_base=$(echo $1 | cut -d '?' -f 1 | sed -e "s/\/$//g")
url_pl="$url_base/?lang=pl"
url_lem="$url_base/?lang=lem"

article_name=$(remove_quotes "$(echo $url_base | sed -e "s/$lem_fm_url//")")
html_file_name="$article_name.html"
html_pl_file_path="pl/$html_file_name"
html_lem_file_path="lem/$html_file_name"
curl -L "$url_pl" > "$html_pl_file_path"
curl -L "$url_lem" > "$html_lem_file_path"
source ./filter_content.sh "$html_pl_file_path" "pl/"
source ./filter_content.sh "$html_lem_file_path" "lem/"


