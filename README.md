# FastAPI Azure AD Example

This is a simple example of how to set up a FastAPI REST API with Azure AD authentication.

## Overview of the Example

This example demonstrates how to protect FastAPI endpoints using Azure AD Bearer Token Authentication. It includes a secure endpoint that requires authentication and uses the MSAL library to validate the access token. The example also provides a testing endpoint to acquire a token for testing purposes.

## Workflow Overview

1. The application loads environment variables for Azure AD configuration.
2. The application creates an instance of the `ConfidentialClientApplication` from the `msal` library.
3. The `/get_token` endpoint is available for testing purposes to acquire a token. Note that in production, tokens should be requested from the client application, not from the server.
4. The `/secure` endpoint is protected and requires authentication. It uses the `OAuth2PasswordBearer` dependency to extract the access token from the Authorization header.
5. If no token is provided, the endpoint returns a `401 Unauthorized` response.
6. If a token is provided, it validates the token using MSAL. If the token is invalid, it returns a `403 Forbidden` response.
7. If the token is valid, it returns a `200 OK` response with the message: `{"Hello": "Secure World"}`.

## Setup

### Python Environment

Create a new Python environment and install the requirements:

```bash
conda create -n fastapi-azure-ad python=3.8 -y
conda activate fastapi-azure-ad
pip install -r requirements.txt
```

### Azure AD

Before you write any code, you'll need to register a new application in Azure AD to get your client id and client secret. This information will be used to configure your application's authentication settings.

1. Login to the Azure portal.
2. Navigate to Azure Active Directory.
3. Click on "App Registrations" and then "New Registration".
4. Provide a name for the application, select "Accounts in this organizational directory only", and then click "Register".
5. After the application is created, click on "Certificates & secrets" and then "New client secret". Take note of the client id and client secret - you will need these in the next step.

### Environment Variables

Set the following environment variables:

```bash
AZURE_AD_APP_CLIENT_ID = <client id from Azure AD> # Azure AD -> App Registrations -> <your app> -> Overview
AZURE_AD_APP_CLIENT_SECRET = <client secret from Azure AD> # Azure AD -> App Registrations -> <your app> -> Certificates & secrets
AZURE_AD_AUTHORITY = https://login.microsoftonline.com/<your tenant id> # Azure AD -> App Registrations -> <your app> -> Overview
```

### Run the Application

Run the following command to start the application:

```bash
python main.py
```

You can see the API documentation at [http://localhost:8000/docs](http://localhost:8000/docs).

### Test the Application

To test the application I have create a script that will acquire a token and then make a request to the secure endpoint. Run the following command to test the application:

```bash
python test.py
```

The script should output the following:

```json
{"Hello": "Secure World"}
```

Please note that this example is for educational purposes only and should not be considered production-ready. Proper security measures and best practices should be implemented for production deployments.

## References
- [FastAPI](https://fastapi.tiangolo.com/)
- [MSAL Python](https://github.com/AzureAD/microsoft-authentication-library-for-python)
- [Microsoft Authentication Library (MSAL) for Python](https://learn.microsoft.com/en-us/python/api/msal/overview-msal?view=msal-py-latest)