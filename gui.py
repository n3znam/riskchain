import tkinter as tk
from tkinter import messagebox
from validator import is_valid_btc_address, check_local_db, save_to_local_db
from public_fetcher import fetch_public_address_data
from analyzer import analyze_address
from exporter import save_report

class BitcoinRiskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bitcoin Address Risk Checker")
        self.root.geometry("700x600")
        self.root.configure(bg="#f4f4f4")

        self.label = tk.Label(root, text="Enter a Bitcoin address:", font=("Arial", 14), bg="#f4f4f4")
        self.label.pack(pady=15)

        self.entry = tk.Entry(root, width=50, font=("Arial", 12))
        self.entry.pack(pady=5)

        self.check_button = tk.Button(
            root, text="Analyze", command=self.analyze,
            bg="#007acc", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5
        )
        self.check_button.pack(pady=10)

        self.output = tk.Text(root, height=25, width=80, font=("Courier New", 10))
        self.output.pack(pady=10)

    def analyze(self):
        address = self.entry.get().strip()
        self.output.delete(1.0, tk.END)

        if not is_valid_btc_address(address):
            messagebox.showerror("Error", "Invalid BTC address.")
            return

        local_data = check_local_db(address)
        if local_data:
            self.output.insert(tk.END, f"[Cached] Report for {address}:\n")
            self.display_report(address, local_data)
            return

        self.output.insert(tk.END, f"Fetching data for {address}...\n")
        data = fetch_public_address_data(address)
        if not data:
            messagebox.showerror("Error", "Failed to fetch data from public explorers.")
            return

        analyzed = analyze_address(data)
        save_report(address, analyzed, format="json")
        save_to_local_db(address, analyzed)
        self.output.insert(tk.END, f"\n[✓] Analysis complete:\n")
        self.display_report(address, analyzed)

    def display_report(self, address, report):
        self.output.insert(tk.END, f"Address: {address}\n")
        self.output.insert(tk.END, f"TX Count: {report['tx_count']}\n")
        self.output.insert(tk.END, f"Received: {report['received']} BTC\n")
        self.output.insert(tk.END, f"Sent: {report['sent']} BTC\n")
        self.output.insert(tk.END, f"Days Since Last Activity: {report['age_days']}\n")
        self.output.insert(tk.END, f"Risk Score: {report['risk_score']}/5\n")

        self.output.insert(tk.END, "\nNotes:\n")
        for note in report.get("notes", []):
            if isinstance(note, dict):
                self.output.insert(
                    tk.END,
                    f" - {note['text']} [{note.get('category', 'info').upper()} | severity {note.get('severity', 1)}]\n"
                )
            else:
                self.output.insert(tk.END, f" - {note}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BitcoinRiskGUI(root)
    root.mainloop()
