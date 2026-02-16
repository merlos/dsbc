# DeepSeek Balance Checker CLI

A command-line tool to check DeepSeek API account balances and view available models with pricing.

## Features

- ✅ Check account balance (total, available, used)
- ✅ View available models and their pricing
- ✅ Support for token from environment variable or command-line argument
- ✅ JSON output option for scripting
- ✅ API health check
- ✅ Verbose mode for debugging
- ✅ Clean, formatted output

## Installation

### Option 1: Install from source

```bash
# Clone the repository
git clone https://github.com/yourusername/deepseek-balance-checker.git
cd deepseek-balance-checker/cli

# Install in development mode
pip install -e .

# Or install globally
pip install .
```

### Option 2: Run directly (no installation)

```bash
# Make the script executable
chmod +x deepseek_balance.py

# Run directly
./deepseek_balance.py --help
```

## Usage

### Basic Usage

```bash
# Set environment variable
export DEEPSEEK_API_TOKEN="your-api-token-here"

# Check balance
deepseek-balance

# Or run directly
python deepseek_balance.py
```

### Command Line Options

```bash
# Show help
deepseek-balance --help

# Use specific token
deepseek-balance --token sk-abc123def456

# Show available models
deepseek-balance --models

# Show both balance and models
deepseek-balance --verbose

# JSON output (for scripting)
deepseek-balance --json

# Check API health only
deepseek-balance --health

# Verbose mode
deepseek-balance --verbose
```

### Environment Variables

The tool checks for API tokens in this order:

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
$ deepseek-balance
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
$ deepseek-balance --models
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
$ deepseek-balance --json
{
  "total_balance": 100.0,
  "available_balance": 75.5,
  "used_balance": 24.5,
  "currency": "USD",
  "account_id": "acc_1234567890",
  "timestamp": "2024-01-15T14:30:00Z"
}
```

### Example 4: Verbose Mode

```bash
$ deepseek-balance --verbose
Using API token: sk-abc1...xyz9
API Health: ✅ Healthy
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

## API Integration

### Python Module Usage

You can also use the client as a Python module:

```python
from deepseek_balance import DeepSeekClient

# Initialize client
client = DeepSeekClient("your-api-token")

# Get balance
balance = client.get_balance()
print(f"Available balance: {balance['available_balance']} {balance['currency']}")

# Get models
models = client.get_models()
for model in models['data']:
    print(f"Model: {model['name']} - {model['pricing']['input']}/1K tokens")
```

## Error Handling

The tool provides clear error messages:

```bash
# No token provided
$ deepseek-balance
Error: No API token provided. Set DEEPSEEK_API_TOKEN environment variable or use --token argument.

# Invalid token
$ deepseek-balance --token invalid-token
Error: Failed to fetch balance: 401 Client Error: Unauthorized

# Network issues
$ deepseek-balance
Error: Failed to fetch balance: HTTPSConnectionPool(host='api.deepseek.com', port=443): Max retries exceeded
```

## Development

### Project Structure

```
deepseek-balance-checker/
├── cli/
│   ├── deepseek_balance.py    # Main CLI script
│   ├── setup.py               # Package setup
│   ├── README.md              # This file
│   ├── requirements.txt       # Dependencies
│   └── tests/                 # Test files
├── docs/                      # Documentation
└── examples/                  # Usage examples
```

### Running Tests

```bash
# Install test dependencies
pip install pytest requests-mock

# Run tests
pytest tests/
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Disclaimer

This tool is not officially affiliated with DeepSeek. Use at your own risk. Always keep your API tokens secure and never commit them to version control.

## Support

- Issues: [GitHub Issues](https://github.com/yourusername/deepseek-balance-checker/issues)
- Documentation: [GitHub Wiki](https://github.com/yourusername/deepseek-balance-checker/wiki)
- Email: your.email@example.com