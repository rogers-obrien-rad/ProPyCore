![Contributors](https://img.shields.io/github/contributors/rogers-obrien-rad/ProPyCore)
![Last Commit](https://img.shields.io/github/last-commit/rogers-obrien-rad/ProPyCore)
[![Test Suite](https://github.com/rogers-obrien-rad/ProPyCore/actions/workflows/tests.yml/badge.svg)](https://github.com/rogers-obrien-rad/ProPyCore/actions/workflows/tests.yml)

![ro_logo](https://github.com/rogers-obrien-rad/general-template/blob/main/images/ro_logo.png)

# ProPyCore
_A Python-based connection with Procore that doesn't require a user authentication_

This package accesses Procore's API through the _Client Credentials_ [OAuth 2.0 grant type](https://developers.procore.com/documentation/oauth-choose-grant-type) which is meant for _Data Connection Applications_ i.e. "userless access".

## Installation
You can install this package with:

```bash
pip install ProPyCore
```

## Examples
To get started, you need to create an instance of a `Procore` object from `propycore.procore`. To do so, you will need to access information from your Procore Data Connection App:
* **Client ID**: Accessible from your app at [Procore Developers](https://developers.procore.com/signin) - will vary between sandbox and production modes
* **Client Secret**: Accessible from your app at [Procore Developers](https://developers.procore.com/signin) - will vary between sandbox and production modes
* **Redirect URI**: For data connection apps, this value will be "urn:ietf:wg:oauth:2.0:oob"
* **OAuth URL**: Will be "https://sandbox.procore.com" for sandbox environments or "https://app.procore.com" for production
* **Base URL**: Will be "https://sandbox.procore.com" for sandbox environments or "https://app.procore.com" for production

Once you have these values, you will use them as parameters in the `Procore` object:

```python
connection = Procore(
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    oauth_url=os.getenv("OAUTH_URL"),
    base_url=os.getenv("BASE_URL")
)
```

In this case, I have saved my App information as individual environment variables. For examples on how to access Procore information and create new object, see the [snippets](https://github.com/rogers-obrien-rad/ProPyCore/tree/main/snippets) folder for a rather exhaustive list. 

# Resources

### Procore:
* **[Procore Developer Dcoumentation](https://developers.procore.com/documentation/introduction)**: Various articles concerning the setup and use of Procore's API
* **[REST API Reference](https://developers.procore.com/reference/rest/v1/docs/rest-api-overview)**: Endpoints, response samples, and limited code snippets showcasing the use of the API. 

### GitHub Repositories
* **[Procore's Own Python Sample](https://github.com/procore/Procore-Sample-Python)**: Includes basic code to setup a Python Flash application but uses the other OAuth 2.0 grant type
* **[Python SDK for Procore](https://github.com/fylein/procore-sdk-py)**: Small SDK that includes basic code to work with Procore. Uses the other OAuth 2.0 grant type. 

# License
This repository is licensed through the [MIT License](https://github.com/rogers-obrien-rad/ProPyCore/blob/main/LICENSE). 
