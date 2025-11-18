import falcon
from dotenv import load_dotenv

from ikon_auth import IKonJWTVerifier

load_dotenv()
verifier = IKonJWTVerifier()


class PublicResource:
    def on_get(self, req, resp):
        resp.media = {"message": "Falcon public OK"}


class SecureResource:
    def on_get(self, req, resp):
        auth_header = req.get_header("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            resp.status = falcon.HTTP_401
            resp.media = {"error": "Missing or invalid Authorization header"}
            return

        token = auth_header.split(" ", 1)[1]

        try:
            claims = verifier.verify(token)
            resp.media = {"message": "Falcon secure OK", "claims": claims}
        except Exception as e:
            resp.status = falcon.HTTP_401
            resp.media = {"error": str(e)}


app = falcon.App()
app.add_route("/", PublicResource())
app.add_route("/secure", SecureResource())
