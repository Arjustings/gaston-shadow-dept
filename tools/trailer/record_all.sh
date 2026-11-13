#!/bin/bash
cd "$(dirname "$0")/.."
while read -r name lvl miss; do
  timeout 150 node trailer/record.mjs "$name" "$lvl" $miss 2>&1 | tail -1
done <<'L'
rabbit 0
eiffel 1
elephant 6
dragon 8
gaston 9
fail 3 miss
ship 5
L
rm -rf trailer/gameplay/*_frames
