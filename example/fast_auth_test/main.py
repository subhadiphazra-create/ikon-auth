from fastapi import FastAPI, Depends
from ikon_auth import verify_token

app = FastAPI(title="FastAPI + ikon-auth")

@app.get("/")
def public():
    return {"message": "FastAPI public OK"}

@app.get("/secure", dependencies=[Depends(verify_token)])
def secure(claims=Depends(verify_token)):
    return {
        "message": "FastAPI secure OK",
        "claims": claims,
    }
