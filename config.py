INFURA_URL = "https://sepolia.infura.io/v3/443a34dbee674e33874682921b2f66db"
CONTRACT_ADDRESS = "0x9E12CbCA8a35caC95c88e52172c8d66aC5B106C2"

# Paste your ABI JSON as a Python list below
CONTRACT_ABI = [
     {
      "inputs": [],
      "stateMutability": "nonpayable",
      "type": "constructor"
    },
    {
      "inputs": [],
      "name": "degreeCount",
      "outputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "",
          "type": "uint256"
        }
      ],
      "name": "degrees",
      "outputs": [
        {
          "internalType": "string",
          "name": "studentName",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "course",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "year",
          "type": "uint256"
        },
        {
          "internalType": "bool",
          "name": "verified",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "string",
          "name": "_name",
          "type": "string"
        },
        {
          "internalType": "string",
          "name": "_course",
          "type": "string"
        },
        {
          "internalType": "uint256",
          "name": "_year",
          "type": "uint256"
        }
      ],
      "name": "issueDegree",
      "outputs": [],
      "stateMutability": "nonpayable",
      "type": "function"
    },
    {
      "inputs": [],
      "name": "owner",
      "outputs": [
        {
          "internalType": "address",
          "name": "",
          "type": "address"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    },
    {
      "inputs": [
        {
          "internalType": "uint256",
          "name": "_id",
          "type": "uint256"
        }
      ],
      "name": "verifyDegree",
      "outputs": [
        {
          "internalType": "bool",
          "name": "",
          "type": "bool"
        }
      ],
      "stateMutability": "view",
      "type": "function"
    }
  ]
 
PRIVATE_KEY = "1f7cd0c9910523f403fea719c5b61be150c1730f0c4d10edc99ad02b12fa3a40"  # University wallet private key (DO NOT expose in real app)
ACCOUNT_ADDRESS = "0xd2f94b352fb72fa5a6a73a1c74726ab828802b0a"  # Public address of issuer 

