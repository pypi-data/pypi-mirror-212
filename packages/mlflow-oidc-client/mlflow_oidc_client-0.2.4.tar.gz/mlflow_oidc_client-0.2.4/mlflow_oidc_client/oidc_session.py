import json
import threading
from dataclasses import asdict, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Type

import jwt
from oidc_client import AuthorizationError, TokenResponse, fetch_provider_config, login
from oidc_client.config import DEFAULT_OIDC_SCOPE, DEFAULT_REDIRECT_URI

# FIXME: type-check when we drop support for Python 3.10
try:
    from typing import Self
except ImportError:  # pragma: no cover
    from typing_extensions import Self

DEFAULT_CACHE_PATH = Path.home() / ".mlflow" / "oidc_client" / "cache"

JWT_CLAIM_EXPIRY = "exp"
JWT_OPTION_VERIFY_SIGNATURE = "verify_signature"

# Global session lock
lock = threading.Lock()


class OIDCSessionError(RuntimeError):
    """Raised when the OAuth 2.1 authorization flow fails."""

    pass


class OIDCSession:
    """Authentication session, caching proxy for OIDC Client's TokenResponse.

    Note: only a single active session is allowed globally, even if MLflow uses
    multiple threads.
    """

    def __init__(
        self,
        issuer: str,
        client_id: str,
        client_secret: str | None = None,
        redirect_uri: str = DEFAULT_REDIRECT_URI,
        audience: str | None = None,
        scope: str = DEFAULT_OIDC_SCOPE,
        interactive: bool = True,
        cache_path: Path = DEFAULT_CACHE_PATH,
    ):
        """Initialize session by reading cache or creating a new one."""
        self.issuer = issuer
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.audience = audience
        self.scope = scope
        self.interactive = interactive

        self._cache_file = cache_path / f"{client_id}.json"

        lock.acquire()
        try:
            with self._cache_file.open() as fd:
                self._cache = TokenResponse(**json.loads(fd.read()))
        except (TypeError, FileNotFoundError, json.JSONDecodeError):
            self.refresh_cache()

    def close(self) -> None:
        """Close the session and write cache to file."""
        self._cache_file.parent.mkdir(parents=True, exist_ok=True)

        with self._cache_file.open("w") as fd:
            fd.write(json.dumps(asdict(self._cache)))

        self._cache_file.chmod(0o600)
        lock.release()

    def refresh_cache(self) -> None:
        """Refresh the cached TokenResponse from the OAuth/OIDC authorization server."""
        try:
            self._cache = login(
                fetch_provider_config(self.issuer),
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                audience=self.audience,
                scope=self.scope,
                interactive=self.interactive,
            )
        except AuthorizationError as error:
            raise OIDCSessionError(f"authorization error: {error}")

        # Workaround 'created_at' not being set in strict OIDC mode (e.g. Auth0)
        if self._cache.created_at is None:
            self._cache = replace(
                self._cache, created_at=int(datetime.now(tz=timezone.utc).timestamp())
            )

    def __enter__(self) -> Self:
        """Enter the session context."""
        return self

    def __exit__(
        self, exc_type: Type[Exception], exc_value: Exception, traceback: str
    ) -> None:
        """Exit the session context, closing the session."""
        self.close()

    @property
    def token_type(self) -> str:
        """Return the cached token type."""
        return self._cache.token_type

    @property
    def access_token(self) -> str:
        """Return the access token (refreshes the cache if stale)."""
        if (
            not self._cache.access_token
            or not self._cache.created_at
            or not self._cache.expires_in
        ):
            self.refresh_cache()

        if not self._cache.created_at or not self._cache.expires_in:
            raise OIDCSessionError(
                "internal error: " "unable to determine access token expiry."
            )

        expiry = self._cache.created_at + self._cache.expires_in
        if int(datetime.now(tz=timezone.utc).timestamp()) >= expiry:
            self.refresh_cache()

        return self._cache.access_token

    @property
    def id_token(self) -> str:
        """Return the ID token (refreshes the cache if stale)."""
        if not self._cache.id_token:
            self.refresh_cache()

        if not self._cache.id_token:
            raise OIDCSessionError(
                "OIDC flow error: "
                "the authorization server did not include an ID token in its response."
            )

        claims = jwt.decode(
            self._cache.id_token, options={JWT_OPTION_VERIFY_SIGNATURE: False}
        )
        if int(datetime.now(tz=timezone.utc).timestamp()) >= claims[JWT_CLAIM_EXPIRY]:
            self.refresh_cache()

        return self._cache.id_token
