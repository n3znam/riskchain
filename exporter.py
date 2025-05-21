import os
import json
from datetime import datetime


def save_report(address, report, format="json", directory="reports"):
    """
    Writes a report for a given address in JSON or TXT format.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H-%M")
    safe_address = address.replace("/", "_").replace("\\", "_")
    filename = f"{directory}/{safe_address}_{timestamp}.{format}"

    try:
        if format == "json":
            data = {
                "address": address,
                "report": report
            }
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)

        elif format == "txt":
            lines = [
                f"=== Bitcoin Address Risk Report ===",
                f"Address: {address}",
                f"TX Count: {report['tx_count']}",
                f"Received: {report['received']} BTC",
                f"Sent: {report['sent']} BTC",
                f"Days Since Last Activity: {report['age_days']}",
                f"Risk Score: {report['risk_score']}/5",
                f"Notes:"
            ]
            for note in report.get("notes", []):
                if isinstance(note, dict):
                    lines.append(
                        f" - {note['text']} [{note.get('category', 'info')} | severity {note.get('severity', 1)}]")
                else:
                    lines.append(f" - {note}")
            with open(filename, 'w') as f:
                f.write("\n".join(lines))

        else:
            print(f"[!] Unsupported format: {format}")
            return

        print(f"[✓] Report saved to {filename}")

    except Exception as e:
        print(f"[!] Failed to save report: {e}")
