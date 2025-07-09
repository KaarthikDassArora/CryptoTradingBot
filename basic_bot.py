#!/usr/bin/env python3
"""
BasicBot - A reusable Python class for Binance USDT-M Futures Testnet
"""

import os
import json
import logging
import argparse
from datetime import datetime
from typing import Dict, Any, Optional
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from dotenv import load_dotenv


class BasicBot:
    """
    A reusable bot class for Binance USDT-M Futures Testnet trading
    """
    
    def __init__(self, api_key: str = None, api_secret: str = None, demo: bool = False):
        """
        Initialize the BasicBot with API credentials
        
        Args:
            api_key (str): Binance API key
            api_secret (str): Binance API secret
            demo (bool): If True, run in demo mode (no real API calls)
        """
        # Load environment variables
        load_dotenv()
        
        self.demo = demo
        # Setup logging
        self._setup_logging()
        if self.demo:
            self.logger.info("BasicBot initialized in DEMO MODE (no real API calls)")
            self.api_key = None
            self.api_secret = None
            self.client = None
        else:
            # Get API credentials from environment or parameters
            self.api_key = api_key or os.getenv('BINANCE_API_KEY')
            self.api_secret = api_secret or os.getenv('BINANCE_API_SECRET')
            if not self.api_key or not self.api_secret:
                raise ValueError("API credentials are required. Set BINANCE_API_KEY and BINANCE_API_SECRET environment variables or pass them as parameters.")
            # Initialize Binance client for testnet
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=True,  # Enable testnet mode
                base_url="https://testnet.binancefuture.com"  # Testnet endpoint
            )
            self.logger.info("BasicBot initialized successfully in testnet mode")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/bot.log'),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('BasicBot')
    
    def _validate_symbol(self, symbol: str) -> str:
        """
        Validate and format symbol
        
        Args:
            symbol (str): Trading symbol
            
        Returns:
            str: Formatted symbol
        """
        if not symbol:
            raise ValueError("Symbol cannot be empty")
        
        # Convert to uppercase and remove spaces
        symbol = symbol.upper().strip()
        
        # Basic validation for USDT pairs
        if not symbol.endswith('USDT'):
            raise ValueError("Symbol must end with USDT for USDT-M Futures")
        
        return symbol
    
    def _validate_quantity(self, quantity: float) -> float:
        """
        Validate quantity
        
        Args:
            quantity (float): Order quantity
            
        Returns:
            float: Validated quantity
        """
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        
        return quantity
    
    def _validate_price(self, price: float) -> float:
        """
        Validate price
        
        Args:
            price (float): Order price
            
        Returns:
            float: Validated price
        """
        if price <= 0:
            raise ValueError("Price must be greater than 0")
        
        return price
    
    def _validate_side(self, side: str) -> str:
        """
        Validate order side
        
        Args:
            side (str): Order side (BUY/SELL)
            
        Returns:
            str: Validated side
        """
        side = side.upper().strip()
        if side not in ['BUY', 'SELL']:
            raise ValueError("Side must be either 'BUY' or 'SELL'")
        
        return side
    
    def _log_api_request(self, method: str, endpoint: str, params: Dict = None):
        """Log API request details"""
        self.logger.info(f"API Request - Method: {method}, Endpoint: {endpoint}")
        if params:
            self.logger.info(f"API Request Parameters: {json.dumps(params, indent=2)}")
    
    def _log_api_response(self, response: Dict):
        """Log API response details"""
        self.logger.info(f"API Response: {json.dumps(response, indent=2)}")
    
    def _log_error(self, error: Exception, context: str = ""):
        """Log error details"""
        self.logger.error(f"Error in {context}: {str(error)}")
        if hasattr(error, 'response'):
            self.logger.error(f"Error Response: {error.response.text if error.response else 'No response'}")
    
    def place_market_order(self, symbol: str, side: str, quantity: float) -> Dict[str, Any]:
        """
        Place a market order
        
        Args:
            symbol (str): Trading symbol (e.g., BTCUSDT)
            side (str): Order side (BUY/SELL)
            quantity (float): Order quantity
            
        Returns:
            Dict[str, Any]: Order response
        """
        try:
            # Validate inputs
            symbol = self._validate_symbol(symbol)
            side = self._validate_side(side)
            quantity = self._validate_quantity(quantity)
            
            self.logger.info(f"Placing market order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}")
            
            if self.demo:
                # Simulate a market order response
                response = {
                    'orderId': 123456,
                    'clientOrderId': 'demo123',
                    'avgPrice': '50000.00',
                    'status': 'FILLED'
                }
            else:
                # Prepare order parameters
                params = {
                    'symbol': symbol,
                    'side': side,
                    'type': 'MARKET',
                    'quantity': quantity
                }
                self._log_api_request('POST', '/fapi/v1/order', params)
                response = self.client.futures_create_order(**params)
                self._log_api_response(response)
            formatted_response = {
                'status': 'SUCCESS',
                'order_type': 'MARKET',
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'order_id': response.get('orderId'),
                'client_order_id': response.get('clientOrderId'),
                'price': response.get('avgPrice', 'N/A'),
                'status': response.get('status'),
                'timestamp': datetime.now().isoformat(),
                'raw_response': response
            }
            self.logger.info(f"Market order placed successfully - Order ID: {formatted_response.get('order_id')}")
            return formatted_response
            
        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_error(e, "place_market_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_error(e, "place_market_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def place_limit_order(self, symbol: str, side: str, quantity: float, price: float) -> Dict[str, Any]:
        """
        Place a limit order
        
        Args:
            symbol (str): Trading symbol (e.g., BTCUSDT)
            side (str): Order side (BUY/SELL)
            quantity (float): Order quantity
            price (float): Order price
            
        Returns:
            Dict[str, Any]: Order response
        """
        try:
            # Validate inputs
            symbol = self._validate_symbol(symbol)
            side = self._validate_side(side)
            quantity = self._validate_quantity(quantity)
            price = self._validate_price(price)
            
            self.logger.info(f"Placing limit order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Price: {price}")
            
            if self.demo:
                response = {
                    'orderId': 234567,
                    'clientOrderId': 'demoLimit',
                    'status': 'NEW'
                }
            else:
                params = {
                    'symbol': symbol,
                    'side': side,
                    'type': 'LIMIT',
                    'timeInForce': 'GTC',
                    'quantity': quantity,
                    'price': price
                }
                self._log_api_request('POST', '/fapi/v1/order', params)
                response = self.client.futures_create_order(**params)
                self._log_api_response(response)
            formatted_response = {
                'status': 'SUCCESS',
                'order_type': 'LIMIT',
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'price': price,
                'order_id': response.get('orderId'),
                'client_order_id': response.get('clientOrderId'),
                'status': response.get('status'),
                'timestamp': datetime.now().isoformat(),
                'raw_response': response
            }
            self.logger.info(f"Limit order placed successfully - Order ID: {formatted_response.get('order_id')}")
            return formatted_response
            
        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_error(e, "place_limit_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_error(e, "place_limit_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def place_stop_market_order(self, symbol: str, side: str, quantity: float, stop_price: float) -> Dict[str, Any]:
        """
        Place a stop market order
        
        Args:
            symbol (str): Trading symbol (e.g., BTCUSDT)
            side (str): Order side (BUY/SELL)
            quantity (float): Order quantity
            stop_price (float): Stop price
            
        Returns:
            Dict[str, Any]: Order response
        """
        try:
            # Validate inputs
            symbol = self._validate_symbol(symbol)
            side = self._validate_side(side)
            quantity = self._validate_quantity(quantity)
            stop_price = self._validate_price(stop_price)
            
            self.logger.info(f"Placing stop market order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Stop Price: {stop_price}")
            
            if self.demo:
                response = {
                    'orderId': 345678,
                    'clientOrderId': 'demoStop',
                    'status': 'NEW'
                }
            else:
                # Prepare order parameters
                params = {
                    'symbol': symbol,
                    'side': side,
                    'type': 'STOP_MARKET',
                    'quantity': quantity,
                    'stopPrice': stop_price
                }
                
                self._log_api_request('POST', '/fapi/v1/order', params)
                
                # Place order
                response = self.client.futures_create_order(**params)
                
                self._log_api_response(response)
            
            # Format response for output
            formatted_response = {
                'status': 'SUCCESS',
                'order_type': 'STOP_MARKET',
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'stop_price': stop_price,
                'order_id': response.get('orderId'),
                'client_order_id': response.get('clientOrderId'),
                'status': response.get('status'),
                'timestamp': datetime.now().isoformat(),
                'raw_response': response
            }
            
            self.logger.info(f"Stop market order placed successfully - Order ID: {formatted_response.get('order_id')}")
            return formatted_response
            
        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_error(e, "place_stop_market_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_error(e, "place_stop_market_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_account_info(self) -> Dict[str, Any]:
        """
        Get account information
        
        Returns:
            Dict[str, Any]: Account information
        """
        try:
            self.logger.info("Fetching account information")
            if self.demo:
                response = {
                    'totalWalletBalance': '10000.00',
                    'totalUnrealizedProfit': '0.00',
                    'assets': [
                        {'asset': 'USDT', 'walletBalance': '10000.00', 'unrealizedProfit': '0.00'}
                    ]
                }
                return {
                    'status': 'SUCCESS',
                    'account_info': response,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                response = self.client.futures_account()
                self._log_api_response(response)
                return {
                    'status': 'SUCCESS',
                    'account_info': response,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            self._log_error(e, "get_account_info")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def place_oco_order(self, symbol: str, side: str, quantity: float, limit_price: float, stop_price: float, stop_limit_price: float) -> Dict[str, Any]:
        """
        Place an OCO (One-Cancels-the-Other) order
        
        Args:
            symbol (str): Trading symbol (e.g., BTCUSDT)
            side (str): Order side (BUY/SELL)
            quantity (float): Order quantity
            limit_price (float): Limit order price
            stop_price (float): Stop price
            stop_limit_price (float): Stop limit price
            
        Returns:
            Dict[str, Any]: Order response
        """
        try:
            # Validate inputs
            symbol = self._validate_symbol(symbol)
            side = self._validate_side(side)
            quantity = self._validate_quantity(quantity)
            limit_price = self._validate_price(limit_price)
            stop_price = self._validate_price(stop_price)
            stop_limit_price = self._validate_price(stop_limit_price)
            
            self.logger.info(f"Placing OCO order - Symbol: {symbol}, Side: {side}, Quantity: {quantity}, Limit Price: {limit_price}, Stop Price: {stop_price}, Stop Limit Price: {stop_limit_price}")
            
            if self.demo:
                response = {
                    'orderListId': 456789,
                    'contingencyType': 'OCO',
                    'listStatusType': 'RESPONSE',
                    'listOrderStatus': 'EXEC_STARTED',
                    'listClientOrderId': 'demoOCO'
                }
            else:
                # Prepare OCO order parameters
                params = {
                    'symbol': symbol,
                    'side': side,
                    'quantity': quantity,
                    'price': limit_price,
                    'stopPrice': stop_price,
                    'stopLimitPrice': stop_limit_price,
                    'stopLimitTimeInForce': 'GTC'
                }
                
                self._log_api_request('POST', '/fapi/v1/order/oco', params)
                
                # Place OCO order
                response = self.client.futures_create_oco_order(**params)
                
                self._log_api_response(response)
            
            # Format response for output
            formatted_response = {
                'status': 'SUCCESS',
                'order_type': 'OCO',
                'symbol': symbol,
                'side': side,
                'quantity': quantity,
                'limit_price': limit_price,
                'stop_price': stop_price,
                'stop_limit_price': stop_limit_price,
                'order_list_id': response.get('orderListId'),
                'contingency_type': response.get('contingencyType'),
                'list_status_type': response.get('listStatusType'),
                'list_order_status': response.get('listOrderStatus'),
                'timestamp': datetime.now().isoformat(),
                'raw_response': response
            }
            
            self.logger.info(f"OCO order placed successfully - Order List ID: {formatted_response.get('order_list_id')}")
            return formatted_response
            
        except (BinanceAPIException, BinanceOrderException) as e:
            self._log_error(e, "place_oco_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            self._log_error(e, "place_oco_order")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }

    def get_order_status(self, symbol: str, order_id: int) -> Dict[str, Any]:
        """
        Get order status
        
        Args:
            symbol (str): Trading symbol
            order_id (int): Order ID
            
        Returns:
            Dict[str, Any]: Order status
        """
        try:
            symbol = self._validate_symbol(symbol)
            
            self.logger.info(f"Fetching order status - Symbol: {symbol}, Order ID: {order_id}")
            
            if self.demo:
                response = {
                    'orderId': order_id,
                    'symbol': symbol,
                    'status': 'FILLED',
                    'price': '50000.00',
                    'avgPrice': '50000.00',
                    'executedQty': '0.001'
                }
            else:
                response = self.client.futures_get_order(symbol=symbol, orderId=order_id)
                self._log_api_response(response)
            
            return {
                'status': 'SUCCESS',
                'order_status': response,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            self._log_error(e, "get_order_status")
            return {
                'status': 'ERROR',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }


def main():
    """Main entry point for CLI interface"""
    parser = argparse.ArgumentParser(description='BasicBot - Binance USDT-M Futures Testnet Trading Bot')
    parser.add_argument('--api-key', help='Binance API Key')
    parser.add_argument('--api-secret', help='Binance API Secret')
    parser.add_argument('--demo', action='store_true', help='Run in demo mode (no real API calls)')
    parser.add_argument('--symbol', help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('--order-type', choices=['MARKET', 'LIMIT', 'STOP_MARKET', 'OCO'], help='Order type')
    parser.add_argument('--quantity', type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Order price (for LIMIT orders)')
    parser.add_argument('--stop-price', type=float, help='Stop price (for STOP_MARKET orders)')
    parser.add_argument('--limit-price', type=float, help='Limit price (for OCO orders)')
    parser.add_argument('--stop-limit-price', type=float, help='Stop limit price (for OCO orders)')
    parser.add_argument('--account-info', action='store_true', help='Get account information')
    
    args = parser.parse_args()
    
    try:
        # Initialize bot
        bot = BasicBot(api_key=args.api_key, api_secret=args.api_secret, demo=args.demo)
        
        # Handle account info request
        if args.account_info:
            result = bot.get_account_info()
            print(json.dumps(result, indent=2))
            return
        
        # Validate required arguments for order placement
        if not all([args.symbol, args.side, args.order_type, args.quantity]):
            print("Error: symbol, side, order-type, and quantity are required for order placement")
            return
        
        # Place order based on type
        if args.order_type == 'MARKET':
            result = bot.place_market_order(args.symbol, args.side, args.quantity)
        elif args.order_type == 'LIMIT':
            if not args.price:
                print("Error: price is required for LIMIT orders")
                return
            result = bot.place_limit_order(args.symbol, args.side, args.quantity, args.price)
        elif args.order_type == 'STOP_MARKET':
            if not args.stop_price:
                print("Error: stop-price is required for STOP_MARKET orders")
                return
            result = bot.place_stop_market_order(args.symbol, args.side, args.quantity, args.stop_price)
        elif args.order_type == 'OCO':
            if not all([args.limit_price, args.stop_price, args.stop_limit_price]):
                print("Error: limit-price, stop-price, and stop-limit-price are required for OCO orders")
                return
            result = bot.place_oco_order(args.symbol, args.side, args.quantity, args.limit_price, args.stop_price, args.stop_limit_price)
        else:
            print(f"Error: Unsupported order type: {args.order_type}")
            return
        
        # Print result
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 