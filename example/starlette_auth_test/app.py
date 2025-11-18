from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from dotenv import load_dotenv

from ikon_auth import IKonJWTVerifier

load_dotenv()
verifier = IKonJWTVerifier()


async def public(request: Request):
    return JSONResponse({"message": "Starlette public OK"})


async def secure(request: Request):
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.lower().startswith("bearer "):
        return JSONResponse(
            {"error": "Missing or invalid Authorization header"},
            status_code=401,
        )

    token = auth_header.split(" ", 1)[1]

    try:
        claims = verifier.verify(token)
        return JSONResponse(
            {"message": "Starlette secure OK", "claims": claims}, status_code=200
        )
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=401)


app = Starlette(
    routes=[
        Route("/", public),
        Route("/secure", secure),
    ]
)
