# Market Scout Israel - Quick Start Guide

This guide will help you get started with the Market Scout Israel price monitoring system.

## 🚀 Installation

1. **Clone and install:**
```bash
git clone https://github.com/Zasada1980/PriceAIFB-Dev.git
cd PriceAIFB-Dev
pip install -e .
```

2. **Initialize database:**
```bash
python main.py init-database
```

3. **Run demo (optional):**
```bash
python demo.py
```

## 📊 Basic Usage

### CLI Commands

**View help:**
```bash
python main.py --help
```

**Check system stats:**
```bash
python main.py stats
```

**List recent listings:**
```bash
python main.py list-listings --limit 10
```

**Scrape data from Yad2:**
```bash
python main.py scrape --query "מחשב" --pages 3 --platform yad2
```

**Start API server:**
```bash
python main.py serve --host localhost --port 8000
```

### API Usage

Once the server is running, you can access:

- **API Documentation:** http://localhost:8000/docs
- **API Root:** http://localhost:8000/

**Example API calls:**
```bash
# Get all listings
curl "http://localhost:8000/listings"

# Filter by category
curl "http://localhost:8000/listings?category=gpu"

# Filter by price range
curl "http://localhost:8000/listings?min_price=1000&max_price=3000"

# Search for products
curl "http://localhost:8000/search?q=Intel"

# Get category statistics
curl "http://localhost:8000/stats/categories"

# Get city statistics
curl "http://localhost:8000/stats/cities"

# Get price trends
curl "http://localhost:8000/stats/trends?category=cpu&days=30"
```

## 🔧 Configuration

Create a `.env` file from the example:
```bash
cp .env.example .env
```

Key settings:
```env
# Database (SQLite by default)
DATABASE_URL=sqlite:///market_scout.db

# For PostgreSQL:
# DATABASE_URL=postgresql://user:password@localhost/market_scout

# Scraping settings
SCRAPING_DELAY_MIN=1
SCRAPING_DELAY_MAX=3
MAX_CONCURRENT_REQUESTS=5

# API settings
API_HOST=localhost
API_PORT=8000
```

## 📈 Data Analysis Examples

### Price Monitoring
```python
# Using Python requests
import requests

# Get average GPU prices
response = requests.get("http://localhost:8000/stats/categories")
data = response.json()

for category in data:
    if category['category'] == 'gpu':
        print(f"GPU average price: {category['avg_price']} ILS")
```

### Market Trends
```bash
# Get CPU price trends for last 7 days
curl "http://localhost:8000/stats/trends?category=cpu&days=7"

# Search for specific models
curl "http://localhost:8000/search?q=RTX%203080"

# Compare prices by city
curl "http://localhost:8000/listings?city=תל%20אביב"
curl "http://localhost:8000/listings?city=חיפה"
```

## 🛠️ Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_utils.py -v

# Run with coverage
pytest --cov=market_scout
```

### Code Quality
```bash
# Format code
black market_scout/ tests/

# Sort imports
isort market_scout/ tests/

# Type checking
mypy market_scout/

# Linting
flake8 market_scout/
```

## 🔍 Supported Platforms

### Yad2 (Ready)
- Computer components category
- Automatic price extraction
- Hebrew/English support
- Location detection

### Facebook Groups (Framework Ready)
- Requires Facebook API integration
- Group-specific configuration
- Authentication setup needed

## 🚨 Important Notes

### Legal Compliance
- Respect platform terms of service
- Built-in rate limiting (1-3 second delays)
- Only collect publicly available data
- Check robots.txt compliance

### Data Accuracy
- Prices extracted automatically (may need verification)
- Product categorization is rule-based
- Location detection works for major Israeli cities
- Condition assessment based on text analysis

### Performance
- SQLite for development/small deployments
- PostgreSQL recommended for production
- API supports pagination and filtering
- Database includes proper indexing

## 📋 Troubleshooting

**Database issues:**
```bash
# Reset database
rm market_scout.db
python main.py init-database
```

**API server issues:**
```bash
# Check if port is in use
lsof -i :8000

# Run on different port
python main.py serve --port 8001
```

**Scraping issues:**
- Check internet connection
- Verify target site accessibility
- Review rate limiting settings
- Check for site structure changes

## 🎯 Next Steps

1. **Configure real scraping targets**
2. **Set up regular scraping schedule**
3. **Add price alerts**
4. **Create custom analysis reports**
5. **Export data for external analysis**

For more detailed information, see the main README.md file.