# Market Scout Israel

A comprehensive price monitoring system for computer components and builds in the Israeli secondary market. This system automatically collects, processes, and analyzes listings from various platforms including Yad2 and Facebook Groups to provide up-to-date market intelligence.

## 🎯 Project Goals

1. **Automated Data Collection**: Automatically collect and fix information from computer component and build listings on Israel's secondary market (Facebook groups, Yad2, etc.)
2. **Price Database**: Build an up-to-date price reference database with date, city, product condition, and warranty information
3. **Market Intelligence**: Provide insights into market trends, pricing patterns, and regional variations

## 🏗️ Architecture

```
market_scout/
├── api/           # FastAPI REST API endpoints
├── config/        # Configuration management
├── models/        # Database models and schemas
├── scrapers/      # Platform-specific scrapers
│   ├── base.py    # Base scraper interface
│   ├── yad2.py    # Yad2 scraper
│   └── facebook.py # Facebook Groups scraper
└── utils/         # Utility functions and database setup
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- pip or poetry for dependency management

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Zasada1980/PriceAIFB-Dev.git
cd PriceAIFB-Dev
```

2. Install dependencies:
```bash
pip install -r requirements.txt
# or
pip install -e .
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize database:
```bash
python main.py init-database
```

### Basic Usage

1. **Scrape listings from Yad2:**
```bash
python main.py scrape --query "מחשב" --pages 3 --platform yad2
```

2. **Start the API server:**
```bash
python main.py serve --host localhost --port 8000
```

3. **View listings:**
```bash
python main.py list-listings --limit 20
```

4. **Get statistics:**
```bash
python main.py stats
```

## 📊 API Endpoints

### Core Endpoints

- `GET /` - API information
- `GET /listings` - Get listings with filtering options
- `GET /listings/{id}` - Get specific listing
- `GET /search` - Search listings by text

### Statistics Endpoints

- `GET /stats/categories` - Statistics by product category
- `GET /stats/cities` - Statistics by city
- `GET /stats/trends` - Price trends over time

### Example API Usage

```bash
# Get all GPU listings
curl "http://localhost:8000/listings?category=gpu&limit=50"

# Search for Intel products
curl "http://localhost:8000/search?q=intel"

# Get price trends for CPUs over last 30 days
curl "http://localhost:8000/stats/trends?category=cpu&days=30"
```

## 🛠️ Configuration

Key configuration options in `.env`:

```bash
# Database
DATABASE_URL=sqlite:///market_scout.db

# Scraping settings
SCRAPING_DELAY_MIN=1
SCRAPING_DELAY_MAX=3
MAX_CONCURRENT_REQUESTS=5

# API settings
API_HOST=localhost
API_PORT=8000

# Platform settings
FACEBOOK_GROUPS=group1,group2,group3
YAD2_BASE_URL=https://www.yad2.co.il
```

## 🗃️ Database Schema

The system uses SQLAlchemy models with the following key entities:

### Listing Model
- **Product Info**: Title, description, category, condition, brand, model
- **Pricing**: Price, currency, warranty details
- **Location**: City, region
- **Source**: Platform, URL, source ID
- **Metadata**: Scraped date, posted date, seller info

### Supported Categories
- CPU, GPU, Motherboard, RAM, Storage, PSU, Cooling, Case, Complete Build

### Supported Conditions
- New, Like New, Excellent, Good, Fair, Poor, For Parts

## 🔍 Scrapers

### Yad2 Scraper
- Searches computer category on Yad2
- Extracts listing details, prices, locations
- Handles Hebrew and English content
- Built-in rate limiting and error handling

### Facebook Groups Scraper
- **Note**: Requires proper Facebook API integration
- Placeholder implementation included
- Would need authentication and Graph API setup

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=market_scout

# Run specific test file
pytest tests/unit/test_utils.py
```

## 📈 Data Analysis Features

- **Price Trends**: Track price changes over time
- **Regional Analysis**: Compare prices across cities
- **Category Statistics**: Average prices by component type
- **Condition Impact**: Price differences by product condition
- **Market Activity**: Listing volume and trends

## 🚨 Important Notes

### Legal and Ethical Considerations
- **Respect robots.txt** and platform terms of service
- **Rate limiting** is implemented to avoid overloading servers
- **Data privacy** - only collect publicly available information
- **Commercial use** - ensure compliance with platform policies

### Limitations
- Facebook scraper requires proper API integration
- Some platforms may block automated access
- Data accuracy depends on source quality
- Regional coverage limited to Israeli market

## 🔄 Development

### Code Style
- Black formatting
- isort import sorting
- Type hints with mypy
- Comprehensive test coverage

### Development Commands
```bash
# Format code
black market_scout/ tests/

# Sort imports
isort market_scout/ tests/

# Type checking
mypy market_scout/

# Run linting
flake8 market_scout/ tests/
```

## 🛣️ Roadmap

- [ ] Enhanced Facebook API integration
- [ ] Machine learning price prediction
- [ ] Web dashboard interface
- [ ] Mobile notifications for deals
- [ ] Advanced analytics and reporting
- [ ] Multi-language support
- [ ] Export functionality (CSV, Excel)
- [ ] Price alerts system

## 📄 License

This project is intended for educational and research purposes. Please ensure compliance with platform terms of service and local laws when using this software.

## 🤝 Contributing

Contributions are welcome! Please:
1. Follow the existing code style
2. Add tests for new features
3. Update documentation as needed
4. Respect ethical scraping practices

## 📞 Support

For questions or issues, please open a GitHub issue or contact the development team.
