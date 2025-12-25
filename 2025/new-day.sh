#!/usr/bin/env bash

set -e

day_num="$1"
if [[ -z "$day_num" ]]; then
  echo "Usage: pnpm new-day <day-number>"
  exit 1
fi

target_ts="src/d${day_num}.ts"
target_txt="data/d${day_num}.txt"
target_example="data/d${day_num}_example.txt"

cp src/template.ts "$target_ts"
touch "$target_txt"
touch "$target_example"

# Add script to package.json
cp src/template.ts "$target_ts"
touch "$target_txt"
touch "$target_example"

# Add script to package.json using jq
jq ".scripts.d${day_num} = \"pnpm with-env pnpm tsx ./src/d${day_num}.ts\"" package.json > package.json.tmp && mv package.json.tmp package.json

echo "Day $day_num setup complete."
