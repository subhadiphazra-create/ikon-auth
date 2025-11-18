import tornado.ioloop
import tornado.web
from dotenv import load_dotenv

from ikon_auth import IKonJWTVerifier

load_dotenv()
verifier = IKonJWTVerifier()


class PublicHandler(tornado.web.RequestHandler):
    def get(self):
        self.write({"message": "Tornado public OK"})


class SecureHandler(tornado.web.RequestHandler):
    def get(self):
        auth_header = self.request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            self.set_status(401)
            self.write({"error": "Missing or invalid Authorization header"})
            return

        token = auth_header.split(" ", 1)[1]

        try:
            claims = verifier.verify(token)
            self.write({"message": "Tornado secure OK", "claims": claims})
        except Exception as e:
            self.set_status(401)
            self.write({"error": str(e)})


def make_app():
    return tornado.web.Application(
        [
            (r"/", PublicHandler),
            (r"/secure", SecureHandler),
        ]
    )


if __name__ == "__main__":
    app = make_app()
    app.listen(8056)
    tornado.ioloop.IOLoop.current().start()
