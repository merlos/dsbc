#!/usr/bin/env python3
"""
Example test script for DeepSeek Balance Checker.
This demonstrates how to use the CLI programmatically.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add parent directory to path to import the module
sys.path.insert(0, str(Path(__file__).parent))

def test_cli_help():
    """Test that the CLI shows help."""
    print("Testing CLI help...")
    result = subprocess.run(
        [sys.executable, "deepseek_balance.py", "--help"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "usage:" in result.stdout.lower()
    print("✓ Help command works")

def test_module_import():
    """Test that the module can be imported."""
    print("Testing module import...")
    try:
        from deepseek_balance import DeepSeekClient, format_balance, get_api_token
        print("✓ Module imports successfully")
        return True
    except ImportError as e:
        print(f"✗ Failed to import module: {e}")
        return False

def test_client_class():
    """Test the DeepSeekClient class structure."""
    print("Testing client class...")
    from deepseek_balance import DeepSeekClient
    
    # Test initialization
    client = DeepSeekClient("test-token")
    assert client.api_token == "test-token"
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == "Bearer test-token"
    print("✓ Client initializes correctly")

def test_format_functions():
    """Test the formatting functions."""
    print("Testing formatting functions...")
    from deepseek_balance import format_balance, format_models
    
    # Test balance formatting
    balance_data = {
        "total_balance": 100.0,
        "available_balance": 75.5,
        "used_balance": 24.5,
        "currency": "USD",
        "account_id": "acc_123456",
        "timestamp": "2024-01-15T14:30:00Z"
    }
    
    formatted = format_balance(balance_data)
    assert "DEEPSEEK ACCOUNT BALANCE" in formatted
    assert "100.00 USD" in formatted
    assert "75.50 USD" in formatted
    print("✓ Balance formatting works")
    
    # Test models formatting
    models_data = {
        "data": [
            {
                "id": "deepseek-chat",
                "name": "DeepSeek Chat",
                "context_window": 32768,
                "pricing": {
                    "input": "0.00014",
                    "output": "0.00028"
                }
            }
        ]
    }
    
    formatted = format_models(models_data)
    assert "DEEPSEEK AVAILABLE MODELS" in formatted
    assert "DeepSeek Chat" in formatted
    print("✓ Models formatting works")

def test_token_priority():
    """Test token priority logic."""
    print("Testing token priority...")
    from deepseek_balance import get_api_token
    
    # Save original environment
    original_env = os.environ.copy()
    
    try:
        # Test 1: Command line argument should take priority
        os.environ["DEEPSEEK_API_TOKEN"] = "env-token"
        token = get_api_token("arg-token")
        assert token == "arg-token"
        print("✓ Command line argument has priority")
        
        # Test 2: Environment variable
        token = get_api_token(None)
        assert token == "env-token"
        print("✓ Environment variable works")
        
        # Test 3: Alternative environment variables
        del os.environ["DEEPSEEK_API_TOKEN"]
        os.environ["DEEPSEEK_TOKEN"] = "alt-token"
        token = get_api_token(None)
        assert token == "alt-token"
        print("✓ Alternative env var works")
        
    finally:
        # Restore environment
        os.environ.clear()
        os.environ.update(original_env)

def main():
    """Run all tests."""
    print("=" * 60)
    print("DeepSeek Balance Checker - Test Suite")
    print("=" * 60)
    
    tests = [
        test_cli_help,
        test_module_import,
        test_client_class,
        test_format_functions,
        test_token_priority,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())