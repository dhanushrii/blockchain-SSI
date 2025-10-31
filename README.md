# 🎓 Degree Verification using Self-Sovereign Identity (SSI)
---

## 🔍 Overview
This project implements a **Self-Sovereign Identity (SSI)** system on blockchain for **degree verification**.

It enables:
- **Issuers** to issue verified credentials (like degrees),
- **Holders** to securely control and share them, and
- **Verifiers** to check authenticity through blockchain.

The architecture includes:
- **Smart Contracts** (for blockchain logic)  
- **Backend API** (Flask / FastAPI)  
- **Frontend UI** (HTML, CSS, JavaScript)

### 💡 Why this matters
Traditional identity systems rely on centralized authorities and are prone to fraud and delays.  
SSI changes this by giving **full control to the user** — they hold their credentials and choose what to share.  
Blockchain ensures **immutability, transparency, and trust** among issuers, holders, and verifiers.

---

## ⚙️ Tech Stack Used

| Component | Technology |
|------------|-------------|
| **Blockchain** | Ethereum |
| **Smart Contracts** | Solidity, Hardhat, Sepolia Testnet |
| **Frontend** | HTML, CSS, JavaScript |
| **Backend** | Flask (Python Framework) |
| **Database** | SQLite |
| **Wallet** | MetaMask (for blockchain interaction) |

---

## ✨ Features
- 🧩 Decentralized identity using **DIDs** and **Verifiable Credentials**  
- 🔁 **Issuer → Holder → Verifier** credential flow  
- 🔐 Credentials stored **off-chain**, hashes stored **on-chain**  
- 🔎 Secure verification & immutability through blockchain  
- 💻 Simple **web UI + backend API** integration  

---

## 🧠 System Workflow
1. **Issuer** issues a verifiable credential (e.g., degree).  
2. **Holder** stores the credential and controls access.  
3. **Verifier** requests credential verification.  
4. **Blockchain** validates authenticity through stored hashes.  

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/dhanushrii/blockchain-SSI.git
cd blockchain-SSI
```

### 2️⃣ Install Backend Dependencies
```bash
python -m venv venv
source venv/bin/activate  # (use venv\Scripts\activate on Windows)
pip install -r requirements.txt
```

### 3️⃣ Deploy Smart Contract
```bash
cd contract
npx hardhat run scripts/deploy.js --network sepolia
```
> 💡 Make sure your MetaMask is connected to the **Sepolia Test Network** and has test ETH (use a Sepolia faucet).

### 4️⃣ Run Backend Server
```bash
uvicorn main:app --port 8001 --reload
```

### 5️⃣ Run Frontend
Open the file:
```
frontend/index.html
```
Then connect MetaMask (Sepolia network) to interact with the smart contract.

---

## 🪄 MetaMask Usage Guide

| Scenario | MetaMask Required? | Purpose |
|-----------|--------------------|----------|
| Local testing (Hardhat only) | ❌ No | Hardhat provides local test accounts |
| Frontend DApp interaction | ✅ Yes | Connects browser UI to blockchain |
| Deployment on Sepolia testnet | ✅ Yes | Signs and sends transactions |
| Backend-only testing | ❌ No | Use private key in `.env` instead |

> 🦊 **Tip:** MetaMask acts as the bridge between your DApp and the blockchain, managing keys and signing transactions.

---

## 🗄️ Database
- The backend uses **SQLite** for local storage.
- You can reset the backend data by deleting the `db.sqlite3` file.

---

## 🧪 Testing
To test smart contracts locally:
```bash
npx hardhat test
npx hardhat node
```
You can then deploy to a local network using:
```bash
npx hardhat run scripts/deploy.js --network localhost
```
---

## 📌 Notes
- Ensure MetaMask is set to **Sepolia Test Network**.
- Use a **Sepolia faucet** to get test ETH for contract deployment.
- You can re-deploy the contract anytime by rerunning the deploy script.
- Make sure backend (`http://localhost:8001`) and frontend are both running before use.
---
