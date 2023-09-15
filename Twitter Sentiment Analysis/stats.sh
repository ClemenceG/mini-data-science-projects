#!/bin/bash

cat $1 | wc -l
head -1 $1
tail -10000 $1 | grep -i "potus" | wc -l
sed -n '100,200p' $1 | grep "fake" | wc -l
