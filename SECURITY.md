# Security Policy

## Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Please do NOT create a public GitHub issue for security vulnerabilities.**

Instead, please:

1. **Email us directly** at [security@example.com] (replace with actual email)
2. **Use GitHub Security Advisories** (preferred): Go to the Security tab → Report a vulnerability
3. **Contact the maintainers** through private channels

### What to Include

Please include the following information in your report:

- **Description** of the vulnerability
- **Steps to reproduce** the issue
- **Potential impact** and severity assessment
- **Suggested fix** (if you have one)
- **Your contact information** for follow-up

### Response Timeline

- **Initial Response**: Within 48 hours
- **Assessment**: Within 7 days
- **Fix Development**: Timeline depends on severity
- **Disclosure**: Coordinated disclosure after fix is available

## Security Measures

### Current Security Practices

1. **Dependency Scanning**: Automated vulnerability scanning with Trivy
2. **Code Analysis**: Static analysis with Ruff and mypy
3. **Secrets Management**: No secrets in source code, .env.example for templates
4. **Container Security**: Multi-stage builds, non-root user, minimal base images
5. **CI/CD Security**: Automated security checks in GitHub Actions

### Known Security Considerations

1. **Data Processing**: This tool processes external data (emails, listings)
   - Always validate and sanitize input data
   - Be cautious with email parsing and HTML content
   - Implement rate limiting for API endpoints

2. **Configuration**: 
   - Use environment variables for sensitive configuration
   - Regularly rotate API keys and credentials
   - Validate configuration values

3. **Dependencies**:
   - Regularly update dependencies
   - Monitor for security advisories
   - Use pinned versions in production

## Deployment Security

### Recommended Practices

1. **Environment Variables**:
   ```bash
   # Use strong, unique values
   DATABASE_URL=postgresql://user:strong_password@localhost/db
   API_SECRET_KEY=long_random_secure_key
   ```

2. **Docker Security**:
   ```bash
   # Run containers as non-root user
   docker run --user 1000:1000 priceaifb-dev
   
   # Limit container capabilities
   docker run --cap-drop=ALL priceaifb-dev
   ```

3. **Network Security**:
   - Use HTTPS in production
   - Implement proper firewall rules
   - Limit exposed ports

### Security Checklist

Before deploying to production:

- [ ] All secrets moved to environment variables
- [ ] Dependencies updated and scanned
- [ ] Container runs as non-root user
- [ ] Logging configured (no sensitive data in logs)
- [ ] Network access restricted
- [ ] Backup and recovery plan in place
- [ ] Monitoring and alerting configured

## Common Vulnerabilities

### Input Validation

Always validate external input:

```python
# Good
def process_price(price_str: str) -> float:
    try:
        price = float(price_str)
        if price < 0 or price > 1000000:
            raise ValueError("Price out of valid range")
        return price
    except ValueError as e:
        logger.warning("Invalid price input", price=price_str, error=str(e))
        raise
```

### Email Processing

When processing email content:

```python
# Be cautious with HTML content
from html import escape

def sanitize_description(text: str) -> str:
    # Remove potentially dangerous content
    sanitized = escape(text)
    # Additional sanitization as needed
    return sanitized
```

### API Security

For future API endpoints:

```python
# Implement rate limiting
# Validate authentication
# Sanitize responses
# Use HTTPS only
```

## Dependencies Security

### Monitoring

We use several tools to monitor dependencies:

1. **Trivy**: Container and dependency vulnerability scanning
2. **GitHub Dependabot**: Automated dependency updates
3. **pip-audit**: Python package vulnerability scanning (future)

### Update Process

1. Regular dependency reviews (monthly)
2. Immediate updates for critical vulnerabilities
3. Testing before applying updates
4. Coordinated updates across environments

## Incident Response

### In Case of Security Incident

1. **Immediate Response**:
   - Assess the scope and impact
   - Contain the incident if possible
   - Document everything

2. **Communication**:
   - Notify stakeholders
   - Prepare status updates
   - Coordinate disclosure timeline

3. **Recovery**:
   - Implement fixes
   - Deploy updates
   - Verify resolution

4. **Post-Incident**:
   - Conduct post-mortem
   - Update security measures
   - Share lessons learned

## Contact Information

- **Security Team**: [security@example.com]
- **Maintainers**: See CONTRIBUTING.md
- **GitHub Security**: Use repository Security tab

## Updates to This Policy

This security policy may be updated as the project evolves. Major changes will be announced through:

- Repository notifications
- Release notes
- Security advisories

---

**Last Updated**: January 2024  
**Version**: 1.0