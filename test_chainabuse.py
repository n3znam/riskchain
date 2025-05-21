import requests
import sys
import io

# Fix for Unicode output in some terminal environments
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Type a real API key here
CHAINABUSE_KEY = "key"

# Test BTC address
address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

def test_chainabuse(address):
    if CHAINABUSE_KEY == "key":
        print("Error: Please enter a valid Chainabuse API key in CHAINABUSE_KEY.")
        return

    url = f"https://api.chainabuse.com/api/reports?search={address}"
    headers = {"Authorization": f"Bearer {CHAINABUSE_KEY}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"HTTP Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            reports = data.get("data", [])
            print(f"Chainabuse reports found: {len(reports)}")
            for report in reports:
                category = report.get("category", "Unknown")
                created_at = report.get("created_at", "Unknown")
                print(f"- Type: {category}, Date: {created_at}")
        else:
            print("API returned error response:")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
    except ValueError:
        print("Failed to parse JSON response.")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    test_chainabuse(address)
