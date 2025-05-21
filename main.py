from exporter import save_report
from validator import is_valid_btc_address, check_local_db, save_to_local_db
from public_fetcher import fetch_public_address_data as fetch_address_data
from analyzer import analyze_address
from report import print_report

def main():
    print("🟡 BTC Risk Check")
    print("🔍 Type a BTC adress for analyze:")

    address = input("> ").strip()

    if not is_valid_btc_address(address):
        print("Invalid address. Please enter a valid BTC address.")
        return

    local_data = check_local_db(address)
    if local_data:
        print("The address has already been parsed. Cached information is being used.\n")
        print_report(address, local_data)
        return

    print("Extracting information from the web...")
    address_data = fetch_address_data(address)
    if not address_data:
        print("Еxtraction failed")
        return

    source = address_data.get("source", "unknown").capitalize()
    print(f"The data was obtained from: {source}\n")

    analyzed = analyze_address(address_data)
    print("\nAnalyze finish:")
    print_report(address, analyzed)

    print("\nSave and exit...")
    save_report(address, analyzed, format="json")
    save_to_local_db(address, analyzed)
    print("Ready!")

if __name__ == "__main__":
    main()
