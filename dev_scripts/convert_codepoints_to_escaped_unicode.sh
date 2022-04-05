#/!usr/bin/env sh

# Script to convert all occurrences of 'U+' in a file to '\u'
# (Made to automatically convert upstream SMuFL JSON to python-ready metadata)

function help_and_exit {
    echo "Convert all occurrences of 'U+' in a file (or files) to '\u'"
    echo "    USAGE: convert_codepoints_to_escaped_unicode.sh FILE [FILE ...]"
    exit
}

FILE_ARRAY=()
while [[ $# -gt 0 ]]
do
    if [ "$1" = "-h" ] || [ "$1" = "-help" ] || [ "$1" = "--h" ] || [ "$1" = "--help" ]; then
        help_and_exit
    else
        FILE_ARRAY+=("$1")
    fi
    shift
done

if [ ${#FILE_ARRAY[@]} = 0 ]; then
    help_and_exit
fi

for i in "${FILE_ARRAY[@]}"
do
    sed -i 's/U+/\\u/g' $i
done
