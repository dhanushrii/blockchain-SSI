# ssi_wrapper.py
import subprocess
import json

def create_student_did():
    """
    Calls Node script to create a student DID and returns the DID as a Python dict
    """
    result = subprocess.run(
        ["node", "ssi_person2/Blockchain/create-dids.js"],
        capture_output=True,
        text=True
    )
    print("STDOUT:", result.stdout)   # Debug: what Node actually printed
    print("STDERR:", result.stderr)   # Debug: any Node errors

    if not result.stdout:
        raise Exception(f"Node script did not return any output. STDERR: {result.stderr}")
    
    return json.loads(result.stdout)  # assumes Node script prints JSON

def create_employer_did():
    """
    Calls Node script to create an employer DID
    """
    result = subprocess.run(
        ["node", "ssi_person2/Blockchain/create-employer-did.js"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def issue_vc(holder_did: str, degree: dict):
    """
    Calls Node script to issue a Verifiable Credential
    """
    payload = json.dumps({
        "holderDid": holder_did,
        "degree": degree
    })

    result = subprocess.run(
        ["node", "ssi_person2/blockchain/issue-credential.js", payload],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def verify_vc(vc: dict):
    """
    Calls Node script to verify a Verifiable Credential
    """
    payload = json.dumps(vc)
    result = subprocess.run(
        ["node", "ssi_person2/blockchain/verify-credential.js", payload],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)
