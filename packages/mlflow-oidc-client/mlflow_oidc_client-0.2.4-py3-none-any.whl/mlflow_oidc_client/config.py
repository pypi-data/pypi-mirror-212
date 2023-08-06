import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from oidc_client.config import DEFAULT_OIDC_SCOPE, DEFAULT_REDIRECT_URI

# FIXME: type-check when we drop support for Python 3.10
try:
    import tomllib
except ImportError:  # pragma: no cover
    import toml as tomllib  # type: ignore

DEFAULT_CONFIG_FILE = Path.cwd() / "pyproject.toml"


class TrackingServerOIDCConfigError(ValueError):
    """Raised on encountering a bad tracking server OIDC configuration."""

    pass


@dataclass(frozen=True)
class TrackingServerOIDCSettings:
    """OIDC provider configuration for a MLflow tracking server."""

    uri: str
    issuer: str
    client_id: str
    redirect_uri: str
    scope: str
    client_secret: str | None = None
    audience: str | None = None
    interactive: bool = False
    use_id_token: bool = False


@lru_cache
def read_settings(
    match_uri: str,
    path: Path = DEFAULT_CONFIG_FILE,
) -> TrackingServerOIDCSettings:
    """Read tracking server authorization settings for the matching URI."""
    matched_server_conf = {}
    try:
        with open(path) as config_file:
            data = tomllib.loads(config_file.read())
            known_server_confs = data["tool"]["mlflow-oidc-client"]["tracking-servers"]
            for server_conf in known_server_confs:
                if not server_conf.get("uri"):
                    continue
                if server_conf["uri"] == match_uri:
                    matched_server_conf = server_conf
    except (FileNotFoundError, KeyError, TypeError):
        pass

    issuer = os.getenv("MLFLOW_TRACKING_OIDC_ISSUER") or matched_server_conf.get(
        "issuer"
    )
    client_id = os.getenv("MLFLOW_TRACKING_OIDC_CLIENT_ID") or matched_server_conf.get(
        "client-id"
    )
    if not issuer or not client_id:
        raise TrackingServerOIDCConfigError(
            "a valid OIDC client configuration requires at least "
            "the issuer and client ID to be set "
            f"(matching config for '{match_uri}')."
        )

    client_secret = os.getenv(
        "MLFLOW_TRACKING_OIDC_CLIENT_SECRET"
    ) or matched_server_conf.get("client-secret")

    return TrackingServerOIDCSettings(
        uri=match_uri,
        issuer=issuer,
        client_id=client_id,
        redirect_uri=os.getenv("MLFLOW_TRACKING_OIDC_REDIRECT_URI")
        or matched_server_conf.get("redirect-uri")
        or DEFAULT_REDIRECT_URI,
        client_secret=client_secret,
        scope=os.getenv("MLFLOW_TRACKING_OIDC_SCOPE")
        or matched_server_conf.get("scope")
        or DEFAULT_OIDC_SCOPE,
        audience=os.getenv("MLFLOW_TRACKING_OIDC_AUDIENCE")
        or matched_server_conf.get("audience")
        or client_id,
        interactive=os.getenv(
            "MLFLOW_TRACKING_OIDC_INTERACTIVE",
            str(matched_server_conf.get("interactive", client_secret is None)),
        ).lower()
        in ("true", "yes", "1"),
        use_id_token=os.getenv(
            "MLFLOW_TRACKING_OIDC_USE_ID_TOKEN",
            str(matched_server_conf.get("use-id-token", client_secret is None)),
        ).lower()
        in ("true", "yes", "1"),
    )
