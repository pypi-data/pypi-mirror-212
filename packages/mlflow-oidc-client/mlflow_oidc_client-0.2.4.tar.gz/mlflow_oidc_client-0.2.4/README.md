MLflow Client OIDC/OAuth 2.1 Plugin
===================================

MLflow plugin adding OIDC/OAuth 2.1 authorization support to the client, allowing the use of a tracking server secured behind a compatible proxy.

The plugin is built with [OIDC Client](https://gitlab.com/lzinsou/oidc-client) and supports the same OIDC/OAuth 2.1 authorization flows:
- the **authorization code** flow, for interactive user login;
- the **client credentials** flow, for confidential machine-to-machine communication.

This plugin supports reading authorization settings from `pyproject.toml`.


Requirements
------------

Python 3.10+  
MLflow or MLflow Skinny 2+


Installation
------------

```console
pip install mlflow-oidc-client
```


Getting Started
---------------

First, add the following to the project's `pyproject.toml` configuration file:
```toml
[[tool.mlflow-oidc-client.tracking-servers]]
uri = "http://mlflow.example.com/"            # URI of your MLflow Tracking Server
issuer = "https://auth.example.com/"          # URI of your OIDC provider
client-id = "<application ID>"                # Client ID of your project
```

You can now run MLflow client commands without any change. The plugin will match the `MLFLOW_TRACKING_URI` environment variable to the appropriate server configuration found in `pyproject.toml`.
```console
# To list logged experiments:
MLFLOW_TRACKING_URI=http://mlflow.example.com/ mlflow experiments search
```


Configuration
-------------

Options may be set with environment variables or in the `pyproject.toml` configuration file, with environment variables taking precedence.

Each tracking server has its own `[[tool.mlflow-oidc-client.tracking-servers]]` block, which can be given multiple times in the same `pyproject.toml`.

|Environment Variable|Config File|Default Value|Description|
|-|-|-|-|
|MLFLOW_TRACKING_URI|N/A|N/A|MLflow Tracking Server URI|
|MLFLOW_TRACKING_OIDC_ISSUER|issuer|`None` (required)|OIDC authorization issuer URI|
|MLFLOW_TRACKING_OIDC_CLIENT_ID|client-id|`None` (required)|OIDC client ID|
|MLFLOW_TRACKING_OIDC_CLIENT_SECRET|client-secret|`None`|OIDC client secret|
|MLFLOW_TRACKING_OIDC_REDIRECT_URI|redirect-uri|`"http://127.0.0.1:39303/oauth2/callback"`|OIDC redirect URI|
|MLFLOW_TRACKING_OIDC_SCOPE|scope|`"openid profile email"`|OIDC token scope|
|MLFLOW_TRACKING_OIDC_AUDIENCE|audience|Same as the client ID|OIDC token audience|
|MLFLOW_TRACKING_OIDC_INTERACTIVE|interactive|Interactive by default if the application is public (no client secret)|Require a user login in a browser|
|MLFLOW_TRACKING_OIDC_USE_ID_TOKEN|use-id-token|Use the ID token by default if the application is public (no client secret)|Use the ID token instead of the access token as `Bearer` token in the `Authorization` HTTP header|


Examples
--------

Basic configuration providing interactive login for users:
```toml
[[tool.mlflow-oidc-client.tracking-servers]]
uri = "http://mlflow.example.com/"
issuer = "https://auth.example.com/"
client-id = "<application ID>"
```

Basic configuration for a machine-to-machine scenario (no interactive login required):
```toml
[[tool.mlflow-oidc-client.tracking-servers]]
uri = "http://mlflow.example.com/"
issuer = "https://auth.example.com/"
client-id = "<application ID>"
client-secret = "<application ID>"
audience = "<audience>"  # Required by some providers (e.g. Auth0)
```

To avoid committing the client secret to git, you may pass it as the `MLFLOW_TRACKING_OIDC_CLIENT_SECRET` environment variable.


License
-------

This project is licensed under the terms of the MIT license.


A [yzr](https://www.yzr.ai/) Free and Open Source project.
