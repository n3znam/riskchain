import os

def save_txt_report(address, report, directory="reports"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    filename = f"{directory}/{address}.txt"

    lines = [
        f"=== Bitcoin Address Risk Report ===\n",
        f"Address: {address}\n",
        f"TX Count: {report['tx_count']}",
        f"Received: {report['received']} BTC",
        f"Sent: {report['sent']} BTC",
        f"Days Since Last Activity: {report['age_days']}",
        f"Risk Score: {report['risk_score']}/5\n",
        "Notes:"
    ]

    for note in report.get("notes", []):
        lines.append(f" - {note}")

    try:
        with open(filename, "w") as f:
            f.write("\n".join(lines))
        print(f"[✓] TXT report saved to {filename}")
    except Exception as e:
        print(f"[!] Failed to save TXT report: {e}")
