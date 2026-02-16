"""
DeepSeek Balance Checker (dsbc)

A Python package for checking DeepSeek API account balances and managing API usage.
"""

__version__ = "1.0.0"
__author__ = "Ian Merlos"
__email__ = "merlos@example.com"

from .client import DeepSeekClient
from .cli import main, format_balance, format_models, get_api_token

__all__ = [
    "DeepSeekClient",
    "main",
    "format_balance",
    "format_models",
    "get_api_token",
]