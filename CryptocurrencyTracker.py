import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time
import os
from tabulate import tabulate
s
class CryptoPriceTracker:
    def __init__(self):
        self.api_url = "https://api.coingecko.com/api/v3"
        self.currencies = ["bitcoin", "ethereum", "solana", "cardano", "dogecoin"]
        self.prices_history = {}
        self.current_prices = {}
        
    def fetch_current_prices(self, vs_currency="usd"):
        """Fetch current prices for selected cryptocurrencies."""
        currencies_str = ",".join(self.currencies)
        endpoint = f"{self.api_url}/simple/price"
        params = {
            "ids": currencies_str,
            "vs_currencies": vs_currency,
            "include_market_cap": "true",
            "include_24hr_vol": "true",
            "include_24hr_change": "true"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            data = response.json()
            
            self.current_prices = data
            return data
        except Exception as e:
            print(f"Error fetching current prices: {e}")
            return None
    
    def fetch_historical_data(self, currency="bitcoin", days=30, vs_currency="usd"):
        """Fetch historical data for a cryptocurrency."""
        endpoint = f"{self.api_url}/coins/{currency}/market_chart"
        params = {
            "vs_currency": vs_currency,
            "days": days,
            "interval": "daily"
        }
        
        try:
            response = requests.get(endpoint, params=params)
            data = response.json()
            
            # Convert to DataFrame
            prices = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
            prices["date"] = pd.to_datetime(prices["timestamp"], unit="ms")
            
            self.prices_history[currency] = prices
            return prices
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return None
    
    def display_current_prices(self):
        """Display current prices in a formatted table."""
        if not self.current_prices:
            self.fetch_current_prices()
            
        if not self.current_prices:
            print("No price data available.")
            return
            
        table_data = []
        headers = ["Currency", "Price (USD)", "24h Change (%)", "Market Cap", "24h Volume"]
        
        for currency in self.currencies:
            if currency in self.current_prices:
                data = self.current_prices[currency]
                table_data.append([
                    currency.capitalize(),
                    f"${data['usd']:,.2f}",
                    f"{data['usd_24h_change']:,.2f}%",
                    f"${data['usd_market_cap']:,.0f}",
                    f"${data['usd_24h_vol']:,.0f}"
                ])
                
        print("\n" + tabulate(table_data, headers=headers, tablefmt="pretty") + "\n")
    
    def plot_historical_data(self, currencies=None, days=30):
        """Plot historical price data for specified cryptocurrencies."""
        if currencies is None:
            currencies = self.currencies[:3]  # Default to top 3
            
        plt.figure(figsize=(12, 6))
        
        for currency in currencies:
            if currency not in self.prices_history:
                self.fetch_historical_data(currency, days)
                
            if currency in self.prices_history:
                df = self.prices_history[currency]
                plt.plot(df["date"], df["price"], label=currency.capitalize())
        
        plt.title(f"Cryptocurrency Prices - Last {days} Days")
        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        # Save and show plot
        plot_file = f"crypto_prices_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        plt.savefig(plot_file)
        print(f"Plot saved as {plot_file}")
        plt.show()
        
    def set_alert(self, currency, target_price, alert_type="above"):
        """Set a price alert for a cryptocurrency."""
        print(f"Alert set for {currency}: {alert_type} ${target_price}")
        
        while True:
            current = self.fetch_current_prices()
            
            if current and currency in current:
                current_price = current[currency]["usd"]
                
                print(f"{currency.capitalize()} current price: ${current_price:,.2f}", end="\r")
                
                if (alert_type == "above" and current_price >= target_price) or \
                   (alert_type == "below" and current_price <= target_price):
                    print(f"\nALERT: {currency.capitalize()} is now ${current_price:,.2f}!")
                    break
            
            time.sleep(60)  # Check every minute
            
    def export_data(self, format="csv"):
        """Export cryptocurrency data to a file."""
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        
        if not self.current_prices:
            self.fetch_current_prices()
            
        # Export current prices
        df_current = pd.DataFrame()
        
        for currency in self.currencies:
            if currency in self.current_prices:
                data = self.current_prices[currency]
                temp_df = pd.DataFrame({
                    "currency": [currency],
                    "price_usd": [data["usd"]],
                    "change_24h": [data["usd_24h_change"]],
                    "market_cap": [data["usd_market_cap"]],
                    "volume_24h": [data["usd_24h_vol"]],
                    "timestamp": [datetime.now()]
                })
                df_current = pd.concat([df_current, temp_df])
        
        if format == "csv":
            filename = f"crypto_prices_{now}.csv"
            df_current.to_csv(filename, index=False)
        elif format == "excel":
            filename = f"crypto_prices_{now}.xlsx"
            df_current.to_excel(filename, index=False)
            
        print(f"Data exported to {filename}")

def main():
    tracker = CryptoPriceTracker()
    
    while True:
        print("\nCryptocurrency Price Tracker")
        print("---------------------------")
        print("1. Display current prices")
        print("2. View historical price chart")
        print("3. Set price alert")
        print("4. Export data")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            tracker.display_current_prices()
            
        elif choice == '2':
            days = int(input("Enter number of days for historical data (max 365): "))
            currencies = input("Enter cryptocurrencies to chart (comma-separated) or press Enter for default: ")
            
            if currencies:
                currencies_list = [c.strip().lower() for c in currencies.split(",")]
            else:
                currencies_list = None
                
            tracker.plot_historical_data(currencies_list, days)
            
        elif choice == '3':
            currency = input("Enter cryptocurrency name: ").lower()
            target_price = float(input("Enter target price (USD): "))
            alert_type = input("Alert when price goes 'above' or 'below' target? ").lower()
            
            if alert_type not in ['above', 'below']:
                print("Invalid alert type. Setting to 'above'.")
                alert_type = 'above'
                
            print(f"Starting alert for {currency}. Press Ctrl+C to cancel.")
            try:
                tracker.set_alert(currency, target_price, alert_type)
            except KeyboardInterrupt:
                print("\nAlert canceled.")
                
        elif choice == '4':
            format_type = input("Export as 'csv' or 'excel'? ").lower()
            if format_type not in ['csv', 'excel']:
                print("Invalid format. Using CSV.")
                format_type = 'csv'
                
            tracker.export_data(format_type)
            
        elif choice == '5':
            print("Thank you for using the Cryptocurrency Price Tracker!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
