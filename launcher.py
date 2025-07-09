#!/usr/bin/env python3
"""
Launcher script for BasicBot - Choose between CLI and GUI modes
"""

import sys
import subprocess
import os


def main():
    """Main launcher function"""
    print("🚀 BasicBot Launcher")
    print("=" * 40)
    print("Choose your interface:")
    print("1. GUI (Graphical User Interface) - Recommended")
    print("2. CLI (Command Line Interface)")
    print("3. Setup (Install dependencies and configure)")
    print("4. Test (Run unit tests)")
    print("5. Exit")
    print("=" * 40)
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("Launching GUI...")
                try:
                    subprocess.run([sys.executable, "gui_bot.py"], check=True)
                except FileNotFoundError:
                    print("❌ Error: gui_bot.py not found")
                except KeyboardInterrupt:
                    print("\n👋 GUI closed")
                break
                
            elif choice == "2":
                print("Launching CLI...")
                print("Usage examples:")
                print("  python basic_bot.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001")
                print("  python basic_bot.py --account-info")
                print("\nType 'python basic_bot.py --help' for more options")
                break
                
            elif choice == "3":
                print("Running setup...")
                try:
                    subprocess.run([sys.executable, "setup.py"], check=True)
                except FileNotFoundError:
                    print("❌ Error: setup.py not found")
                break
                
            elif choice == "4":
                print("Running tests...")
                try:
                    subprocess.run([sys.executable, "test_bot.py"], check=True)
                except FileNotFoundError:
                    print("❌ Error: test_bot.py not found")
                break
                
            elif choice == "5":
                print("👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main() 