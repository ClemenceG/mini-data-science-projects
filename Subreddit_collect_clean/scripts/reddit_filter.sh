#!/bin/bash
FILE=~/.data/quotes.csv

line=$(tail -n+2 $FILE | sort -R | head -n1)

citation=$(echo $line | cut -d \" -f 4-)
echo \"$citation

author=$(echo $line | cut -d \" -f 2)
echo "   " ~$author
