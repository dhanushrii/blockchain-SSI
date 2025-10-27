from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ssi_wrapper import create_student_did, create_employer_did, issue_vc, verify_vc

app = FastAPI(title="SSI Integration API")

class DIDRequest(BaseModel):
    type: str  # "student" or "employer"

class VCRequest(BaseModel):
    holder_did: str
    degree: dict

class VerifyRequest(BaseModel):
    vc: dict

@app.post("/dids")
async def create_did(req: DIDRequest):
    try:
        if req.type == "student":
            did = create_student_did()
        else:
            did = create_employer_did()
        return {"success": True, "did": did}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vcs/issue")
async def issue_vc_endpoint(req: VCRequest):
    try:
        vc = issue_vc(req.holder_did, req.degree)
        return {"success": True, "vc": vc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/vcs/verify")
async def verify_vc_endpoint(req: VerifyRequest):
    try:
        result = verify_vc(req.vc)
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
