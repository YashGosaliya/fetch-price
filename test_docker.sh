#!/bin/bash

# Test script for Docker container
echo "🚀 Testing Price Fetcher Tool in Docker"
echo "========================================"

# Build the Docker image
echo "📦 Building Docker image..."
docker build -t price-fetcher .

# Test the required query
echo ""
echo "🧪 Testing with required query: {\"country\": \"US\", \"query\":\"iPhone 16 Pro, 128GB\"}"
echo "=================================================================================="

# Run the test query
echo '{"country": "US", "query":"iPhone 16 Pro, 128GB"}' | docker run --rm -i price-fetcher python fetch_best_price.py

echo ""
echo "✅ Test completed!" 