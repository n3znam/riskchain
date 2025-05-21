from colorama import Fore, Style, init
init(autoreset=True)

def print_report(address, report):
    print(f"\n{Style.BRIGHT}Analysis Report for: {address}{Style.RESET_ALL}\n")

    print(f"{Style.DIM}TX Count:{Style.RESET_ALL} {report['tx_count']}")
    print(f"{Style.DIM}Received:{Style.RESET_ALL} {report['received']} BTC")
    print(f"{Style.DIM}Sent:{Style.RESET_ALL} {report['sent']} BTC")
    print(f"{Style.DIM}Days Since Last Activity:{Style.RESET_ALL} {report['age_days']}")

    score_color = Fore.RED if report['risk_score'] >= 3 else Fore.YELLOW if report['risk_score'] == 2 else Fore.GREEN
    print(f"\n{Style.BRIGHT}Risk Score:{Style.RESET_ALL} {score_color}{report['risk_score']}/5{Style.RESET_ALL}\n")

    if not report['notes']:
        print(f"{Fore.GREEN}[✓] No suspicious activity detected. Address appears clean.")
        return

    print(f"{Style.BRIGHT}Notes:{Style.RESET_ALL}")
    for note in report['notes']:
        text = note['text'] if isinstance(note, dict) else str(note)
        severity = note.get("severity", 1) if isinstance(note, dict) else 1
        category = note.get("category", "general") if isinstance(note, dict) else "general"

        if severity == 3:
            color = Fore.RED
        elif severity == 2:
            color = Fore.YELLOW
        else:
            color = Fore.GREEN

        print(f" - {color}{text}{Style.RESET_ALL} {Style.DIM}[{category.upper()} | severity {severity}]{Style.RESET_ALL}")