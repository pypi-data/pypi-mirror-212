import os

from mlflow.tracking.request_header.abstract_request_header_provider import (
    RequestHeaderProvider,
)

from .config import TrackingServerOIDCConfigError, read_settings
from .oidc_session import OIDCSession, OIDCSessionError

AUTHORIZATION_HEADER_KEY = "Authorization"


class PluginOIDCRequestHeaderProvider(RequestHeaderProvider):  # type: ignore[misc]
    """RequestHeaderProvider provided through plugin system"""

    def in_context(self) -> bool:
        return True

    def request_headers(self) -> dict[str, str]:
        try:
            settings = read_settings(match_uri=os.getenv("MLFLOW_TRACKING_URI"))
            with OIDCSession(
                issuer=settings.issuer,
                client_id=settings.client_id,
                redirect_uri=settings.redirect_uri,
                client_secret=settings.client_secret,
                scope=settings.scope,
                audience=settings.audience,
                interactive=settings.interactive,
            ) as session:
                token = (
                    session.id_token if settings.use_id_token else session.access_token
                )
                return {AUTHORIZATION_HEADER_KEY: f"{session.token_type} {token}"}
        except (TrackingServerOIDCConfigError, OIDCSessionError) as error:
            exit(f"[MLflow OIDC Plugin] {error}")
