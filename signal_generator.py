Add Deriv signal generator codeimport requests
import time

# Deriv API endpoint for live ticks
API_URL = "https://www.deriv.com/api/v1/ticks?symbol=R_100"

def get_latest_price():
    try:
        response = requests.get(API_URL)
        data = response.json()
        price = float(data["tick"]["quote"])
        return price
    except:
        return None

def calculate_volatility(prices):
    if len(prices) < 2:
        return 0
    returns = [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
    avg_volatility = sum(returns) / len(returns)
    return avg_volatility

def generate_signal(volatility):
    # Simple rule: if volatility > threshold → High, else Low
    threshold = 5  # Adjust this based on your asset scale
    confidence = min(100, volatility * 10)  # Example confidence percentage
    if volatility > threshold:
        return "High Volatility", confidence
    else:
        return "Low Volatility", confidence

def main():
    prices = []
    while True:
        price = get_latest_price()
        if price:
            prices.append(price)
            if len(prices) > 10:  # Keep only last 10 prices
                prices.pop(0)
            volatility = calculate_volatility(prices)
            signal, confidence = generate_signal(volatility)
            print(f"Price: {price:.2f} | Signal: {signal} | Confidence: {confidence:.1f}%")
        else:
            print("Failed to fetch price.")
        time.sleep(1)  # Wait 1 second before next tick

if __name__ == "__main__":
    main()
