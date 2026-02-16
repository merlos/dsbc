# dsbc CLI - DeepSeek Balance Checker

This is the CLI component of the dsbc (DeepSeek Tools Collection). It's a Python command-line tool to check DeepSeek API account balances and view available models.

## Installation

### From PyPI

```bash
pip install dsbc
```

### From source

```bash
# From the repository root
cd cli
pip install -e .
```

## Usage

```bash
# Set your API token
export DEEPSEEK_API_TOKEN="your-token-here"

# Check balance
dsbc

# View models
dsbc --models

# JSON output
dsbc --json

# Health check
dsbc --health
```

## Development

See the main [README.md](../README.md) for development instructions.

## Project Structure

```
cli/
├── deepseek_balance/     # Main Python package
│   ├── __init__.py      # Package exports
│   ├── cli.py          # CLI interface (dsbc command)
│   └── client.py       # API client
├── tests/              # Test suite
├── pyproject.toml     # Modern packaging config
├── setup.py           # Legacy packaging support
├── uv.lock           # uv lock file
├── requirements.txt   # pip requirements
└── README.md         # This file
```

## License

MIT - See [LICENSE](../LICENSE) file.