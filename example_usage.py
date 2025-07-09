#!/usr/bin/env python3
"""
Example usage of BasicBot class
"""

import json
from basic_bot import BasicBot


def main():
    """Example usage of BasicBot"""
    
    try:
        # Initialize bot (will use environment variables or you can pass credentials directly)
        print("Initializing BasicBot...")
        bot = BasicBot()
        
        # Get account information
        print("\n=== Getting Account Information ===")
        account_info = bot.get_account_info()
        print(json.dumps(account_info, indent=2))
        
        # Example: Place a market order (commented out for safety)
        # print("\n=== Placing Market Order ===")
        # result = bot.place_market_order("BTCUSDT", "BUY", 0.001)
        # print(json.dumps(result, indent=2))
        
        # Example: Place a limit order (commented out for safety)
        # print("\n=== Placing Limit Order ===")
        # result = bot.place_limit_order("BTCUSDT", "SELL", 0.001, 50000)
        # print(json.dumps(result, indent=2))
        
        # Example: Place a stop market order (commented out for safety)
        # print("\n=== Placing Stop Market Order ===")
        # result = bot.place_stop_market_order("BTCUSDT", "SELL", 0.001, 45000)
        # print(json.dumps(result, indent=2))
        
        print("\n=== Example completed successfully ===")
        print("Check logs/bot.log for detailed logs")
        
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main() 