"""
DeepSeek API Client

Client for interacting with DeepSeek API for balance checking and model information.
"""

import requests
from typing import Optional, Dict, Any
from datetime import datetime

# DeepSeek API endpoints
DEEPSEEK_API_BASE = "https://api.deepseek.com"
BALANCE_ENDPOINT = f"{DEEPSEEK_API_BASE}/user/balance"
MODELS_ENDPOINT = f"{DEEPSEEK_API_BASE}/models"


class DeepSeekClient:
    """Client for interacting with DeepSeek API."""
    
    def __init__(self, api_token: str):
        """
        Initialize DeepSeek client with API token.
        
        Args:
            api_token: DeepSeek API token
        """
        self.api_token = api_token
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
            "User-Agent": f"dsbc/1.0.0"
        }
    
    def get_balance(self) -> Dict[str, Any]:
        """
        Get account balance information.
        
        Returns:
            Dictionary with balance information
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        try:
            response = requests.get(BALANCE_ENDPOINT, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch balance: {e}")
    
    def get_models(self) -> Dict[str, Any]:
        """
        Get available models and their pricing.
        
        Returns:
            Dictionary with models information
            
        Raises:
            requests.exceptions.RequestException: If API request fails
        """
        try:
            response = requests.get(MODELS_ENDPOINT, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch models: {e}")
    
    def check_health(self) -> bool:
        """
        Check if API token is valid and API is accessible.
        
        Returns:
            True if API is accessible, False otherwise
        """
        try:
            response = requests.get(BALANCE_ENDPOINT, headers=self.headers, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def get_usage(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Get usage statistics for a date range.
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Dictionary with usage statistics
            
        Note: This endpoint may not be available in all DeepSeek API versions
        """
        params = {}
        if start_date:
            params["start_date"] = start_date
        if end_date:
            params["end_date"] = end_date
        
        try:
            # Note: This endpoint might be different or not available
            # Adjust based on actual DeepSeek API documentation
            response = requests.get(
                f"{DEEPSEEK_API_BASE}/usage",
                headers=self.headers,
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to fetch usage: {e}")