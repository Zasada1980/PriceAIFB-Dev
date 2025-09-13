# Contributing to PriceAIFB-Dev

Thank you for your interest in contributing to PriceAIFB-Dev! This document provides guidelines and instructions for contributors.

## Development Environment Setup

### Prerequisites

- Python 3.11+
- Git
- Docker and Docker Compose (optional, for containerized development)

### Quick Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Zasada1980/PriceAIFB-Dev.git
   cd PriceAIFB-Dev
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   make install-dev
   # or manually: pip install -r requirements.txt -e ".[dev]"
   ```

4. **Set up environment:**
   ```bash
   make env  # copies .env.example to .env
   ```

5. **Verify setup:**
   ```bash
   make run  # Should output demo JSON result
   make test # Should pass all tests
   ```

## Development Workflow

### Code Style and Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **Ruff**: Fast linting and static analysis
- **mypy**: Type checking
- **pytest**: Testing framework

### Development Commands

Use the Makefile for common development tasks:

```bash
make help          # Show all available commands
make format        # Format code with black and isort
make lint          # Run ruff linting
make typecheck     # Run mypy type checking
make test          # Run tests
make coverage      # Run tests with coverage report
make check         # Run all quality checks
make run           # Run demo pipeline
```

### Pre-commit Checklist

Before committing, ensure:

1. **Code is formatted:** `make format`
2. **No linting errors:** `make lint`
3. **Type checking passes:** `make typecheck`
4. **All tests pass:** `make test`
5. **Coverage is maintained:** `make coverage`

Or run all checks at once:
```bash
make check
```

## Project Architecture

### Directory Structure

```
src/
├── app/
│   ├── core/           # Configuration, logging, base classes
│   ├── services/       # Business logic (scoring, analysis)
│   └── pipelines/      # Data processing pipelines
└── tests/             # Test suite
```

### Key Principles

1. **Layered Architecture**: Clear separation between core, services, and pipelines
2. **Dependency Injection**: Use configuration and settings injection
3. **Type Safety**: Use type hints throughout the codebase
4. **Testing**: Comprehensive unit tests for business logic
5. **Documentation**: Clear docstrings and comments

## Making Changes

### Branching Strategy

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature development branches
- `bugfix/*`: Bug fix branches

### Commit Messages

Use clear, descriptive commit messages:

```
feat: add RVI calculation with VRAM penalty
fix: handle zero price in PVR calculation
docs: update contributing guidelines
test: add edge cases for scoring service
refactor: extract configuration to separate module
```

### Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the guidelines above

3. **Test thoroughly:**
   ```bash
   make check
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "feat: your descriptive message"
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request** with:
   - Clear description of changes
   - Link to related issues
   - Screenshots for UI changes
   - Test results

### Code Review

All changes require code review. Please:

- Respond to feedback promptly
- Make requested changes in separate commits
- Keep discussions professional and constructive
- Squash commits before merging if requested

## Testing Guidelines

### Writing Tests

- Place tests in `tests/` directory
- Use descriptive test names: `test_calculate_rvi_with_vram_penalty`
- Test edge cases and error conditions
- Use fixtures for common test data
- Aim for >90% code coverage

### Test Categories

1. **Unit Tests**: Test individual functions and classes
2. **Integration Tests**: Test component interactions
3. **Pipeline Tests**: Test end-to-end workflows

### Running Tests

```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_scoring.py

# Run with coverage
make coverage

# Run fast (no coverage)
make test-fast
```

## Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include parameter types and descriptions
- Provide usage examples for complex functions
- Document any assumptions or limitations

### README and Docs

- Keep README.md up to date
- Document new features and configuration options
- Include examples and troubleshooting tips

## Release Process

### Version Management

We use semantic versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Dependency Management

Use `requirements.in` for high-level dependencies:

```bash
# Add new dependency to requirements.in
echo "new-package>=1.0.0" >> requirements.in

# Compile pinned requirements
make compile

# Update all dependencies
make compile-upgrade
```

## Security Guidelines

- Never commit secrets or sensitive data
- Use environment variables for configuration
- Follow the principle of least privilege
- Report security issues privately to maintainers

## Getting Help

- Check existing issues and documentation first
- Create detailed bug reports with reproduction steps
- Ask questions in discussions or issues
- Join our development chat (if available)

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Maintain professional behavior

Thank you for contributing to PriceAIFB-Dev!