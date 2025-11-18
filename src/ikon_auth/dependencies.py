from logging import getLogger

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException

from .jwks_provider import IKonJWTVerifier

logger = getLogger(__name__)

security = HTTPBearer()
jwt_verifier = IKonJWTVerifier()


def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials
    logger.info(f"Token Received: {token[:50]}...")

    try:
        result = jwt_verifier.verify(token)
        logger.info("Token Verified Successfully")
        return result
    except Exception as e:
        logger.error(f"Token Verification Failed: {str(e)}")
        raise HTTPException(
            status_code=403,
            detail=f"Invalid or expired token: {str(e)}",
        )
