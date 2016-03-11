#! /bin/bash

set -e

ORIGINAL="connect-4.data.Z"
INPUT="connect-4.data"
OUTPUT="connect-4.data.converted"

uncompress -c $ORIGINAL > $INPUT
sed -e 's/win/1/g' -e 's/draw/0/g' -e 's/loss/0/g' -e 's/b/0/g' -e 's/x/1/g' -e 's/o/2/g' $INPUT > $OUTPUT
