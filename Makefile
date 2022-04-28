#The entire dataset split into the county-level subsets store in different counties
county data:
	mkdir -p county
img:
	mkdir -p img
# All source codes store into this folder
src:
	mkdir -p src
# Split data in src/raw_data by county boundaries in src/county_boundaries
split:
	python -B src/split_by_maine_county.py

# Run a basic development server to debug the gh-pages site
dev:
	python -m http.server -d docs

# Generate a static tier map for the gh-pages site and README
map:
	python -B src/tier_map.py