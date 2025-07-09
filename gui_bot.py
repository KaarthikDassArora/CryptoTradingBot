#!/usr/bin/env python3
"""
GUI for BasicBot - A modern interface for Binance USDT-M Futures Testnet trading
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import threading
from datetime import datetime
from basic_bot import BasicBot


class BasicBotGUI:
    """Modern GUI for BasicBot"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("BasicBot - Binance USDT-M Futures Testnet")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Setup GUI (including log area) first
        self.setup_gui()
        self.setup_log_area()
        
        # Initialize bot
        self.bot = None
        self.setup_bot()
    
    def setup_bot(self):
        """Initialize the BasicBot"""
        try:
            self.bot = BasicBot(demo=self.demo_mode_var.get())
            self.log_message("✅ BasicBot initialized successfully")
        except Exception as e:
            # If log_text is not ready, just show a messagebox
            if hasattr(self, 'log_text'):
                self.log_message(f"❌ Error initializing BasicBot: {str(e)}")
            messagebox.showerror("Error", f"Failed to initialize BasicBot:\n{str(e)}")
    
    def setup_gui(self):
        """Setup the main GUI components"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="BasicBot - Binance USDT-M Futures Testnet", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # DEMO MODE checkbox
        self.demo_mode_var = tk.BooleanVar(value=False)
        demo_checkbox = ttk.Checkbutton(main_frame, text="Demo Mode (No API keys required, no real trades)", variable=self.demo_mode_var, command=self.on_demo_mode_toggle)
        demo_checkbox.grid(row=0, column=3, sticky=tk.E, padx=10)
        
        # Order Type Selection
        ttk.Label(main_frame, text="Order Type:", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
        self.order_type_var = tk.StringVar(value="MARKET")
        order_type_combo = ttk.Combobox(main_frame, textvariable=self.order_type_var, 
                                       values=["MARKET", "LIMIT", "STOP_MARKET", "OCO"], 
                                       state="readonly", width=15)
        order_type_combo.grid(row=1, column=1, sticky=tk.W, pady=5)
        order_type_combo.bind("<<ComboboxSelected>>", self.on_order_type_change)
        
        # Symbol
        ttk.Label(main_frame, text="Symbol:", font=("Arial", 12, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
        self.symbol_var = tk.StringVar(value="BTCUSDT")
        symbol_entry = ttk.Entry(main_frame, textvariable=self.symbol_var, width=20)
        symbol_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Side
        ttk.Label(main_frame, text="Side:", font=("Arial", 12, "bold")).grid(row=3, column=0, sticky=tk.W, pady=5)
        self.side_var = tk.StringVar(value="BUY")
        side_combo = ttk.Combobox(main_frame, textvariable=self.side_var, 
                                 values=["BUY", "SELL"], state="readonly", width=15)
        side_combo.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # Quantity
        ttk.Label(main_frame, text="Quantity:", font=("Arial", 12, "bold")).grid(row=4, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="0.001")
        quantity_entry = ttk.Entry(main_frame, textvariable=self.quantity_var, width=20)
        quantity_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # Price (for LIMIT orders)
        self.price_label = ttk.Label(main_frame, text="Price:", font=("Arial", 12, "bold"))
        self.price_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar(value="50000")
        self.price_entry = ttk.Entry(main_frame, textvariable=self.price_var, width=20)
        self.price_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # Stop Price (for STOP_MARKET orders)
        self.stop_price_label = ttk.Label(main_frame, text="Stop Price:", font=("Arial", 12, "bold"))
        self.stop_price_var = tk.StringVar(value="45000")
        self.stop_price_entry = ttk.Entry(main_frame, textvariable=self.stop_price_var, width=20)
        
        # OCO Order Fields
        self.oco_frame = ttk.LabelFrame(main_frame, text="OCO Order Settings", padding="10")
        
        # Limit Price for OCO
        ttk.Label(self.oco_frame, text="Limit Price:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=2)
        self.oco_limit_price_var = tk.StringVar(value="50000")
        ttk.Entry(self.oco_frame, textvariable=self.oco_limit_price_var, width=15).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Stop Price for OCO
        ttk.Label(self.oco_frame, text="Stop Price:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=2)
        self.oco_stop_price_var = tk.StringVar(value="45000")
        ttk.Entry(self.oco_frame, textvariable=self.oco_stop_price_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Stop Limit Price for OCO
        ttk.Label(self.oco_frame, text="Stop Limit Price:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=2)
        self.oco_stop_limit_price_var = tk.StringVar(value="44900")
        ttk.Entry(self.oco_frame, textvariable=self.oco_stop_limit_price_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=3, pady=20)
        
        # Place Order Button
        self.place_order_btn = ttk.Button(buttons_frame, text="Place Order", 
                                        command=self.place_order, style="Accent.TButton")
        self.place_order_btn.pack(side=tk.LEFT, padx=5)
        
        # Get Account Info Button
        ttk.Button(buttons_frame, text="Get Account Info", 
                  command=self.get_account_info).pack(side=tk.LEFT, padx=5)
        
        # Clear Logs Button
        ttk.Button(buttons_frame, text="Clear Logs", 
                  command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        
        # Status Label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               font=("Arial", 10), foreground="green")
        status_label.grid(row=7, column=0, columnspan=3, pady=10)
        
        # Initialize visibility
        self.on_order_type_change()
    
    def setup_log_area(self):
        """Setup the log display area"""
        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Logs", padding="10")
        log_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=10)
        
        # Configure grid weights for log area
        self.root.rowconfigure(1, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log Text Area
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initial log message
        self.log_message("🚀 BasicBot GUI started")
        self.log_message("📋 Configure your order settings above")
    
    def on_order_type_change(self, event=None):
        """Handle order type change"""
        order_type = self.order_type_var.get()
        
        # Hide all optional fields
        self.price_label.grid_remove()
        self.price_entry.grid_remove()
        self.stop_price_label.grid_remove()
        self.stop_price_entry.grid_remove()
        self.oco_frame.grid_remove()
        
        # Show relevant fields based on order type
        if order_type == "LIMIT":
            self.price_label.grid()
            self.price_entry.grid()
        elif order_type == "STOP_MARKET":
            self.stop_price_label.grid()
            self.stop_price_entry.grid()
        elif order_type == "OCO":
            self.oco_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
    
    def log_message(self, message):
        """Add message to log area"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        
        # Limit log size
        lines = self.log_text.get("1.0", tk.END).split('\n')
        if len(lines) > 1000:
            self.log_text.delete("1.0", "100.0")
    
    def clear_logs(self):
        """Clear the log area"""
        self.log_text.delete("1.0", tk.END)
        self.log_message("📝 Logs cleared")
    
    def validate_inputs(self):
        """Validate all input fields"""
        try:
            # Validate symbol
            symbol = self.symbol_var.get().strip().upper()
            if not symbol or not symbol.endswith('USDT'):
                raise ValueError("Symbol must end with USDT")
            
            # Validate side
            side = self.side_var.get()
            if side not in ['BUY', 'SELL']:
                raise ValueError("Side must be BUY or SELL")
            
            # Validate quantity
            quantity = float(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError("Quantity must be greater than 0")
            
            # Validate order type specific fields
            order_type = self.order_type_var.get()
            
            if order_type == "LIMIT":
                price = float(self.price_var.get())
                if price <= 0:
                    raise ValueError("Price must be greater than 0")
            
            elif order_type == "STOP_MARKET":
                stop_price = float(self.stop_price_var.get())
                if stop_price <= 0:
                    raise ValueError("Stop price must be greater than 0")
            
            elif order_type == "OCO":
                limit_price = float(self.oco_limit_price_var.get())
                stop_price = float(self.oco_stop_price_var.get())
                stop_limit_price = float(self.oco_stop_limit_price_var.get())
                
                if limit_price <= 0 or stop_price <= 0 or stop_limit_price <= 0:
                    raise ValueError("All OCO prices must be greater than 0")
                
                if side == "BUY":
                    if limit_price <= stop_price:
                        raise ValueError("For BUY orders: Limit price should be higher than stop price")
                else:  # SELL
                    if limit_price >= stop_price:
                        raise ValueError("For SELL orders: Limit price should be lower than stop price")
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Validation Error", str(e))
            return False
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {str(e)}")
            return False
    
    def place_order(self):
        """Place the order based on current settings"""
        if not self.validate_inputs():
            return
        
        if not self.bot:
            messagebox.showerror("Error", "BasicBot not initialized")
            return
        
        # Disable button during order placement
        self.place_order_btn.config(state="disabled")
        self.status_var.set("Placing order...")
        
        # Run order placement in separate thread
        threading.Thread(target=self._place_order_thread, daemon=True).start()
    
    def _place_order_thread(self):
        """Place order in separate thread"""
        try:
            order_type = self.order_type_var.get()
            symbol = self.symbol_var.get().strip().upper()
            side = self.side_var.get()
            quantity = float(self.quantity_var.get())
            
            self.log_message(f"📤 Placing {order_type} order: {side} {quantity} {symbol}")
            
            if order_type == "MARKET":
                result = self.bot.place_market_order(symbol, side, quantity)
            
            elif order_type == "LIMIT":
                price = float(self.price_var.get())
                result = self.bot.place_limit_order(symbol, side, quantity, price)
            
            elif order_type == "STOP_MARKET":
                stop_price = float(self.stop_price_var.get())
                result = self.bot.place_stop_market_order(symbol, side, quantity, stop_price)
            
            elif order_type == "OCO":
                limit_price = float(self.oco_limit_price_var.get())
                stop_price = float(self.oco_stop_price_var.get())
                stop_limit_price = float(self.oco_stop_limit_price_var.get())
                result = self.bot.place_oco_order(symbol, side, quantity, limit_price, stop_price, stop_limit_price)
            
            else:
                raise ValueError(f"Unsupported order type: {order_type}")
            
            # Update GUI in main thread
            self.root.after(0, self._handle_order_result, result)
            
        except Exception as e:
            self.root.after(0, self._handle_order_error, str(e))
    
    def _handle_order_result(self, result):
        """Handle order result in main thread"""
        self.place_order_btn.config(state="normal")
        
        # Debug logging
        self.log_message(f"🔍 Debug: Received result: {result}")
        
        if result.get('status') == 'SUCCESS':
            self.status_var.set("Order placed successfully")
            self.log_message("✅ Order placed successfully!")
            self.log_message(f"📋 Order ID: {result.get('order_id', 'N/A')}")
            self.log_message(f"💰 Price: {result.get('price', 'N/A')}")
            
            # Show detailed result
            result_str = json.dumps(result, indent=2)
            self.log_message(f"📄 Full Response:\n{result_str}")
            
            messagebox.showinfo("Success", "Order placed successfully!")
        else:
            self.status_var.set("Order failed")
            error_msg = result.get('error', 'Unknown error')
            self.log_message(f"❌ Order failed: {error_msg}")
            messagebox.showerror("Error", f"Order failed:\n{error_msg}")
    
    def _handle_order_error(self, error_msg):
        """Handle order error in main thread"""
        self.place_order_btn.config(state="normal")
        self.status_var.set("Order failed")
        self.log_message(f"❌ Error: {error_msg}")
        messagebox.showerror("Error", f"Order failed:\n{error_msg}")
    
    def get_account_info(self):
        """Get account information"""
        if not self.bot:
            messagebox.showerror("Error", "BasicBot not initialized")
            return
        
        self.log_message("📊 Fetching account information...")
        
        def fetch_account_info():
            try:
                result = self.bot.get_account_info()
                self.root.after(0, self._handle_account_info, result)
            except Exception as e:
                self.root.after(0, self._handle_account_error, str(e))
        
        threading.Thread(target=fetch_account_info, daemon=True).start()
    
    def _handle_account_info(self, result):
        """Handle account info result"""
        if result.get('status') == 'SUCCESS':
            self.log_message("✅ Account information retrieved")
            account_info = result.get('account_info', {})
            
            # Display key account information
            if 'totalWalletBalance' in account_info:
                self.log_message(f"💰 Total Balance: {account_info['totalWalletBalance']}")
            if 'totalUnrealizedProfit' in account_info:
                self.log_message(f"📈 Unrealized P&L: {account_info['totalUnrealizedProfit']}")
            
            # Show full response in log
            result_str = json.dumps(result, indent=2)
            self.log_message(f"📄 Full Account Info:\n{result_str}")
        else:
            error_msg = result.get('error', 'Unknown error')
            self.log_message(f"❌ Failed to get account info: {error_msg}")
            messagebox.showerror("Error", f"Failed to get account info:\n{error_msg}")
    
    def _handle_account_error(self, error_msg):
        """Handle account info error"""
        self.log_message(f"❌ Error getting account info: {error_msg}")
        messagebox.showerror("Error", f"Failed to get account info:\n{error_msg}")

    def on_demo_mode_toggle(self):
        """Re-initialize bot when demo mode is toggled"""
        self.setup_bot()
        self.log_message(f"Demo Mode is now {'ON' if self.demo_mode_var.get() else 'OFF'}.")


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')  # Use a modern theme
    
    # Create and run the GUI
    app = BasicBotGUI(root)
    
    # Start the GUI
    root.mainloop()


if __name__ == "__main__":
    main() 