#!/bin/bash
remove_english_month_name() {
	sed 's/\/авґуст[^ ]*//;s/\/януар[^ ]*//;s/\/фебруар[^ ]*//;s/\/септембр[^ ]*//;s/\/юл[^ ]*//;s/\/новемб[^ ]*//;s/\/октоб[^ ]//;s/\/деземб[^ ]//;s/\/апріл[^ ]//;s/\/май[^ ]//;s/\/юн[^ ]//;s/\/мар[^ ]//'
}

cat "$1" | sed 's/[.!?] */&\n/g' | sed 's/\([^,]*\),\( *\)\([^,]*\)/\1, \3/g' | sed 's/[\«\»]/\"/g' | sed 's/[\„\”]/\"/g' | remove_english_month_name > "$2"

