import re
import json
import os

def is_valid_btc_address(address):
    """
    Поддържа:
    - Legacy (P2PKH):      1...
    - Script Hash (P2SH):  3...
    - SegWit (Bech32):     bc1q...
    - Taproot (Bech32m):   bc1p...
    """
    legacy_pattern = re.compile(r'^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$')
    bech32_pattern = re.compile(r'^(bc1)[0-9a-z]{8,87}$')  # 14–90 символа общо

    return bool(legacy_pattern.match(address) or bech32_pattern.match(address))

def check_local_db(address, db_path='btc_db.json'):
    if not os.path.exists(db_path):
        return None
    try:
        with open(db_path, 'r') as f:
            content = f.read().strip()
            if not content:
                print("[!] ⚠️ btc_db.json is empty. Ignored.")
                return None
            db = json.loads(content)
            return db.get(address)
    except json.JSONDecodeError:
        print("[!] ⚠️ btc_db.json is broken (invalid JSON). It is ignored.")
        return None
    except Exception as e:
        print(f"[!] ⚠️ Unexpected error reading db: {e}")
        return None

def save_to_local_db(address, report, db_path='btc_db.json'):
    db = {}
    if os.path.exists(db_path):
        try:
            with open(db_path, 'r') as f:
                content = f.read().strip()
                if content:
                    db = json.loads(content)
        except Exception as e:
            print(f"[!] Failed to load local DB: {e}")

    db[address] = report

    try:
        with open(db_path, 'w') as f:
            json.dump(db, f, indent=2)
        print(f"[✓] Cached analysis to local DB for {address}")
    except Exception as e:
        print(f"[!] Failed to save to local DB: {e}")
