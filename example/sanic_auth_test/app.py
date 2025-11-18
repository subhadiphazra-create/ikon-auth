from sanic import Sanic
from sanic.response import json
from dotenv import load_dotenv

from ikon_auth import IKonJWTVerifier

load_dotenv()

app = Sanic("sanic_ikon_auth_test")
verifier = IKonJWTVerifier()


@app.get("/")
async def public(request):
    return json({"message": "Sanic public OK"})


@app.get("/secure")
async def secure(request):
    auth_header = request.headers.get("authorization")

    if not auth_header or not auth_header.lower().startswith("bearer "):
        return json(
            {"error": "Missing or invalid Authorization header"},
            status=401,
        )

    token = auth_header.split(" ", 1)[1]

    try:
        claims = verifier.verify(token)
        return json({"message": "Sanic secure OK", "claims": claims})
    except Exception as e:
        return json({"error": str(e)}, status=401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004, dev=True)
