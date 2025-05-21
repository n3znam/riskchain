import requests

# Type a real api key
CHAINABUSE_KEY = "key"

# Primary BTC Address
address = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"

def test_chainabuse(address):
    url = f"https://api.chainabuse.com/api/reports?search={address}"
    headers = {"Authorization": f"Bearer {CHAINABUSE_KEY}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"HTTP Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"Chainabuse reports found: {len(data.get('data', []))}")
            for report in data.get("data", []):
                print(f"- Type: {report.get('category')}, Date: {report.get('created_at')}")
        else:
            print(" API returned error:", response.text)

    except Exception as e:
        print(f" Exception occurred: {e}")

# Running
if __name__ == "__main__":
    test_chainabuse(address)
