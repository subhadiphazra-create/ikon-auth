from bottle import route, run, request, response
from dotenv import load_dotenv

from ikon_auth import IKonJWTVerifier

load_dotenv()
verifier = IKonJWTVerifier()


@route("/")
def public():
    response.content_type = "application/json"
    return {"message": "Bottle public OK"}


@route("/secure")
def secure():
    auth_header = request.get_header("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        response.status = 401
        return {"error": "Missing or invalid Authorization header"}

    token = auth_header.split(" ", 1)[1]

    try:
        claims = verifier.verify(token)
        return {"message": "Bottle secure OK", "claims": claims}
    except Exception as e:
        response.status = 401
        return {"error": str(e)}


if __name__ == "__main__":
    run(host="0.0.0.0", port=8008, debug=True, reloader=True)
