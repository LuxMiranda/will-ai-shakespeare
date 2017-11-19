#!/usr/bin/env bash

Q="\""
SONNET="$(python2 shakespeare.py)"
TEXT=$Q$SONNET$Q

convert shakespeare.jpg -blur 18,20 -font Lobster-Regular -pointsize 30 -fill grey -draw 'text 100,100 '"${TEXT}" out.jpg
