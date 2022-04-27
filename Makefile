# Split data in src/raw_data by county boundaries in src/county_boundaries
split:
	python -B src/split_by_maine_county.py

# Run a basic development server to debug docs
dev:
	python -m http.server -d docs
