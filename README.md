# PriceAIFB-Dev

**Analytics and scoring system for secondary market listings (RVI/PVR/VPS)**

A minimal viable project framework for analyzing and scoring real estate, vehicle, and computing equipment listings using IFR (Ideal Final Result) principles and TRIZ contradiction resolution.

![CI Status](https://github.com/Zasada1980/PriceAIFB-Dev/workflows/CI%20Pipeline/badge.svg)
[![Coverage](https://img.shields.io/badge/coverage-%3E70%25-green.svg)](https://github.com/Zasada1980/PriceAIFB-Dev)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 🎯 Project Goals (IFR - Ideal Final Result)

**The system from the box:**
- ✅ Starts locally with one command (`python` or `docker compose`)
- ✅ Has deterministic dependencies (pinned requirements.txt)
- ✅ Has layered structure (core, adapters, services, pipelines, models, api)
- ✅ Demonstrates working pipeline (demo scoring) as extension point
- ✅ Has basic CI (lint+type+tests+image scan), no red statuses
- ✅ Contains no sensitive data and doesn't commit secrets
- ✅ Ready for extension without breaking (minimal coupling, clear integration points)

## 🏗️ Architecture & TRIZ Principles Applied

### Key Contradictions Resolved

| Contradiction | Solution | TRIZ Principle |
|--------------|----------|---------------|
| Architecture flexibility vs minimal code | Layered framework with stubs | #1 Segmentation |
| Fast CI setup vs complexity | Unified workflow ci.yml | #10 Preliminary action |
| Logging extensibility vs simplicity | JSON logger with metrics capability | #15 Dynamism |
| Fixed environment vs need for updates | requirements.in + pinned requirements.txt | #3 Local quality |
| Fast scoring modification vs regression protection | Unit tests + dataclass results | #11 Buffering |
| Container stability vs small size | Multi-stage Dockerfile | #2 Extraction |
| Low contributor barrier vs need for rules | CONTRIBUTING + Makefile shortcuts | #24 Intermediary |

### Directory Structure

```
PriceAIFB-Dev/
├── src/
│   └── app/
│       ├── core/          # Configuration, logging, base classes
│       │   ├── config.py  # Pydantic settings
│       │   └── logging.py # Structured JSON logging
│       ├── services/      # Business logic
│       │   └── scoring.py # RVI/PVR calculation engine
│       └── pipelines/     # Data processing workflows
│           └── run.py     # Demo pipeline runner
├── tests/
│   └── test_scoring.py    # Comprehensive scoring tests
├── .github/workflows/
│   └── ci.yml            # Complete CI/CD pipeline
├── requirements.in        # High-level dependencies
├── requirements.txt       # Pinned dependencies
├── pyproject.toml        # Tool configuration
├── Dockerfile            # Multi-stage container build
├── docker-compose.yml    # Container orchestration
├── Makefile             # Development shortcuts
└── docs/                # Documentation
    ├── CONTRIBUTING.md
    ├── SECURITY.md
    └── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (optional)

### Local Development

```bash
# 1. Clone and setup
git clone https://github.com/Zasada1980/PriceAIFB-Dev.git
cd PriceAIFB-Dev

# 2. Environment setup
cp .env.example .env
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run demo pipeline
python -m src.app.pipelines.run
```

Expected output:
```json
{
  "status": "success",
  "pipeline": "demo_scoring",
  "scoring": {
    "rvi": 71.53,
    "pvr": 0.0159,
    "final_score": 15.9,
    "vram_penalty_applied": true
  },
  "interpretation": {
    "investment_grade": "good",
    "recommendation": "✅ Good investment opportunity"
  }
}
```

### Docker Deployment

```bash
# Build and run
docker compose up -d --build

# Check logs
docker compose logs -f

# Stop
docker compose down
```

## 📊 Scoring System (RVI/PVR/VPS)

### Core Formulas

**RVI (Resale Value Index):**
```
RVI = (CPU_score × wCPU + GPU_score × wGPU + Other_score × wOther)
      × PLS × MLI × CWM × VRAM_penalty
```

**PVR (Price-to-Value Ratio):**
```
PVR = RVI / Price
```

**Final Score:**
```
Final Score = PVR × 1000  (scaled for readability)
```

### Parameters

- **wCPU/wGPU/wOther**: Component weights (0.4/0.5/0.1)
- **PLS**: Platform Liquidity Score (upgrade potential)
- **MLI**: Market Liquidity Index (resale speed)
- **CWM**: Condition/Warranty Multiplier
- **VRAM_penalty**: Applied when GPU VRAM ≤ 8GB (0.85×)

### Investment Grades

- **🔥 Excellent (>20)**: Strong buy recommendation
- **✅ Good (15-20)**: Good investment opportunity  
- **⚠️ Average (10-15)**: Consider other factors
- **❌ Poor (<10)**: Avoid or negotiate significantly

## 🛠️ Development

### Available Commands

```bash
make help          # Show all commands
make format        # Format code (black + isort)
make lint          # Run linting (ruff)
make typecheck     # Type checking (mypy)
make test          # Run tests
make coverage      # Tests with coverage
make run           # Run demo pipeline
make check         # All quality checks
make build         # Build Docker image
make up            # Start with docker-compose
```

### Dependency Management

```bash
# Add new dependency
echo "new-package>=1.0.0" >> requirements.in
make compile

# Update all dependencies  
make compile-upgrade
```

### Code Quality Standards

- **Formatting**: Black (88 chars)
- **Imports**: isort
- **Linting**: Ruff (pycodestyle + pyflakes + bugbear)
- **Type Checking**: mypy (strict mode)
- **Testing**: pytest with >90% coverage
- **Documentation**: Comprehensive docstrings

## 🔒 Security & Configuration

### Environment Variables

```bash
# Core settings
LOG_LEVEL=INFO
LOG_FORMAT=json
DEBUG=false

# Scoring parameters (customizable)
CPU_WEIGHT=0.4
GPU_WEIGHT=0.5
OTHER_WEIGHT=0.1
VRAM_PENALTY_THRESHOLD=8
VRAM_PENALTY_FACTOR=0.85
```

### Security Features

- ✅ No secrets in source code
- ✅ Environment-based configuration
- ✅ Container security (non-root user)
- ✅ Automated vulnerability scanning (Trivy)
- ✅ Dependency pinning
- ✅ Input validation and sanitization

## 🧪 Testing

### Running Tests

```bash
# All tests
make test

# Specific test file
pytest tests/test_scoring.py -v

# With coverage
make coverage

# Fast tests (no coverage)
pytest tests/test_scoring.py --tb=short
```

### Test Coverage

- **Scoring Service**: 100% coverage
- **Configuration**: 100% coverage  
- **Overall**: >70% coverage
- **Critical Paths**: 100% coverage required

## 🚀 CI/CD Pipeline

### Automated Checks

1. **Code Linting** (ruff)
2. **Format Checking** (black, isort)
3. **Type Checking** (mypy)
4. **Unit Tests** (pytest + coverage)
5. **Docker Build & Test**
6. **Security Scanning** (Trivy)
7. **Demo Pipeline Validation**

### GitHub Actions

- Triggers: Push/PR to main/develop
- Parallel execution for speed
- Artifact storage (demo outputs)
- Security integration (GitHub Security tab)
- Comprehensive reporting

## 📈 Roadmap

### Phase 1: Foundation ✅
- [x] Minimal viable framework
- [x] Core scoring engine (RVI/PVR)
- [x] Demo pipeline
- [x] CI/CD setup
- [x] Docker containerization

### Phase 2: Data Ingestion (Next)
- [ ] IMAP email adapter
- [ ] Email parsing and normalization
- [ ] Text extraction and cleaning
- [ ] Basic data validation

### Phase 3: Intelligence (Future)
- [ ] Machine learning price prediction
- [ ] Synonym dictionaries
- [ ] Market trend analysis
- [ ] Comparative scoring

### Phase 4: Integration (Future)  
- [ ] Database layer (SQLite → PostgreSQL)
- [ ] REST API endpoints
- [ ] Telegram notifications
- [ ] Web dashboard

### Phase 5: Operations (Future)
- [ ] Metrics and monitoring (Prometheus)
- [ ] Distributed deployment
- [ ] Rate limiting and throttling
- [ ] Advanced analytics

## 📝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for:

- Development environment setup
- Code style guidelines
- Pull request process
- Testing requirements

### Quick Contribution Setup

```bash
# Development setup
make dev-setup
make env

# Before committing
make check

# Run demo
make run
```

## 🔐 Security

For security concerns, please see [SECURITY.md](SECURITY.md) or contact us privately.

- **Reporting**: Use GitHub Security advisories
- **Response Time**: 48 hours for initial response
- **Disclosure**: Coordinated disclosure after fixes

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: [GitHub Issues](https://github.com/Zasada1980/PriceAIFB-Dev/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Zasada1980/PriceAIFB-Dev/discussions)
- **Documentation**: [Wiki](https://github.com/Zasada1980/PriceAIFB-Dev/wiki)

---

**Built with ❤️ using TRIZ principles and IFR methodology**
