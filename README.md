# BasicBot - Binance USDT-M Futures Testnet Trading Bot

A reusable Python class for trading on Binance USDT-M Futures Testnet using the official `python-binance` library.

## Features

- ✅ **Testnet Mode**: Configured for Binance Futures Testnet
- ✅ **Multiple Order Types**: Market, Limit, Stop Market, and OCO orders
- ✅ **Input Validation**: Comprehensive validation for all inputs
- ✅ **Exception Handling**: Proper error handling and logging
- ✅ **CLI Interface**: Command-line interface for easy usage
- ✅ **GUI Interface**: Modern graphical user interface
- ✅ **Logging**: Detailed logging to `logs/bot.log`
- ✅ **Formatted Output**: JSON-formatted responses

## Installation

1. Clone or download the project files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

### GUI Requirements

The GUI uses tkinter which is included with Python. If you're on Linux and tkinter is missing:
```bash
sudo apt-get install python3-tk
```

## Setup

### 1. Get Binance Testnet API Credentials

1. Visit [Binance Testnet](https://testnet.binancefuture.com/)
2. Create an account and log in
3. Go to API Management
4. Create a new API key
5. Save your API Key and Secret

### 2. Configure API Credentials

**Option A: Environment Variables (Recommended)**
Create a `.env` file in the project root:
```env
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Option B: Command Line Arguments**
Pass credentials directly via command line arguments (see usage examples below)

## Usage

### GUI Interface (Recommended)

Launch the graphical interface:
```bash
python gui_bot.py
```

**GUI Features:**
- 🖥️ **Modern Interface**: Clean, intuitive design
- 📊 **Real-time Logs**: Live logging with timestamps
- 🔄 **Dynamic Forms**: Fields change based on order type
- ⚡ **Async Operations**: Non-blocking order placement
- 📋 **Account Info**: View account details
- 🧹 **Log Management**: Clear logs easily

**Order Types in GUI:**
- **MARKET**: Immediate execution at current price
- **LIMIT**: Execution at specified price
- **STOP_MARKET**: Stop loss at specified price
- **OCO**: One-Cancels-the-Other (limit + stop orders)

### CLI Interface

#### 1. Market Order
```bash
python basic_bot.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

#### 2. Limit Order
```bash
python basic_bot.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 50000
```

#### 3. Stop Market Order
```bash
python basic_bot.py --symbol BTCUSDT --side SELL --order-type STOP_MARKET --quantity 0.001 --stop-price 45000
```

#### 4. OCO Order
```bash
python basic_bot.py --symbol BTCUSDT --side SELL --order-type OCO --quantity 0.001 --limit-price 50000 --stop-price 45000 --stop-limit-price 44900
```

#### 5. Get Account Information
```bash
python basic_bot.py --account-info
```

### Programmatic Usage

```python
from basic_bot import BasicBot

# Initialize bot
bot = BasicBot(api_key="your_api_key", api_secret="your_api_secret")

# Place a market order
result = bot.place_market_order("BTCUSDT", "BUY", 0.001)
print(result)

# Place a limit order
result = bot.place_limit_order("BTCUSDT", "SELL", 0.001, 50000)
print(result)

# Place a stop market order
result = bot.place_stop_market_order("BTCUSDT", "SELL", 0.001, 45000)
print(result)

# Place an OCO order
result = bot.place_oco_order("BTCUSDT", "SELL", 0.001, 50000, 45000, 44900)
print(result)

# Get account information
account_info = bot.get_account_info()
print(account_info)
```

## API Reference

### BasicBot Class

#### Constructor
```python
BasicBot(api_key: str = None, api_secret: str = None)
```

#### Methods

##### `place_market_order(symbol, side, quantity)`
Place a market order.

**Parameters:**
- `symbol` (str): Trading symbol (e.g., "BTCUSDT")
- `side` (str): Order side ("BUY" or "SELL")
- `quantity` (float): Order quantity

**Returns:** Dict with order details

##### `place_limit_order(symbol, side, quantity, price)`
Place a limit order.

**Parameters:**
- `symbol` (str): Trading symbol
- `side` (str): Order side ("BUY" or "SELL")
- `quantity` (float): Order quantity
- `price` (float): Order price

**Returns:** Dict with order details

##### `place_stop_market_order(symbol, side, quantity, stop_price)`
Place a stop market order.

**Parameters:**
- `symbol` (str): Trading symbol
- `side` (str): Order side ("BUY" or "SELL")
- `quantity` (float): Order quantity
- `stop_price` (float): Stop price

**Returns:** Dict with order details

##### `place_oco_order(symbol, side, quantity, limit_price, stop_price, stop_limit_price)`
Place an OCO (One-Cancels-the-Other) order.

**Parameters:**
- `symbol` (str): Trading symbol
- `side` (str): Order side ("BUY" or "SELL")
- `quantity` (float): Order quantity
- `limit_price` (float): Limit order price
- `stop_price` (float): Stop price
- `stop_limit_price` (float): Stop limit price

**Returns:** Dict with order details

##### `get_account_info()`
Get account information.

**Returns:** Dict with account details

##### `get_order_status(symbol, order_id)`
Get order status.

**Parameters:**
- `symbol` (str): Trading symbol
- `order_id` (int): Order ID

**Returns:** Dict with order status

## Order Types Explained

### Market Order
- **Purpose**: Immediate execution at current market price
- **Use Case**: Quick entry/exit when price is not critical
- **Risk**: Slippage may occur in volatile markets

### Limit Order
- **Purpose**: Execution only at specified price or better
- **Use Case**: Precise price control
- **Risk**: Order may not execute if price doesn't reach target

### Stop Market Order
- **Purpose**: Stop loss or take profit at specified price
- **Use Case**: Risk management and profit taking
- **Risk**: May execute at worse price due to slippage

### OCO Order (One-Cancels-the-Other)
- **Purpose**: Place two orders simultaneously - one cancels the other
- **Use Case**: Advanced risk management with profit taking
- **Components**: 
  - Limit order (take profit)
  - Stop limit order (stop loss)
- **Risk**: More complex but provides better control

## Response Format

All methods return a dictionary with the following structure:

```json
{
  "status": "SUCCESS",
  "order_type": "MARKET",
  "symbol": "BTCUSDT",
  "side": "BUY",
  "quantity": 0.001,
  "order_id": 123456789,
  "client_order_id": "abc123",
  "price": "50000.00",
  "timestamp": "2024-01-01T12:00:00",
  "raw_response": {...}
}
```

## Logging

All API requests, responses, and errors are logged to `logs/bot.log` with timestamps.

## Error Handling

The bot includes comprehensive error handling for:
- Invalid API credentials
- Invalid symbol format
- Invalid order parameters
- Network errors
- Binance API errors

## Security Notes

- ⚠️ **Never commit API credentials to version control**
- ⚠️ **Use environment variables for production**
- ⚠️ **This bot is configured for TESTNET only**
- ⚠️ **Test thoroughly before using with real funds**

## Testnet Information

- **Base URL**: https://testnet.binancefuture.com
- **Testnet API**: https://testnet.binancefuture.com
- **Testnet Website**: https://testnet.binancefuture.com

## Dependencies

- `python-binance==1.0.19`
- `requests==2.31.0`
- `python-dotenv==1.0.0`
- `tkinter` (included with Python)

## License

This project is for educational purposes. Use at your own risk.

## Disclaimer

This bot is for educational and testing purposes only. Trading cryptocurrencies involves risk. Always test thoroughly on testnet before using with real funds. 