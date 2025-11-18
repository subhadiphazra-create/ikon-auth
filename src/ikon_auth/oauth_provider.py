from datetime import datetime, timedelta
from logging import getLogger
from typing import Optional, Dict, Any
import threading

import requests

from .config import settings

logger = getLogger(__name__)


class OAuthProvider:
    def __init__(self):
        self.oauth_url = f"{settings.base_issuer_url}/platform/oauth2/token"
        self.client_id = settings.oauth_client_id
        self.client_secret = settings.oauth_client_secret

        self._validate_credentials()

        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[datetime] = None
        self._lock = threading.Lock()

        logger.info("OAuthProvider initialized")

    def _validate_credentials(self) -> None:
        missing = []
        if not self.client_id:
            missing.append("oauth_client_id")
        if not self.client_secret:
            missing.append("oauth_client_secret")
        if not settings.base_issuer_url:
            missing.append("base_issuer_url")

        if missing:
            raise RuntimeError(
                f"Missing required OAuth environment variables: {', '.join(missing)}"
            )

    def _is_token_valid(self) -> bool:
        return (
            self._access_token is not None
            and self._token_expires_at is not None
            and datetime.now() < self._token_expires_at
        )

    def regenerate_token(self) -> Dict[str, Any]:
        payload = "grant_type=client_credentials"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        logger.info(f"Requesting new OAuth token from: {self.oauth_url}")

        response = requests.post(
            self.oauth_url,
            headers=headers,
            data=payload,
            auth=(self.client_id, self.client_secret),
            timeout=10,
        )

        logger.info(f"OAuth Response Status: {response.status_code}")
        response.raise_for_status()

        token_data = response.json()
        self._access_token = token_data["access_token"]
        self._token_expires_at = datetime.now() + timedelta(
            seconds=token_data["expires_in"]
        )

        logger.info("OAuth token generated successfully")
        return token_data

    def get_token(self) -> str:
        """
        Returns a Bearer token string, regenerating if expired.
        """
        with self._lock:
            if not self._is_token_valid():
                logger.info("Token invalid or expired – regenerating")
                self.regenerate_token()
            return f"Bearer {self._access_token}"
