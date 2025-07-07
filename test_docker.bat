@echo off
REM Test script for Docker container (Windows)

echo 🚀 Testing Price Fetcher Tool in Docker
echo ========================================

REM Build the Docker image
echo 📦 Building Docker image...
docker build -t price-fetcher .

REM Test the required query
echo.
echo 🧪 Testing with required query: {"country": "US", "query":"iPhone 16 Pro, 128GB"}
echo ==================================================================================

REM Run the test query
echo {"country": "US", "query":"iPhone 16 Pro, 128GB"} | docker run --rm -i price-fetcher python fetch_best_price.py

echo.
echo ✅ Test completed!
pause 