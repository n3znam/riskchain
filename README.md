# RiskChain

**RiskChain** is a lightweight, privacy-focused tool to analyze any Bitcoin address for signs of abuse, sanctions, scams, or suspicious behavior using on-chain heuristics and public intelligence APIs.

## 🚀 Elevator Pitch

RiskChain: Analyze any Bitcoin address instantly for signs of abuse, sanctions, scams, or suspicious behavior using blockchain heuristics and public threat intelligence APIs.

---

## 📖 Project Story

### What inspired it?

While Bitcoin is transparent, it's notoriously difficult to assess the trustworthiness of a wallet address before sending or receiving funds. Most tools require switching between block explorers, abuse databases, and manual heuristics.

We wanted a tool that provides real-time, reliable, and automatic risk assessments for any BTC address — helping individuals, developers, and investigators make safer decisions.

**RiskChain** was created to close that gap by combining blockchain analysis with multiple external data sources and behavioral heuristics.

---

### How we built it

- **Language**: Python 3.8+
- **Core Features**:
  - Address format validation
  - Local database caching
  - Risk score generation (0–5 scale)
  - Abuse database and sanctions API integration
  - Heuristics-based behavior analysis
- **Public blockchain data sources**:
  - Blockstream.info
  - Mempool.space
  - Blockchair
- **Abuse & sanctions databases**:
  - Chainabuse
  - BitcoinAbuse
  - Chainalysis Sanctions API
  - BitcoinWhosWho
- **Output formats**:
  - JSON
  - TXT

---

### Heuristics implemented

- Reused address detection
- Dust attack pattern detection
- Mixer behavior (many inputs and outputs)
- Dormancy analysis (days since last activity)
- High transaction volume indicators

---

### What we learned

- Managing inconsistent API responses and rate limits
- Combining off-chain threat intelligence with on-chain behavior
- Building a modular, extensible risk analysis engine
- Creating readable and useful reports for both humans and machines

---

### Challenges we faced

- Public APIs occasionally failed or had rate limits
- Abuse databases are often incomplete or not up to date
- Designing fair and explainable risk scores
- Protecting API credentials while keeping the app lightweight

---

### Outcome

RiskChain enables:

- Safer Bitcoin transactions for users and businesses
- Faster investigations for researchers and forensic analysts
- Extensible infrastructure for threat intelligence automation

---

## ✅ Requirements

- Python 3.8+
- `requests`, `colorama`, `json`, `os`, `datetime`

Install dependencies:
```bash
pip install -r requirements.txt

🛠 Usage

Run the analyzer:

python3 main.py

Or test Chainabuse API independently:

python3 test_chainabuse.py
