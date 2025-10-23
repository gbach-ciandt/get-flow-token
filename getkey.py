import httpx
import os
import time
from dotenv import load_dotenv
from datetime import datetime
import asyncio

TOKEN_FILE = "token.txt"

async def get_token():
    load_dotenv()
    api_token_url = os.getenv("TOKEN_API_URL")
    api_messages_url = os.getenv("MESSAGES_API_URL")
    client_id = os.getenv("CLIENT-ID")
    client_secret = os.getenv("CLIENT-SECRET")
    app_to_access = os.getenv("APPS")
    tenant = os.getenv("TENANT")
    token = ""

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{api_token_url}/token",
                headers={
                    'accept': '/',
                    'Content-Type': 'application/json',
                    'FlowTenant': tenant
                },
                json={
                    "clientId": client_id,
                    "clientSecret": client_secret,
                    "appToAccess": app_to_access
                }
            )

            resp.raise_for_status()  
            data = resp.json()
            token_expiration = time.time() + data.get("expires_in", 3600) - 60
            token = data["access_token"]

            with open(TOKEN_FILE, "w") as f:
                f.write(f"{token}")

            return token
    except Exception as e:
        print("Error: " + e)
        return ""

async def main():
    bearer_token = await get_token()
    if(bearer_token == ""):
        print("Error processing the request")


asyncio.run(main())