#!/bin/zsh

mkdir county_simple

npm install -g mapshaper

find ./county -type f -name "*.geojson" -exec mapshaper {} -simplify 20% -o county_simple/{} \;
