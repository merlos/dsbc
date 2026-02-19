# dsbc - DeepSeek Tools Collection

[![PyPI version](https://img.shields.io/pypi/v/dsbc.svg)](https://pypi.org/project/dsbc/)
[![Python versions](https://img.shields.io/pypi/pyversions/dsbc.svg)](https://pypi.org/project/dsbc/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub Actions](https://github.com/merlos/dsbc/actions/workflows/release.yml/badge.svg)](https://github.com/merlos/dsbc/actions/workflows/release.yml)

A collection of tools for interacting with DeepSeek API, starting with a Python CLI tool to check account balances and view available models.

## Features

- ✅ **Check account balance** - Total, available, and used balance
- ✅ **View available models** - With pricing and context window information
- ✅ **Multiple auth methods** - Environment variables or command-line tokens
- ✅ **JSON output** - Perfect for scripting and automation
- ✅ **API health checks** - Verify your API token works
- ✅ **Verbose mode** - Detailed output for debugging
- ✅ **Modern packaging** - Works with both `pip` and `uv`
- ✅ **Type hints** - Full type annotations for better IDE support
- ✅ **Comprehensive tests** - Well-tested with pytest
- ✅ **GitHub Actions** - Automated releases to PyPI

## Installation

### Install with pip

```bash
# Install from PyPI
pip install dsbc

# Install with development dependencies
pip install dsbc[dev]

# Install with uv support
pip install dsbc[uv]
```

### Install with uv

```bash
# Install from PyPI
uv pip install dsbc

# Install with development dependencies
uv pip install "dsbc[dev]"
```

### Install from source

```bash
# Clone the repository
git clone https://github.com/ianmerlos/dsbc.git
cd dsbc/cli

# Install with pip in development mode
pip install -e .

# Or install with uv
uv pip install -e .
```

## Quick Start

```bash
# Set your API token as environment variable
export DEEPSEEK_API_TOKEN="your-api-token-here" 
# Also DEEKSEEK_API_KEY, DEEPSEEK_TOKEN, OPENAI_API_KEY

# Check your balance
dsbc

# Show available models
dsbc --models

# JSON output for scripting
dsbc --json

# Check API health
dsbc --health

# Verbose mode
dsbc --verbose
```

## Usage

### Basic Commands

```bash
# Show help
dsbc --help

# Check balance with specific token
dsbc --token sk-abc123def456

# Show models and balance
dsbc --models --verbose

# Output in JSON format
dsbc --json

# Check if API is accessible
dsbc --health
```

### Environment Variables

The tool checks for API tokens in this order of priority:

1. `--token` command-line argument
2. `DEEPSEEK_API_TOKEN` environment variable (default)
3. `DEEPSEEK_TOKEN` environment variable
4. `DEEPSEEK_API_KEY` environment variable
5. `OPENAI_API_KEY` environment variable (for compatibility)

```bash
# Set default environment variable
export DEEPSEEK_API_TOKEN="sk-abc123def456"

# Or use a different variable
export DEEPSEEK_TOKEN="sk-xyz789uvw012"
```

## Examples

### Example 1: Basic Balance Check

```bash
$ dsbc
==================================================
DEEPSEEK ACCOUNT BALANCE
==================================================
Total Balance:    100.00 USD
Available Balance: 75.50 USD
Used Balance:     24.50 USD
Usage:            24.5%
Account ID:       acc_1234567890
Last Updated:     2024-01-15 14:30:00 UTC
==================================================
```

### Example 2: Check Models

```bash
$ dsbc --models
==================================================
DEEPSEEK AVAILABLE MODELS
==================================================

Model: DeepSeek Chat
  ID: deepseek-chat
  Context Window: 32768
  Pricing:
    Input:  $0.00014 per 1K tokens
    Output: $0.00028 per 1K tokens

Model: DeepSeek Coder
  ID: deepseek-coder
  Context Window: 16384
  Pricing:
    Input:  $0.00028 per 1K tokens
    Output: $0.00056 per 1K tokens
==================================================
```

### Example 3: JSON Output

```bash
$ dsbc --json
{
  "total_balance": 100.0,
  "available_balance": 75.5,
  "used_balance": 24.5,
  "currency": "USD",
  "account_id": "acc_1234567890",
  "timestamp": "2024-01-15T14:30:00Z"
}
```

### Example 4: Python Module Usage

```python
from dsbc import DeepSeekClient

# Initialize client
client = DeepSeekClient("your-api-token")

# Get balance
balance = client.get_balance()
print(f"Available: {balance['available_balance']} {balance['currency']}")

# Get models
models = client.get_models()
for model in models['data']:
    print(f"{model['name']}: ${model['pricing']['input']}/1K tokens")
```

## Repository Structure

This repository contains multiple components for interacting with DeepSeek API:

```
dsbc/
├── cli/                    # Python CLI tool (current focus)
│   ├── deepseek_balance/   # Main package
│   │   ├── __init__.py    # Package exports
│   │   ├── cli.py        # CLI interface
│   │   └── client.py     # API client
│   ├── tests/            # Test suite
│   ├── pyproject.toml    # Modern packaging config
│   ├── setup.py          # Legacy packaging support
│   ├── uv.lock           # uv lock file
│   └── requirements.txt  # pip requirements
├── .github/workflows/    # GitHub Actions
├── LICENSE               # MIT License
└── README.md            # This file

Future components may include:
- android/               # Android app/widget
- ios/                   # iOS app/widget
- web/                   # Web dashboard
- api/                   # REST API server
```

## Development

### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/ianmerlos/dsbc.git
cd dsbc/cli

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with uv (recommended)
uv pip install -e ".[dev]"

# Or install with pip
pip install -e ".[dev]"
```

### Running Tests

```bash
# Navigate to cli directory
cd cli

# Run all tests
pytest

# Run tests with coverage
pytest --cov=deepseek_balance --cov-report=html

# Run specific test file
pytest tests/test_client.py -v
```

### Code Quality

```bash
# Navigate to cli directory
cd cli

# Format code with black
black deepseek_balance tests

# Sort imports with isort
isort deepseek_balance tests

# Check code style with flake8
flake8 deepseek_balance tests

# Type checking with mypy
mypy deepseek_balance
```

### Building and Publishing

```bash
# Navigate to cli directory
cd cli

# Build package
python -m build

# Check package
twine check dist/*

# Test upload to TestPyPI
twine upload --repository testpypi dist/*

# Upload to PyPI (requires credentials)
twine upload dist/*
```

## GitHub Actions

The repository includes GitHub Actions workflow for:

1. **Automated testing** on multiple Python versions
2. **Code coverage** reporting to Codecov
3. **Automated releases** to PyPI when tags are pushed
4. **Manual releases** via workflow dispatch

### Release Process

```bash
# Create a new version tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# GitHub Actions will automatically:
# 1. Run tests on all Python versions
# 2. Build the package
# 3. Publish to PyPI
# 4. Create GitHub release
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Ensure code quality checks pass
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Security

**Important Security Notes:**

- Never commit API tokens to version control
- Use environment variables or secure secret management
- Consider using `.env` files with `.gitignore`
- Rotate tokens regularly
- Monitor usage for suspicious activity

## Support

- **Issues**: [GitHub Issues](https://github.com/ianmerlos/dsbc/issues)
- **Documentation**: [GitHub Wiki](https://github.com/ianmerlos/dsbc/wiki)
- **Email**: merlos@example.com

## Acknowledgments

- DeepSeek for providing the API
- Python community for excellent libraries
- Contributors who help improve this project

---

**Note**: This tool is not officially affiliated with DeepSeek. Use at your own risk and always review the official DeepSeek API documentation for the most up-to-date information.