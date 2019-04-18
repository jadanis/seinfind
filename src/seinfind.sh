#!/bin/bash

str="'$*'"
if [ -z "$str" ]; then
  echo "Whoops! You didn\'t provide a search string!"
else
  python ./seinfind.py "$str"
fi
