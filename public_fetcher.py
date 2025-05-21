import requests

BLOCKSTREAM_BASE = "https://blockstream.info/api"
BLOCKCHAIR_BASE = "https://api.blockchair.com/bitcoin/dashboards/address"
MEMPOOL_BASE = "https://mempool.space/api"

def fetch_from_blockstream(address):
    try:
        info = requests.get(f"{BLOCKSTREAM_BASE}/address/{address}").json()
        txs = requests.get(f"{BLOCKSTREAM_BASE}/address/{address}/txs").json()
        return {
            "source": "blockstream",
            "address": address,
            "chain_stats": info.get("chain_stats", {}),
            "mempool_stats": info.get("mempool_stats", {}),
            "txs": txs[:10]  # limit for performance
        }
    except Exception as e:
        print(f"[Blockstream Error] {e}")
        return None

def fetch_from_blockchair(address):
    try:
        resp = requests.get(f"{BLOCKCHAIR_BASE}/{address}")
        data = resp.json()["data"][address]
        return {
            "source": "blockchair",
            "address": address,
            "chain_stats": data.get("address", {}),
            "txs": data.get("transactions", [])[:10]
        }
    except Exception as e:
        print(f"[Blockchair Error] {e}")
        return None

def fetch_from_mempool(address):
    try:
        info = requests.get(f"{MEMPOOL_BASE}/address/{address}").json()
        txs = requests.get(f"{MEMPOOL_BASE}/address/{address}/txs").json()
        return {
            "source": "mempool.space",
            "address": address,
            "chain_stats": info.get("chain_stats", {}),
            "mempool_stats": info.get("mempool_stats", {}),
            "txs": txs[:10]
        }
    except Exception as e:
        print(f"[Mempool Error] {e}")
        return None

def fetch_public_address_data(address):
    print("[~] Trying Blockstream...")
    data = fetch_from_blockstream(address)
    if data: return data

    print("[~] Trying Mempool.space...")
    data = fetch_from_mempool(address)
    if data: return data

    print("[~] Trying Blockchair...")
    data = fetch_from_blockchair(address)
    if data: return data

    print("[!] All public sources failed.")
    return None
