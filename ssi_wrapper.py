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
    import subprocess, json

    payload = json.dumps({
        "holderDid": holder_did,
        "degree": degree
    })

    result = subprocess.run(
        ["node", "ssi_person2/Blockchain/issue-credential.js", payload],
        capture_output=True,
        text=True
    )

    if not result.stdout.strip():
        raise Exception(f"Node script did not return valid JSON. STDERR: {result.stderr}")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as e:
        raise Exception(f"Invalid JSON from Node: {result.stdout}\nError: {e}")


def verify_vc(vc: dict):
    """
    Calls Node script to verify a Verifiable Credential
    """
    # Convert Python dict → JSON string
    payload = json.dumps(vc)

    # Pass payload as argument to Node
    result = subprocess.run(
        ["node", "ssi_person2/blockchain/verify-credential.js", payload],
        capture_output=True,
        text=True
    )

    # Debugging (optional, comment out later)
    # print("STDOUT:", result.stdout)
    # print("STDERR:", result.stderr)

    # Handle empty or invalid JSON from Node
    if not result.stdout.strip():
        raise ValueError("Node script returned empty output")

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON output from Node: {result.stdout}")