# 🛒 Best Price Fetcher Tool

A powerful tool that compares product prices across multiple e-commerce websites for a given country and query. The tool scrapes various online retailers to find the best deals and returns results sorted by price.

## 🎯 **Proof of Working**

✅ **Required Query Test**: `{"country": "US", "query":"iPhone 16 Pro, 128GB"}`

**Results**: Found 8 results ranging from $455.99 to $760.00
- ✅ Successfully scraped eBay US
- ✅ Results sorted by price (lowest first)
- ✅ All results include product name, price, currency, and direct links

**Proof File**: `proof_of_working.json` contains complete test results with timestamps.

## 🚀 **Quick Start with Docker**

### **Prerequisites**
- Docker installed on your system
- Git (to clone the repository)

### **1. Clone the Repository**
```bash
git clone <your-repo-url>
cd price-fetcher-tool
```

### **2. Build and Run with Docker**

#### **Option A: Using Docker Compose (Recommended)**
```bash
# Build and start the container
docker-compose up -d

# Run the required test query
echo '{"country": "US", "query":"iPhone 16 Pro, 128GB"}' | docker exec -i price-fetcher python fetch_best_price.py
```

#### **Option B: Using Docker directly**
```bash
# Build the image
docker build -t price-fetcher .

# Run the required test query
echo '{"country": "US", "query":"iPhone 16 Pro, 128GB"}' | docker run --rm -i price-fetcher python fetch_best_price.py
```

#### **Option C: Using test scripts**
```bash
# For Linux/Mac
chmod +x test_docker.sh
./test_docker.sh

# For Windows
test_docker.bat
```

### **3. Interactive Testing**
```bash
# Enter the container for interactive use
docker exec -it price-fetcher bash

# Inside container, test different queries
echo '{"country": "US", "query":"Samsung Galaxy S24"}' | python fetch_best_price.py
echo '{"country": "US", "query":"PlayStation 5"}' | python fetch_best_price.py
```

## 🧪 **Testing Instructions**

### **1. Required Test Query**
```bash
# This is the mandatory test that must pass
echo '{"country": "US", "query":"iPhone 16 Pro, 128GB"}' | python fetch_best_price.py
```

**Expected Output**: JSON array with product results sorted by price.

### **2. Additional Test Queries**
```bash
# Test different products
echo '{"country": "US", "query":"MacBook Pro M3"}' | python fetch_best_price.py
echo '{"country": "US", "query":"Sony WH-1000XM5"}' | python fetch_best_price.py
echo '{"country": "US", "query":"Xbox Series X"}' | python fetch_best_price.py

# Test different countries
echo '{"country": "IN", "query":"OnePlus 12"}' | python fetch_best_price.py
```

### **3. Run Demo Script**
```bash
# Captures proof of working and saves to proof_of_working.json
python demo.py
```

### **4. Run Test Suite**
```bash
# Comprehensive test with multiple queries
python test_tool.py
```

## 📋 **Manual Installation (Alternative)**

If you prefer not to use Docker:

### **1. Install Python Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Run the Tool**
```bash
echo '{"country": "US", "query":"iPhone 16 Pro, 128GB"}' | python fetch_best_price.py
```

## 🏗️ **Architecture**

```
price-fetcher-tool/
├── fetch_best_price.py          # Main tool script
├── demo.py                      # Demo script for proof
├── test_tool.py                 # Comprehensive test suite
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose setup
├── test_docker.sh              # Linux/Mac test script
├── test_docker.bat             # Windows test script
├── proof_of_working.json       # Proof of working results
└── scrapers/                   # Scraper modules
    ├── __init__.py             # Scraper registry
    ├── amazon.py               # Amazon US scraper
    ├── ebay.py                 # eBay US scraper
    ├── walmart.py              # Walmart US scraper
    ├── flipkart.py             # Flipkart India scraper
    └── amazon_in.py            # Amazon India scraper
```

## 🌍 **Supported Countries and Retailers**

### **United States (US)**
- ✅ Amazon US
- ✅ eBay US  
- ✅ Walmart US

### **India (IN)**
- ⚠️ Flipkart India (may be blocked)
- ⚠️ Amazon India (may be blocked)

## 📊 **Features**

- **Multi-country support**: Currently supports US and India
- **Multiple retailers**: Searches across major e-commerce sites
- **Concurrent scraping**: Uses threading for faster results
- **Price sorting**: Results automatically sorted by price (lowest first)
- **Robust error handling**: Continues even if some scrapers fail
- **JSON input/output**: Easy integration with other tools
- **Docker support**: Containerized for easy deployment

## 🔧 **Troubleshooting**

### **Common Issues**

1. **Docker not found**:
   ```bash
   # Install Docker from https://docker.com
   ```

2. **Permission denied on test scripts**:
   ```bash
   chmod +x test_docker.sh
   ```

3. **No results found**:
   - Check internet connection
   - Some sites may block automated requests
   - Try different queries

4. **Import errors**:
   ```bash
   # Rebuild Docker image
   docker build --no-cache -t price-fetcher .
   ```

### **Debug Mode**
```bash
# Run with verbose output
docker run --rm -i price-fetcher python -u fetch_best_price.py
```

## 📝 **API Usage**

### **Input Format**
```json
{
  "country": "US",
  "query": "iPhone 16 Pro, 128GB"
}
```

### **Output Format**
```json
[
  {
    "link": "https://www.ebay.com/itm/...",
    "price": "455.99",
    "currency": "USD",
    "productName": "Apple iPhone 16 Pro 128GB",
    "source": "eBay US"
  }
]
```

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch
3. Add new scrapers or improve existing ones
4. Test thoroughly
5. Submit a pull request
