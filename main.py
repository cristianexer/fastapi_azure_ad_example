import os
import msal
import dotenv
import uvicorn
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, Depends, HTTPException, status


# load environment variables
dotenv.load_dotenv(dotenv.find_dotenv())
app = FastAPI(
    title="FastAPI Azure AD Bearer Token Authentication",
    description="A simple example of how to protect FastAPI endpoints with Azure AD Bearer Token Authentication",
    version="0.0.1",
    author="cristianexer",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

AZURE_AD_APP_CLIENT_ID = os.getenv('AZURE_AD_APP_CLIENT_ID', None)
AZURE_AD_APP_CLIENT_SECRET = os.getenv('AZURE_AD_APP_CLIENT_SECRET', None)
AZURE_AD_AUTHORITY = os.getenv('AZURE_AD_AUTHORITY', None)
AZURE_AD_APP_SCOPE = "https://graph.microsoft.com/.default"


clientapp = msal.ConfidentialClientApplication(
    client_id=AZURE_AD_APP_CLIENT_ID, authority=AZURE_AD_AUTHORITY, client_credential=AZURE_AD_APP_CLIENT_SECRET
)

# this endpoint is for testing purposes only - you should not expose this endpoint in production
# tokens should be requested from the client application and not from the server
@app.get("/get_token")
async def get_token():
    token = clientapp.acquire_token_for_client(AZURE_AD_APP_SCOPE)
    return JSONResponse(token)
############################################################################################################



@app.get("/secure")
async def secure_endpoint(token: str = Depends(oauth2_scheme)):
    """
    The secure_endpoint function is a FastAPI endpoint that requires authentication.
    It uses the OAuth2PasswordBearer dependency to get an access token from the Authorization header.
    If no token is provided, it raises HTTPException with status code 401 (Unauthorized).
    If a token is provided, it validates it using MSAL and returns {&quot;Hello&quot;: &quot;Secure World&quot;}.
    
    Parameters
    ----------
        token: str
            Pass the token to the function
    
    Returns
    -------
    
        A dictionary
    """
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Here, you would normally validate the token
    decoded_token = clientapp.acquire_token_for_client(AZURE_AD_APP_SCOPE)
    
    if 'error' in decoded_token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate the token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {"Hello": "Secure World"}


if __name__ == "__main__":
    uvicorn.run('main:app', host="localhost", port=8000, log_level="info", reload=True)
