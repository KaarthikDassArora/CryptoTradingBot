#!/usr/bin/env python3
"""
Test script for BasicBot functionality
"""

import unittest
from unittest.mock import Mock, patch
from basic_bot import BasicBot


class TestBasicBot(unittest.TestCase):
    """Test cases for BasicBot class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock API credentials for testing
        self.api_key = "test_api_key"
        self.api_secret = "test_api_secret"
        
        # Mock the Binance client
        with patch('basic_bot.Client') as mock_client:
            self.mock_client = mock_client.return_value
            self.bot = BasicBot(self.api_key, self.api_secret)
    
    def test_validate_symbol(self):
        """Test symbol validation"""
        # Valid symbols
        self.assertEqual(self.bot._validate_symbol("BTCUSDT"), "BTCUSDT")
        self.assertEqual(self.bot._validate_symbol("ethusdt"), "ETHUSDT")
        self.assertEqual(self.bot._validate_symbol("  btcusdt  "), "BTCUSDT")
        
        # Invalid symbols
        with self.assertRaises(ValueError):
            self.bot._validate_symbol("")
        with self.assertRaises(ValueError):
            self.bot._validate_symbol("BTC")
        with self.assertRaises(ValueError):
            self.bot._validate_symbol("BTCUSD")
    
    def test_validate_side(self):
        """Test side validation"""
        # Valid sides
        self.assertEqual(self.bot._validate_side("BUY"), "BUY")
        self.assertEqual(self.bot._validate_side("SELL"), "SELL")
        self.assertEqual(self.bot._validate_side("buy"), "BUY")
        self.assertEqual(self.bot._validate_side("sell"), "SELL")
        
        # Invalid sides
        with self.assertRaises(ValueError):
            self.bot._validate_side("INVALID")
        with self.assertRaises(ValueError):
            self.bot._validate_side("")
    
    def test_validate_quantity(self):
        """Test quantity validation"""
        # Valid quantities
        self.assertEqual(self.bot._validate_quantity(0.001), 0.001)
        self.assertEqual(self.bot._validate_quantity(1.0), 1.0)
        self.assertEqual(self.bot._validate_quantity(100), 100)
        
        # Invalid quantities
        with self.assertRaises(ValueError):
            self.bot._validate_quantity(0)
        with self.assertRaises(ValueError):
            self.bot._validate_quantity(-1)
    
    def test_validate_price(self):
        """Test price validation"""
        # Valid prices
        self.assertEqual(self.bot._validate_price(50000), 50000)
        self.assertEqual(self.bot._validate_price(0.001), 0.001)
        
        # Invalid prices
        with self.assertRaises(ValueError):
            self.bot._validate_price(0)
        with self.assertRaises(ValueError):
            self.bot._validate_price(-1)
    
    def test_place_market_order_success(self):
        """Test successful market order placement"""
        # Mock successful response
        mock_response = {
            'orderId': 123456789,
            'clientOrderId': 'test123',
            'avgPrice': '50000.00',
            'status': 'FILLED'
        }
        self.mock_client.futures_create_order.return_value = mock_response
        
        result = self.bot.place_market_order("BTCUSDT", "BUY", 0.001)
        
        # Verify the result
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertEqual(result['order_type'], 'MARKET')
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'BUY')
        self.assertEqual(result['quantity'], 0.001)
        self.assertEqual(result['order_id'], 123456789)
        
        # Verify the API call
        self.mock_client.futures_create_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='BUY',
            type='MARKET',
            quantity=0.001
        )
    
    def test_place_limit_order_success(self):
        """Test successful limit order placement"""
        # Mock successful response
        mock_response = {
            'orderId': 123456789,
            'clientOrderId': 'test123',
            'status': 'NEW'
        }
        self.mock_client.futures_create_order.return_value = mock_response
        
        result = self.bot.place_limit_order("BTCUSDT", "SELL", 0.001, 50000)
        
        # Verify the result
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertEqual(result['order_type'], 'LIMIT')
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'SELL')
        self.assertEqual(result['quantity'], 0.001)
        self.assertEqual(result['price'], 50000)
        
        # Verify the API call
        self.mock_client.futures_create_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='SELL',
            type='LIMIT',
            timeInForce='GTC',
            quantity=0.001,
            price=50000
        )
    
    def test_place_stop_market_order_success(self):
        """Test successful stop market order placement"""
        # Mock successful response
        mock_response = {
            'orderId': 123456789,
            'clientOrderId': 'test123',
            'status': 'NEW'
        }
        self.mock_client.futures_create_order.return_value = mock_response
        
        result = self.bot.place_stop_market_order("BTCUSDT", "SELL", 0.001, 45000)
        
        # Verify the result
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertEqual(result['order_type'], 'STOP_MARKET')
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'SELL')
        self.assertEqual(result['quantity'], 0.001)
        self.assertEqual(result['stop_price'], 45000)
        
        # Verify the API call
        self.mock_client.futures_create_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='SELL',
            type='STOP_MARKET',
            quantity=0.001,
            stopPrice=45000
        )
    
    def test_place_oco_order_success(self):
        """Test successful OCO order placement"""
        # Mock successful response
        mock_response = {
            'orderListId': 123456789,
            'contingencyType': 'OCO',
            'listStatusType': 'RESPONSE',
            'listOrderStatus': 'EXEC_STARTED',
            'listClientOrderId': 'test123'
        }
        self.mock_client.futures_create_oco_order.return_value = mock_response
        
        result = self.bot.place_oco_order("BTCUSDT", "SELL", 0.001, 50000, 45000, 44900)
        
        # Verify the result
        self.assertEqual(result['status'], 'SUCCESS')
        self.assertEqual(result['order_type'], 'OCO')
        self.assertEqual(result['symbol'], 'BTCUSDT')
        self.assertEqual(result['side'], 'SELL')
        self.assertEqual(result['quantity'], 0.001)
        self.assertEqual(result['limit_price'], 50000)
        self.assertEqual(result['stop_price'], 45000)
        self.assertEqual(result['stop_limit_price'], 44900)
        
        # Verify the API call
        self.mock_client.futures_create_oco_order.assert_called_once_with(
            symbol='BTCUSDT',
            side='SELL',
            quantity=0.001,
            price=50000,
            stopPrice=45000,
            stopLimitPrice=44900,
            stopLimitTimeInForce='GTC'
        )
    
    def test_api_error_handling(self):
        """Test API error handling"""
        # Mock API error
        from binance.exceptions import BinanceAPIException
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.text = '{"code": -1013, "msg": "Invalid symbol."}'
        
        self.mock_client.futures_create_order.side_effect = BinanceAPIException(
            response=mock_response,
            status_code=400,
            text='{"code": -1013, "msg": "Invalid symbol."}'
        )
        
        result = self.bot.place_market_order("INVALID", "BUY", 0.001)
        
        # Verify error handling
        self.assertEqual(result['status'], 'ERROR')
        self.assertIn('error', result)


def run_tests():
    """Run all tests"""
    print("Running BasicBot tests...")
    unittest.main(verbosity=2)


if __name__ == "__main__":
    run_tests() 