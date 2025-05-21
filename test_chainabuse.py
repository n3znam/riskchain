import requests

# Въведи своя реален API ключ тук:
CHAINABUSE_KEY = "ca_ТВОЯ_КЛЮЧ_ТУК"

# Примерен BTC адрес за тестване
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
            print("❌ API returned error:", response.text)

    except Exception as e:
        print(f"❌ Exception occurred: {e}")

# Изпълнение
if __name__ == "__main__":
    test_chainabuse(address)
