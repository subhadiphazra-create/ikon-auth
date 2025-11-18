import base64
from logging import getLogger

import requests
from jose import jwt, JWTError

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend

from .config import settings

logger = getLogger(__name__)


class IKonJWTVerifier:
    def __init__(self):
        base_api = settings.base_issuer_url

        self.issuer_config_url = f"{base_api}/platform/.well-known/openid-configuration"
        logger.info(f"Fetching OpenID configuration: {self.issuer_config_url}")

        self.jwks_url = self._fetch_jwks_url()
        logger.info(f"JWKS URL fetched: {self.jwks_url}")

        self.jwks_keys = self._fetch_jwks()
        logger.info(f"JWKS keys loaded: {list(self.jwks_keys.keys())}")

        self.issuer = f"{base_api}/platform"
        self.expected_audience = getattr(settings, "oauth_client_id", None)

    @staticmethod
    def _b64_decode(val: str) -> bytes:
        return base64.urlsafe_b64decode(val + "===")

    def _fetch_jwks_url(self) -> str:
        response = requests.get(self.issuer_config_url)
        response.raise_for_status()
        return response.json()["jwks_uri"]

    def _fetch_jwks(self) -> dict:
        response = requests.get(self.jwks_url)
        response.raise_for_status()
        keys = {}
        for k in response.json()["keys"]:
            keys[k["kid"]] = k
        return keys

    def _get_public_key_for_signature(self) -> dict:
        for k, key in self.jwks_keys.items():
            if key.get("use") == "sig":
                logger.info(f"Selected signature key: {k}")
                return key
        raise Exception("No signature key found in JWKS")

    def verify(self, token: str) -> dict:
        try:
            header = jwt.get_unverified_header(token)
            logger.info(f"Token Header: {header}")

            alg = header.get("alg")
            kid = header.get("kid")

            if not alg:
                raise Exception("Missing alg in JWT header")

            logger.info(f"JWT Algorithm: {alg}")
            logger.info(f"Token kid: {kid}")

            if not kid:
                logger.info("kid missing — selecting signature key automatically")
                key_data = self._get_public_key_for_signature()
            else:
                key_data = self.jwks_keys.get(kid)
                if key_data is None:
                    raise Exception(f"No JWKS key found matching kid: {kid}")

            n = int.from_bytes(self._b64_decode(key_data["n"]), "big")
            e = int.from_bytes(self._b64_decode(key_data["e"]), "big")

            numbers = rsa.RSAPublicNumbers(e, n)
            public_key_obj = numbers.public_key(default_backend())

            public_key = public_key_obj.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            ).decode()

            logger.info(f"Using issuer: {self.issuer}")
            logger.info(f"Expected audience: {self.expected_audience}")

            claims = jwt.decode(
                token,
                public_key,
                algorithms=[alg],
                issuer=self.issuer,
                options={
                    "verify_aud": False,   # same as your code
                    "verify_signature": True,
                },
            )

            logger.info(f"Decoded Claims: {claims}")
            return claims

        except JWTError as e:
            logger.error(f"JWT decoding error: {str(e)}")
            raise Exception(f"JWT verification failed: {str(e)}")

        except Exception as e:
            logger.error(f"Unexpected verification error: {str(e)}")
            raise Exception(f"Unexpected token validation error: {str(e)}")
