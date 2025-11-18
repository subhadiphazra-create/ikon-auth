from aiohttp import web
from dotenv import load_dotenv

from ikon_auth import IKonJWTVerifier

load_dotenv()
verifier = IKonJWTVerifier()


async def public(request):
    return web.json_response({"message": "AIOHTTP public OK"})


async def secure(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return web.json_response(
            {"error": "Missing or invalid Authorization header"},
            status=401,
        )

    token = auth_header.split(" ", 1)[1]

    try:
        claims = verifier.verify(token)
        return web.json_response(
            {"message": "AIOHTTP secure OK", "claims": claims}, status=200
        )
    except Exception as e:
        return web.json_response({"error": str(e)}, status=401)


def create_app():
    app = web.Application()
    app.router.add_get("/", public)
    app.router.add_get("/secure", secure)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8205)
