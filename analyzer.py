
from abuse_checker import load_abuse_lists, check_abuse
from datetime import datetime
import time
import json

def load_known_tags(filepath='known_tags.json'):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except:
        return {}

def load_known_exchanges(filepath='exchanges.json'):
    try:
        with open(filepath, 'r') as f:
            return set(json.load(f))
    except:
        return set()

known_tags = load_known_tags()
known_exchanges = load_known_exchanges()

def analyze_address(data):
    stats = data.get("chain_stats", {})
    txs = data.get("txs", [])
    address = data.get("address", "")
    received = stats.get("funded_txo_sum", 0) / 1e8
    sent = stats.get("spent_txo_sum", 0) / 1e8
    tx_count = stats.get("tx_count", 0)
    last_seen = txs[0]['status']['block_time'] if txs else 0
    age_days = int((time.time() - last_seen) / 86400) if last_seen else None

    risk_score = 0
    notes = []
    flags = {}

    abuse_set, abuse_tags = load_abuse_lists()
    abuse_result = check_abuse(address, abuse_set, abuse_tags)
    if abuse_result["is_abusive"]:
        notes.append({
            "text": f"ABUSE FLAG: {abuse_result['tag'] or 'Reported abuse address'}",
            "severity": 3,
            "category": "abuse"
        })
        risk_score += abuse_result["score"]
        flags["is_abusive"] = True

    if address in known_tags:
        notes.append({
            "text": f"Tag: {known_tags[address]}",
            "severity": 3,
            "category": "label"
        })
        risk_score += 3
        flags["is_known"] = True

    if tx_count > 1000:
        notes.append({"text": "High transaction count (exchange or mixer)", "severity": 2, "category": "volume"})
        risk_score += 2
        flags["is_high_volume"] = True

    if received > 100:
        notes.append({"text": "Large amount received", "severity": 1, "category": "volume"})
        risk_score += 1

    if age_days and age_days > 365:
        notes.append({"text": "Dormant for over a year", "severity": 1, "category": "activity"})
        risk_score += 1
        flags["is_dormant"] = True

    reused_inputs = 0
    tx_times = []
    for tx in txs[:10]:
        inputs = tx.get("vin", [])
        reused_inputs += sum(1 for vin in inputs if vin.get("prevout", {}).get("scriptpubkey_address") == address)
        tx_times.append(tx.get("status", {}).get("block_time", 0))

    if reused_inputs >= 3:
        notes.append({"text": "Address appears to be reused multiple times (low privacy)", "severity": 2, "category": "privacy"})
        risk_score += 1
        flags["is_reused"] = True

    # Mixer pattern
    for tx in txs[:5]:
        if len(tx.get("vin", [])) >= 5 and len(tx.get("vout", [])) >= 5:
            notes.append({"text": "Mixer pattern detected (many inputs and outputs)", "severity": 3, "category": "mixer"})
            risk_score += 2
            flags["is_mixer"] = True
            break

    # Dust attack
    for tx in txs[:5]:
        for vout in tx.get("vout", []):
            value = vout.get("value", 0) / 1e8
            if value > 0 and value < 0.00001:
                notes.append({"text": "Dust attack pattern (tiny outputs)", "severity": 2, "category": "anomaly"})
                flags["is_dust"] = True
                risk_score += 1
                break

    # Transaction time analysis
    time_diffs = [t2 - t1 for t1, t2 in zip(tx_times[:-1], tx_times[1:]) if t1 and t2]
    if time_diffs:
        avg_diff = sum(time_diffs) / len(time_diffs)
        if avg_diff < 3600:
            notes.append({"text": "Frequent transactions detected (possible automation)", "severity": 2, "category": "timing"})
            risk_score += 1

    # Peeling chain detection
    for tx in txs[:5]:
        vouts = tx.get("vout", [])
        values = [v.get("value", 0) / 1e8 for v in vouts]
        if len(values) >= 2 and all(0.0005 < v < 1 for v in values[:-1]) and values[-1] < 0.0001:
            notes.append({"text": "Peeling chain pattern detected (progressive output reduction)", "severity": 2, "category": "peeling"})
            risk_score += 1
            flags["is_peeling"] = True
            break

    # Exchange detection
    for tx in txs[:5]:
        for vout in tx.get("vout", []):
            out_addr = vout.get("scriptpubkey_address")
            if out_addr in known_exchanges:
                notes.append({"text": "Funds sent to known exchange", "severity": 2, "category": "exchange"})
                risk_score += 1
                flags["exchange_out"] = True
                break

    # Fee analysis
    for tx in txs[:3]:
        inputs = tx.get("vin", [])
        outputs = tx.get("vout", [])
        in_sum = sum(vin.get("prevout", {}).get("value", 0) for vin in inputs)
        out_sum = sum(vout.get("value", 0) for vout in outputs)
        fee = (in_sum - out_sum) / 1e8 if in_sum > out_sum else 0
        if fee > 0.01:
            notes.append({"text": f"High transaction fee detected (~{fee:.5f} BTC)", "severity": 2, "category": "fee"})
            risk_score += 1
            break

    risk_score = min(risk_score, 5)

    return {
        "address": address,
        "tx_count": tx_count,
        "received": received,
        "sent": sent,
        "age_days": age_days,
        "risk_score": risk_score,
        "notes": notes,
        "flags": flags
    }
