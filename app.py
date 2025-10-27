from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from web3 import Web3
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import INFURA_URL, CONTRACT_ADDRESS, CONTRACT_ABI, PRIVATE_KEY, ACCOUNT_ADDRESS
import time

app = Flask(__name__)
CORS(app)
api = Api(app, doc="/docs", version="1.0", title="Degree Verification API")

CONTRACT_ADDRESS = Web3.to_checksum_address(CONTRACT_ADDRESS)
ACCOUNT_ADDRESS = Web3.to_checksum_address(ACCOUNT_ADDRESS)
# Blockchain setup
web3 = Web3(Web3.HTTPProvider(INFURA_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to Ethereum network")
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Database setup
Base = declarative_base()
engine = create_engine("sqlite:///db.sqlite3")
Session = sessionmaker(bind=engine)
session = Session()

class Degree(Base):
    __tablename__ = "degrees"
    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    student_id = Column(String)
    degree_hash = Column(String, unique=True)
    status = Column(String)

Base.metadata.create_all(engine)

# ====================
# Swagger models
# ====================
degree_model = api.model('Degree', {
    'student_name': fields.String(required=True),
    'student_id': fields.String(required=True),
    'degree_hash': fields.String(required=True)
})

verify_model = api.model('Verify', {
    'degree_hash': fields.String(required=True)
})

# ====================
# API Resources
# ====================
@api.route("/home")
class Home(Resource):
    def get(self):
        return {"message": "Welcome to Degree Verification API"}

@api.route("/issue-degree")
class IssueDegree(Resource):
    @api.expect(degree_model)
    def post(self):
        data = request.json
        student_name = data.get("student_name")
        student_id = data.get("student_id")
        degree_hash = data.get("degree_hash")  # string

        if not all([student_name, student_id, degree_hash]):
            return {"error": "Missing fields"}, 400

        try:
            timestamp = int(time.time())
            nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)

            # Build transaction (send string; Solidity will handle keccak inside)
            txn = contract.functions.issueDegree(
                student_id,
                degree_hash,  # string
                timestamp
            ).build_transaction({
                "chainId": 11155111,
                "gas": 200000,
                "gasPrice": web3.eth.gas_price,
                "nonce": nonce,
            })

            signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

            # Save locally
            degree = Degree(
                student_name=student_name,
                student_id=student_id,
                degree_hash=degree_hash,
                status="Issued"
            )
            session.add(degree)
            session.commit()

            return {
                "message": "Degree issued successfully!",
                "transaction_hash": tx_hash.hex(),
                "block_number": receipt.blockNumber,
                "timestamp": timestamp
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500

# ----------------
# Verify Degree
# ----------------
@api.route("/verify-degree")
class VerifyDegree(Resource):
    @api.expect(verify_model)
    def post(self):
        data = request.json
        degree_hash = data.get("degree_hash")

        if not degree_hash:
            return {"error": "Missing degree_hash"}, 400

        try:
            # Convert string to uint256 using keccak to match Solidity storage
            degree_hash_int = int(Web3.keccak(text=degree_hash).hex(), 16)
            is_valid = contract.functions.verifyDegree(degree_hash_int).call()

            # Update DB status
            degree = session.query(Degree).filter_by(degree_hash=degree_hash).first()
            if degree:
                degree.status = "Verified" if is_valid else "Invalid"
                session.commit()

            return {"degree_hash": degree_hash, "is_valid": is_valid}, 200

        except Exception as e:
            return {"error": str(e)}, 500


@api.route("/degrees")
class ListDegrees(Resource):
    def get(self):
        degrees = session.query(Degree).all()
        output = [{
            "student_name": d.student_name,
            "student_id": d.student_id,
            "degree_hash": d.degree_hash,
            "status": d.status
        } for d in degrees]
        return output, 200

if __name__ == "__main__":
    app.run(debug=True)
