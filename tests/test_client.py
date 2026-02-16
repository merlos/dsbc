"""
Tests for DeepSeekClient
"""

import pytest
from unittest.mock import Mock, patch
from deepseek_balance.client import DeepSeekClient


def test_client_initialization():
    """Test that client initializes correctly."""
    client = DeepSeekClient("test-token-123")
    assert client.api_token == "test-token-123"
    assert "Authorization" in client.headers
    assert client.headers["Authorization"] == "Bearer test-token-123"
    assert "User-Agent" in client.headers
    assert "dsbc" in client.headers["User-Agent"]


@patch("deepseek_balance.client.requests.get")
def test_get_balance_success(mock_get):
    """Test successful balance retrieval."""
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "total_balance": 100.0,
        "available_balance": 75.5,
        "used_balance": 24.5,
        "currency": "USD",
        "account_id": "acc_123",
        "timestamp": "2024-01-15T14:30:00Z"
    }
    mock_get.return_value = mock_response
    
    # Test client
    client = DeepSeekClient("test-token")
    balance = client.get_balance()
    
    # Verify
    assert balance["total_balance"] == 100.0
    assert balance["available_balance"] == 75.5
    assert balance["currency"] == "USD"
    
    # Verify API call
    mock_get.assert_called_once()
    call_args = mock_get.call_args
    assert "https://api.deepseek.com/user/balance" in str(call_args[0])
    assert "Authorization" in call_args[1]["headers"]


@patch("deepseek_balance.client.requests.get")
def test_get_balance_failure(mock_get):
    """Test balance retrieval failure."""
    # Mock failed response
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.raise_for_status.side_effect = Exception("Unauthorized")
    mock_get.return_value = mock_response
    
    # Test client
    client = DeepSeekClient("invalid-token")
    
    with pytest.raises(Exception, match="Failed to fetch balance"):
        client.get_balance()


@patch("deepseek_balance.client.requests.get")
def test_get_models_success(mock_get):
    """Test successful models retrieval."""
    # Mock response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
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
    mock_get.return_value = mock_response
    
    # Test client
    client = DeepSeekClient("test-token")
    models = client.get_models()
    
    # Verify
    assert "data" in models
    assert len(models["data"]) == 1
    assert models["data"][0]["id"] == "deepseek-chat"
    assert models["data"][0]["name"] == "DeepSeek Chat"


@patch("deepseek_balance.client.requests.get")
def test_check_health_success(mock_get):
    """Test health check success."""
    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_get.return_value = mock_response
    
    client = DeepSeekClient("test-token")
    assert client.check_health() is True


@patch("deepseek_balance.client.requests.get")
def test_check_health_failure(mock_get):
    """Test health check failure."""
    # Mock failed response
    mock_response = Mock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response
    
    client = DeepSeekClient("invalid-token")
    assert client.check_health() is False


@patch("deepseek_balance.client.requests.get")
def test_check_health_exception(mock_get):
    """Test health check with exception."""
    # Mock exception
    mock_get.side_effect = Exception("Network error")
    
    client = DeepSeekClient("test-token")
    assert client.check_health() is False


def test_formatting_functions():
    """Test the formatting functions."""
    from deepseek_balance.cli import format_balance, format_models
    
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
    assert "24.50 USD" in formatted
    assert "acc_123456" in formatted
    
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
    assert "deepseek-chat" in formatted
    assert "32768" in formatted