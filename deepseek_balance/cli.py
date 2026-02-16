#!/usr/bin/env python3
"""
DeepSeek Balance Checker CLI

A command-line tool to check DeepSeek API account balances.
Supports token from environment variable or command-line argument.
"""

import os
import sys
import argparse
import json
from typing import Optional, Dict, Any
from datetime import datetime

from .client import DeepSeekClient

# Default environment variable name
DEFAULT_ENV_VAR = "DEEPSEEK_API_TOKEN"

def format_balance(balance_data: Dict[str, Any]) -> str:
    """
    Format balance information for display.
    
    Args:
        balance_data: Raw balance data from API
        
    Returns:
        Formatted string with balance information
    """
    if not balance_data:
        return "No balance data received"
    
    output = []
    output.append("=" * 50)
    output.append("DEEPSEEK ACCOUNT BALANCE")
    output.append("=" * 50)
    
    # Extract balance information
    total_balance = balance_data.get("total_balance", 0)
    available_balance = balance_data.get("available_balance", 0)
    used_balance = balance_data.get("used_balance", 0)
    currency = balance_data.get("currency", "USD")
    
    output.append(f"Total Balance:    {total_balance:.2f} {currency}")
    output.append(f"Available Balance: {available_balance:.2f} {currency}")
    output.append(f"Used Balance:     {used_balance:.2f} {currency}")
    
    # Add usage percentage if total balance > 0
    if total_balance > 0:
        usage_percentage = (used_balance / total_balance) * 100
        output.append(f"Usage:            {usage_percentage:.1f}%")
    
    # Add account info if available
    account_id = balance_data.get("account_id")
    if account_id:
        output.append(f"Account ID:       {account_id}")
    
    # Add timestamp
    timestamp = balance_data.get("timestamp")
    if timestamp:
        try:
            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            output.append(f"Last Updated:     {dt.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        except:
            output.append(f"Last Updated:     {timestamp}")
    
    output.append("=" * 50)
    return "\n".join(output)

def format_models(models_data: Dict[str, Any]) -> str:
    """
    Format models information for display.
    
    Args:
        models_data: Raw models data from API
        
    Returns:
        Formatted string with models information
    """
    if not models_data or "data" not in models_data:
        return "No models data received"
    
    output = []
    output.append("=" * 50)
    output.append("DEEPSEEK AVAILABLE MODELS")
    output.append("=" * 50)
    
    models = models_data.get("data", [])
    if not models:
        output.append("No models available")
        output.append("=" * 50)
        return "\n".join(output)
    
    for model in models:
        model_id = model.get("id", "Unknown")
        model_name = model.get("name", model_id)
        
        # Pricing information
        pricing = model.get("pricing", {})
        input_price = pricing.get("input", "N/A")
        output_price = pricing.get("output", "N/A")
        
        # Context window
        context_window = model.get("context_window", "N/A")
        
        output.append(f"\nModel: {model_name}")
        output.append(f"  ID: {model_id}")
        output.append(f"  Context Window: {context_window}")
        output.append(f"  Pricing:")
        output.append(f"    Input:  ${input_price} per 1K tokens")
        output.append(f"    Output: ${output_price} per 1K tokens")
    
    output.append("\n" + "=" * 50)
    return "\n".join(output)

def get_api_token(args_token: Optional[str] = None) -> str:
    """
    Get API token from command line argument or environment variable.
    
    Args:
        args_token: Token from command line argument
        
    Returns:
        API token
        
    Raises:
        ValueError: If no token is found
    """
    # Priority: 1. Command line argument, 2. Environment variable
    if args_token:
        return args_token
    
    env_token = os.getenv(DEFAULT_ENV_VAR)
    if env_token:
        return env_token
    
    # Check for other common environment variable names
    common_env_vars = ["DEEPSEEK_TOKEN", "DEEPSEEK_API_KEY", "OPENAI_API_KEY"]
    for env_var in common_env_vars:
        token = os.getenv(env_var)
        if token:
            print(f"Note: Using token from {env_var} environment variable", file=sys.stderr)
            return token
    
    raise ValueError(
        f"No API token provided. "
        f"Set {DEFAULT_ENV_VAR} environment variable or use --token argument."
    )

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Check DeepSeek API account balance and available models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Examples:
  %(prog)s                          # Use {DEFAULT_ENV_VAR} environment variable
  %(prog)s --token sk-abc123        # Use provided token
  %(prog)s --models                 # Show available models
  %(prog)s --verbose                # Show detailed information
  %(prog)s --json                   # Output in JSON format

Environment Variables:
  {DEFAULT_ENV_VAR}: Default API token
  DEEPSEEK_TOKEN: Alternative token variable
  DEEPSEEK_API_KEY: Alternative token variable
        """
    )
    
    parser.add_argument(
        "--token", "-t",
        help=f"DeepSeek API token (default: from {DEFAULT_ENV_VAR} env var)"
    )
    
    parser.add_argument(
        "--models", "-m",
        action="store_true",
        help="Show available models and pricing"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose output including API health check"
    )
    
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="Output in JSON format"
    )
    
    parser.add_argument(
        "--health", "-H",
        action="store_true",
        help="Check API health only"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="deepseek-balance-checker 1.0.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Get API token
        api_token = get_api_token(args.token)
        
        # Initialize client
        client = DeepSeekClient(api_token)
        
        # Health check
        if args.health:
            is_healthy = client.check_health()
            if args.json:
                print(json.dumps({"healthy": is_healthy}, indent=2))
            else:
                print("✅ API is accessible" if is_healthy else "❌ API is not accessible")
            sys.exit(0 if is_healthy else 1)
        
        # Verbose output
        if args.verbose:
            print(f"Using API token: {api_token[:8]}...{api_token[-4:]}")
            is_healthy = client.check_health()
            print(f"API Health: {'✅ Healthy' if is_healthy else '❌ Unhealthy'}")
            if not is_healthy:
                print("Warning: API may not be accessible", file=sys.stderr)
        
        # Get models if requested
        if args.models:
            models_data = client.get_models()
            if args.json:
                print(json.dumps(models_data, indent=2))
            else:
                print(format_models(models_data))
        
        # Always get balance (unless only models requested without balance)
        if not args.models or args.verbose:
            balance_data = client.get_balance()
            if args.json:
                print(json.dumps(balance_data, indent=2))
            else:
                print(format_balance(balance_data))
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()